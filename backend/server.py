from fastapi import FastAPI, APIRouter, HTTPException
from fastapi.responses import JSONResponse, Response, FileResponse
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any, Tuple
import uuid
from datetime import datetime
import random

import base64
import mimetypes
from functools import lru_cache

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')


# Utility to load and base64 encode local image files once and cache
@lru_cache(maxsize=None)
def load_image_b64(rel_path: str) -> str:
    try:
        abs_path = (ROOT_DIR / rel_path).resolve()
        mime, _ = mimetypes.guess_type(abs_path)
        if not mime:
            mime = 'image/jpeg'
        with open(abs_path, 'rb') as f:
            data = f.read()
        b64 = base64.b64encode(data).decode('utf-8')
        return f"data:{mime};base64,{b64}"
    except Exception as e:
        logging.warning(f"Failed to load image {rel_path}: {e}")
        return ""

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# Create the main app without a prefix
app = FastAPI()

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")

# Tarot Card Data Models
class TarotCard(BaseModel):
    id: int
    name: str
    image_url: str
    keywords: List[str]
    meaning_upright: str
    meaning_reversed: str
    description: str
    symbolism: str
    yes_no_meaning: str
    image_base64: Optional[str] = None

class ReadingType(BaseModel):
    id: str
    name: str
    description: str
    card_count: int
    positions: List[str]

class TarotReading(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    reading_type: str
    cards: List[Dict[str, Any]]
    interpretation: str
    mode: str = Field(default="rule")  # 'ai' | 'rule' | 'fallback'
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class QuizQuestion(BaseModel):
    id: int
    question: str
    options: List[str]
    correct_answer: int
    difficulty: str  # "beginner", "intermediate", "advanced"
    card_id: int
    explanation: str

# Major Arcana Data - Türkçe ve İngilizce
# Note: Images are returned as base64 Data URIs only from the detail endpoint to keep list payloads small.
MAJOR_ARCANA = [
    {
        "id": 0,
        "name": "The Fool",
        "name_tr": "Deli",
        "image_url": "https://customer-assets.emergentagent.com/job_destiny-tarot-2/artifacts/3hmi66rp_deli.jpg",
        "keywords": ["new beginnings", "innocence", "spontaneity", "free spirit"],
        "keywords_tr": ["yeni başlangıçlar", "saflık", "spontanlık", "özgür ruh"],
        "meaning_upright": "New beginnings, innocence, spontaneity, a free spirit, adventure, idealism, inexperience.",
        "meaning_upright_tr": "Yeni başlangıçlar, saflık, spontanlık, özgür ruh, macera, idealizm, deneyimsizlik.",
        "meaning_reversed": "Foolishness, recklessness, being taken advantage of, ignorance, poor judgment, lack of direction.",
        "meaning_reversed_tr": "Aptallık, dikkatsizlik, kandırılmak, cehalet, kötü yargı, yön eksikliği.",
        "description": "The Fool represents new beginnings, having faith in the future, being inexperienced, not knowing what to expect, having beginner's luck, improvisation and believing in the universe.",
        "description_tr": "Deli, yeni başlangıçları, geleceğe olan inancı, deneyimsiz olmayı, ne bekleyeceğini bilmemeyi, yeni başlayanların şansını, doğaçlamayı ve evrene inanmayı temsil eder.",
        "symbolism": "The Fool carries a small bag, representing what he needs for his journey. The white rose represents purity, the cliff represents the unknown, and the small dog represents loyalty and protection.",
        "symbolism_tr": "Deli küçük bir çanta taşır, bu yolculuğu için neye ihtiyacı olduğunu temsil eder. Beyaz gül saflığı, uçurum bilinmezliği, küçük köpek sadakati ve korumayı temsil eder.",
        "yes_no_meaning": "Yes - new opportunities and fresh starts await.",
        "yes_no_meaning_tr": "Evet - yeni fırsatlar ve yeni başlangıçlar sizi bekliyor."
    },
    {
        "id": 1,
        "name": "The Magician",
        "name_tr": "Büyücü",
        "image_url": "/assets/cards/magician.jpg",
        "keywords": ["manifestation", "resourcefulness", "power", "inspired action"],
        "keywords_tr": ["tezahür", "beceri", "güç", "ilhamlı eylem"],
        "meaning_upright": "Manifestation, resourcefulness, power, inspired action, determination, skill, ability, concentration.",
        "meaning_upright_tr": "Tezahür, beceri, güç, ilhamlı eylem, kararlılık, yetenek, yetki, konsantrasyon.",
        "meaning_reversed": "Manipulation, poor planning, untapped talents, deception, lack of energy, weak willpower.",
        "meaning_reversed_tr": "Manipülasyon, kötü planlama, kullanılmayan yetenekler, aldatma, enerji eksikliği, zayıf irade.",
        "description": "The Magician represents manifestation, resourcefulness, power, and inspired action. He has the ability to turn ideas into reality.",
        "description_tr": "Büyücü tezahürü, beceriyi, gücü ve ilhamlı eylemi temsil eder. Fikirleri gerçeğe dönüştürme yetisine sahiptir.",
        "symbolism": "The infinity symbol above his head represents unlimited potential. The tools on the table represent the four elements and suits of the tarot.",
        "symbolism_tr": "Başının üstündeki sonsuzluk sembolü sınırsız potansiyeli temsil eder. Masadaki aletler dört elementi ve tarot renklerini temsil eder.",
        "yes_no_meaning": "Yes - you have the power to make it happen.",
        "yes_no_meaning_tr": "Evet - bunu gerçekleştirme gücüne sahipsiniz."
    },
    {
        "id": 2,
        "name": "The High Priestess",
        "name_tr": "Yüksek Rahibe",
        "image_url": "/assets/cards/high_priestess.jpg",
        "keywords": ["intuition", "sacred knowledge", "divine feminine", "subconscious mind"],
        "keywords_tr": ["sezgi", "kutsal bilgi", "ilahi dişilik", "bilinçaltı"],
        "meaning_upright": "Intuition, sacred knowledge, divine feminine, the subconscious mind, higher power, inner voice.",
        "meaning_upright_tr": "Sezgi, kutsal bilgi, ilahi dişilik, bilinçaltı, yüksek güç, iç ses.",
        "meaning_reversed": "Secrets, disconnected from intuition, withdrawal, silence, repressed feelings, blocked psychic powers.",
        "meaning_reversed_tr": "Sırlar, sezgiden kopukluk, içe kapanma, sessizlik, bastırılmış duygular, engellenmiş psişik güçler.",
        "description": "The High Priestess represents intuition, sacred knowledge, and the divine feminine. She is a guardian of the subconscious mind and higher wisdom.",
        "description_tr": "Yüksek Rahibe sezgiyi, kutsal bilgiyi ve ilahi dişiliği temsil eder. Bilinçaltının ve yüksek bilgeliğin koruyucusudur.",
        "symbolism": "She sits between two pillars representing the conscious and subconscious minds. The veil behind her conceals deeper mysteries.",
        "symbolism_tr": "Bilinçli ve bilinçsiz aklı temsil eden iki sütun arasında oturur. Arkasındaki perde daha derin gizemleri gizler.",
        "yes_no_meaning": "Maybe - trust your intuition to guide you.",
        "yes_no_meaning_tr": "Belki - sizi yönlendirmesi için sezginize güvenin."
    },
    {
        "id": 3,
        "name": "The Empress",
        "name_tr": "İmparatoriçe",
        "image_url": "/assets/cards/empress.jpg",
        "keywords": ["femininity", "beauty", "nature", "nurturing", "abundance"],
        "keywords_tr": ["kadınlık", "güzellik", "doğa", "besleyicilik", "bolluk"],
        "meaning_upright": "Femininity, beauty, nature, nurturing, abundance, creativity, fertility, motherhood, sensuality.",
        "meaning_upright_tr": "Kadınlık, güzellik, doğa, besleyicilik, bolluk, yaratıcılık, doğurganlık, annelik, duyusallık.",
        "meaning_reversed": "Creative block, dependence on others, smothering, emptiness, nosiness, lack of growth.",
        "meaning_reversed_tr": "Yaratıcı blok, başkalarına bağımlılık, boğuculuk, boşluk, meraklılık, büyüme eksikliği.",
        "description": "The Empress represents femininity, beauty, nature, and abundance. She is the mother figure of the tarot, representing fertility and creativity.",
        "description_tr": "İmparatoriçe kadınlığı, güzelliği, doğayı ve bolluğu temsil eder. Tarot'un anne figürüdür, doğurganlığı ve yaratıcılığı temsil eder.",
        "symbolism": "She is surrounded by nature, representing her connection to the Earth. The crown of stars represents her divine connection.",
        "symbolism_tr": "Doğa ile çevrilidir, Dünya ile bağlantısını temsil eder. Yıldız tacı ilahi bağlantısını temsil eder.",
        "yes_no_meaning": "Yes - abundance and growth are coming.",
        "yes_no_meaning_tr": "Evet - bolluk ve büyüme geliyor."
    },
    {
        "id": 4,
        "name": "The Emperor",
        "name_tr": "İmparator",
        "image_url": "/assets/cards/emperor.jpg",
        "keywords": ["authority", "establishment", "structure", "father figure"],
        "keywords_tr": ["otorite", "kuruluş", "yapı", "baba figürü"],
        "meaning_upright": "Authority, establishment, structure, a father figure, leadership, logic, stability, security, control.",
        "meaning_upright_tr": "Otorite, kuruluş, yapı, baba figürü, liderlik, mantık, istikrar, güvenlik, kontrol.",
        "meaning_reversed": "Tyrant, domineering, rigid, stubborn, lack of discipline, recklessness, abusive power.",
        "meaning_reversed_tr": "Tiran, baskıcı, katı, inatçı, disiplin eksikliği, dikkatsizlik, kötüye kullanılan güç.",
        "description": "The Emperor represents authority, establishment, and structure. He is the father figure of the tarot, representing leadership and control.",
        "description_tr": "İmparator otoriteyi, kuruluşu ve yapıyı temsil eder. Tarot'un baba figürüdür, liderliği ve kontrolü temsil eder.",
        "symbolism": "He sits on a throne decorated with ram heads, representing his astrological association with Aries. The mountains behind him represent his solid foundation.",
        "symbolism_tr": "Koç başlarıyla süslenmiş bir taht üzerinde oturur, Koç burcuyla olan astrolojik bağlantısını temsil eder. Arkasındaki dağlar sağlam temelini temsil eder.",
        "yes_no_meaning": "Yes - take control and lead with authority.",
        "yes_no_meaning_tr": "Evet - kontrolü alın ve otoriteyle liderlik edin."
    },
    {
        "id": 5,
        "name": "The Hierophant",
        "name_tr": "Aziz",
        "image_url": "/assets/cards/hierophant.jpg",
        "keywords": ["spiritual wisdom", "religious beliefs", "conformity", "tradition"],
        "keywords_tr": ["ruhsal bilgelik", "dini inançlar", "uyum", "gelenek"],
        "meaning_upright": "Spiritual wisdom, religious beliefs, conformity, tradition, institutions, group identification, conventional wisdom.",
        "meaning_upright_tr": "Ruhsal bilgelik, dini inançlar, uyum, gelenek, kurumlar, grup kimliği, geleneksel bilgelik.",
        "meaning_reversed": "Personal beliefs, freedom, challenging the status quo, unconventional methods, ignorance, restriction.",
        "meaning_reversed_tr": "Kişisel inançlar, özgürlük, statükoyu sorgulama, alışılmamış yöntemler, cehalet, kısıtlama.",
        "description": "The Hierophant represents spiritual wisdom, religious beliefs, and tradition. He is a bridge between heaven and earth.",
        "description_tr": "Aziz ruhsal bilgeliği, dini inançları ve geleneği temsil eder. Cennet ile dünya arasında bir köprüdür.",
        "symbolism": "He holds keys representing the conscious and subconscious minds. Two acolytes kneel before him, representing the transmission of sacred knowledge.",
        "symbolism_tr": "Bilinçli ve bilinçsiz aklı temsil eden anahtarları tutar. İki yardımcı önünde diz çökmüş, kutsal bilginin aktarımını temsil eder.",
        "yes_no_meaning": "Yes - follow traditional wisdom and established methods.",
        "yes_no_meaning_tr": "Evet - geleneksel bilgeliği ve yerleşik yöntemleri takip edin."
    },
    {
        "id": 6,
        "name": "The Lovers",
        "name_tr": "Aşıklar",
        "image_url": "/assets/cards/lovers.jpg",
        "keywords": ["love", "harmony", "relationships", "values alignment"],
        "keywords_tr": ["aşk", "uyum", "ilişkiler", "değer uyumu"],
        "meaning_upright": "Love, harmony, relationships, values alignment, choices, partnerships, union, duality.",
        "meaning_upright_tr": "Aşk, uyum, ilişkiler, değer uyumu, seçimler, ortaklıklar, birlik, ikilik.",
        "meaning_reversed": "Disharmony, imbalance, misalignment of values, bad choices, indecision, inner conflicts.",
        "meaning_reversed_tr": "Uyumsuzluk, dengesizlik, değer uyumsuzluğu, kötü seçimler, kararsızlık, iç çelişkiler.",
        "description": "The Lovers represents love, harmony, and relationships. It's about making choices and finding balance between opposites.",
        "description_tr": "Aşıklar aşkı, uyumu ve ilişkileri temsil eder. Seçimler yapmak ve zıtlıklar arasında denge bulmakla ilgilidir.",
        "symbolism": "The angel above represents divine blessing on the union. The tree of knowledge and tree of life represent conscious and subconscious choices.",
        "symbolism_tr": "Yukarıdaki melek birliğe ilahi bereket temsil eder. Bilgi ağacı ve yaşam ağacı bilinçli ve bilinçsiz seçimleri temsil eder.",
        "yes_no_meaning": "Yes - especially for matters of the heart.",
        "yes_no_meaning_tr": "Evet - özellikle kalp işleri için."
    },
    {
        "id": 7,
        "name": "The Chariot",
        "name_tr": "Savaş Arabası",
        "image_url": "/assets/cards/chariot.jpg",
        "keywords": ["control", "willpower", "success", "determination"],
        "keywords_tr": ["kontrol", "irade gücü", "başarı", "kararlılık"],
        "meaning_upright": "Control, willpower, success, determination, hard control, self-discipline, focus, action.",
        "meaning_upright_tr": "Kontrol, irade gücü, başarı, kararlılık, sıkı kontrol, öz disiplin, odaklanma, eylem.",
        "meaning_reversed": "Lack of control, lack of direction, aggression, coercion, being driven by outside forces.",
        "meaning_reversed_tr": "Kontrol eksikliği, yön eksikliği, saldırganlık, zorlama, dış güçler tarafından yönlendirilmek.",
        "description": "The Chariot represents control, willpower, and success. It's about overcoming obstacles through determination and focus.",
        "description_tr": "Savaş Arabası kontrolü, irade gücünü ve başarıyı temsil eder. Kararlılık ve odaklanma yoluyla engelleri aşmakla ilgilidir.",
        "symbolism": "The two sphinxes represent opposing forces that must be controlled. The crown represents mastery and achievement.",
        "symbolism_tr": "İki sfenks kontrol edilmesi gereken karşıt güçleri temsil eder. Taç ustalığı ve başarıyı temsil eder.",
        "yes_no_meaning": "Yes - success through determination and focused effort.",
        "yes_no_meaning_tr": "Evet - kararlılık ve odaklı çaba yoluyla başarı."
    },
    {
        "id": 8,
        "name": "Strength",
        "name_tr": "Güç",
        "image_url": "/assets/cards/strength.jpg",
        "keywords": ["strength", "courage", "persuasion", "influence"],
        "keywords_tr": ["güç", "cesaret", "ikna", "etki"],
        "meaning_upright": "Strength, courage, persuasion, influence, compassion, self-control, gentle power, inner strength.",
        "meaning_upright_tr": "Güç, cesaret, ikna, etki, şefkat, öz kontrol, nazik güç, iç güç.",
        "meaning_reversed": "Self-doubt, weakness, insecurity, lack of self-discipline, low energy, raw emotion.",
        "meaning_reversed_tr": "Kendinden şüphe, zayıflık, güvensizlik, öz disiplin eksikliği, düşük enerji, ham duygu.",
        "description": "Strength represents inner strength, courage, and the power of gentleness. It's about taming the beast within through compassion.",
        "description_tr": "Güç iç gücü, cesareti ve nezaketin gücünü temsil eder. İçimizdeki canavarı şefkatle ehlileştirmekle ilgilidir.",
        "symbolism": "A woman gently closes a lion's mouth, representing the triumph of spiritual power over physical force. The infinity symbol represents unlimited potential.",
        "symbolism_tr": "Bir kadın aslanın ağzını nazikçe kapatır, ruhsal gücün fiziksel güç üzerindeki zaferini temsil eder. Sonsuzluk sembolü sınırsız potansiyeli temsil eder.",
        "yes_no_meaning": "Yes - you have the inner strength to overcome challenges.",
        "yes_no_meaning_tr": "Evet - zorlukları aşmak için iç gücünüz var."
    },
    {
        "id": 9,
        "name": "The Hermit",
        "name_tr": "Ermiş",
        "image_url": "/assets/cards/hermit.jpg",
        "keywords": ["soul searching", "seeking truth", "inner guidance"],
        "keywords_tr": ["ruh arayışı", "gerçek arayışı", "iç rehberlik"],
        "meaning_upright": "Soul searching, seeking truth, inner guidance, looking inward, spiritual journey, meditation, self-reflection.",
        "meaning_upright_tr": "Ruh arayışı, gerçek arayışı, iç rehberlik, içe bakış, ruhsal yolculuk, meditasyon, kendini yansıtma.",
        "meaning_reversed": "Isolation, loneliness, withdrawal, seeking false truths, misguided advice, rejection of wisdom.",
        "meaning_reversed_tr": "İzolasyon, yalnızlık, içe kapanma, yanlış gerçekler arayışı, yanlış yönlendirilmiş tavsiye, bilgeliği reddetme.",
        "description": "The Hermit represents soul searching and seeking truth. It's about looking inward for answers and spiritual guidance.",
        "description_tr": "Ermiş ruh arayışını ve gerçek arayışını temsil eder. Cevaplar ve ruhsal rehberlik için içe bakmakla ilgilidir.",
        "symbolism": "The lantern contains a six-pointed star, representing wisdom. The staff represents authority and the rocky path represents the difficult journey of self-discovery.",
        "symbolism_tr": "Fener altı köşeli yıldız içerir, bilgeliği temsil eder. Asa otoriteyi, kayalık yol ise kendini keşfetmenin zor yolculuğunu temsil eder.",
        "yes_no_meaning": "Maybe - look within for the answer.",
        "yes_no_meaning_tr": "Belki - cevap için içinize bakın."
    },
    {
        "id": 10,
        "name": "Wheel of Fortune",
        "name_tr": "Kader Çarkı",
        "image_url": "/assets/cards/wheel_of_fortune.jpg",
        "keywords": ["good luck", "karma", "life cycles", "destiny"],
        "keywords_tr": ["iyi şans", "karma", "yaşam döngüleri", "kader"],
        "meaning_upright": "Good luck, karma, life cycles, destiny, turning point, fate, fortune, unexpected events.",
        "meaning_upright_tr": "İyi şans, karma, yaşam döngüleri, kader, dönüm noktası, talih, servet, beklenmedik olaylar.",
        "meaning_reversed": "Bad luck, lack of control, clinging to control, unwillingness to change, breaking cycles.",
        "meaning_reversed_tr": "Kötü şans, kontrol eksikliği, kontrole sarılma, değişim konusunda isteksizlik, döngüleri kırma.",
        "description": "The Wheel of Fortune represents good luck, karma, and life cycles. It's about the ever-changing nature of life and destiny.",
        "description_tr": "Kader Çarkı iyi şansı, karmayı ve yaşam döngülerini temsil eder. Yaşamın ve kaderin sürekli değişen doğasıyla ilgilidir.",
        "symbolism": "The wheel represents the cyclical nature of life. The creatures in the corners represent the four fixed signs of the zodiac.",
        "symbolism_tr": "Çark yaşamın döngüsel doğasını temsil eder. Köşelerdeki yaratıklar zodiak'ın dört sabit burcunu temsil eder.",
        "yes_no_meaning": "Yes - fortune is turning in your favor.",
        "yes_no_meaning_tr": "Evet - kader sizin lehinize dönüyor."
    },
    {
        "id": 11,
        "name": "Justice",
        "name_tr": "Adalet",
        "image_url": "/assets/cards/justice.jpg",
        "keywords": ["justice", "fairness", "truth", "cause and effect"],
        "keywords_tr": ["adalet", "hakkaniyet", "gerçek", "neden ve sonuç"],
        "meaning_upright": "Justice, fairness, truth, cause and effect, law, legal matters, balanced decisions, integrity.",
        "meaning_upright_tr": "Adalet, hakkaniyet, gerçek, neden ve sonuç, hukuk, yasal konular, dengeli kararlar, dürüstlük.",
        "meaning_reversed": "Unfairness, lack of accountability, dishonesty, bias, avoiding responsibility, harsh judgment.",
        "meaning_reversed_tr": "Haksızlık, hesap verebilirlik eksikliği, dürüstsüzlük, önyargı, sorumluluktan kaçınma, sert yargı.",
        "description": "Justice represents fairness, truth, and cause and effect. It's about making balanced decisions and taking responsibility for actions.",
        "description_tr": "Adalet hakkaniyeti, gerçeği ve neden-sonuç ilişkisini temsil eder. Dengeli kararlar verme ve eylemlerimizin sorumluluğunu almakla ilgilidir.",
        "symbolism": "The scales represent balance and fairness. The sword represents the power of reason and justice. The pillars represent the balance between opposing forces.",
        "symbolism_tr": "Terazi dengeyi ve hakkaniyeti temsil eder. Kılıç aklın ve adaletin gücünü temsil eder. Sütunlar karşıt güçler arasındaki dengeyi temsil eder.",
        "yes_no_meaning": "Yes - if your cause is just and fair.",
        "yes_no_meaning_tr": "Evet - eğer davanız adil ve haklıysa."
    },
    {
        "id": 12,
        "name": "The Hanged Man",
        "name_tr": "Asılan Adam",
        "image_url": "/assets/cards/hanged_man.jpg",
        "keywords": ["suspension", "restriction", "letting go", "sacrifice"],
        "keywords_tr": ["askıya alma", "kısıtlama", "bırakma", "fedakarlık"],
        "meaning_upright": "Suspension, restriction, letting go, sacrifice, prophetic powers, divination, intuition, martyrdom.",
        "meaning_upright_tr": "Askıya alma, kısıtlama, bırakma, fedakarlık, peygamberlik güçleri, kehanet, sezgi, şehitlik.",
        "meaning_reversed": "Delays, resistance, stalling, indecision, lack of sacrifice, unwillingness to make necessary changes.",
        "meaning_reversed_tr": "Gecikmeler, direniş, oyalama, kararsızlık, fedakarlık eksikliği, gerekli değişiklikleri yapmada isteksizlik.",
        "description": "The Hanged Man represents suspension and letting go. It's about sacrifice and gaining new perspectives through surrender.",
        "description_tr": "Asılan Adam askıya almayı ve bırakmayı temsil eder. Fedakarlık ve teslim olma yoluyla yeni perspektifler kazanmakla ilgilidir.",
        "symbolism": "Hanging upside down by one foot, he sees the world from a new perspective. The halo represents spiritual enlightenment gained through sacrifice.",
        "symbolism_tr": "Bir ayağından baş aşağı asılı durumda, dünyayı yeni bir perspektiften görür. Hale fedakarlık yoluyla kazanılan ruhsal aydınlanmayı temsil eder.",
        "yes_no_meaning": "No - wait and reassess the situation.",
        "yes_no_meaning_tr": "Hayır - bekleyin ve durumu yeniden değerlendirin."
    },
    {
        "id": 13,
        "name": "Death",
        "name_tr": "Ölüm",
        "image_url": "/assets/cards/death.jpg",
        "keywords": ["endings", "beginnings", "change", "transformation"],
        "keywords_tr": ["sonlar", "başlangıçlar", "değişim", "dönüşüm"],
        "meaning_upright": "Endings, beginnings, change, transformation, transition, letting go, release, rebirth.",
        "meaning_upright_tr": "Sonlar, başlangıçlar, değişim, dönüşüm, geçiş, bırakma, serbest bırakma, yeniden doğuş.",
        "meaning_reversed": "Resistance to change, personal transformation, inner purging, stagnation, decay, holding on.",
        "meaning_reversed_tr": "Değişime direnç, kişisel dönüşüm, iç temizlik, durgunluk, çürüme, tutunma.",
        "description": "Death represents endings and beginnings. It's about transformation and the natural cycle of death and rebirth.",
        "description_tr": "Ölüm sonları ve başlangıçları temsil eder. Dönüşüm ve ölüm-yeniden doğuşun doğal döngüsüyle ilgilidir.",
        "symbolism": "The skeleton represents what remains after everything else has been stripped away. The rising sun represents new beginnings after endings.",
        "symbolism_tr": "İskelet diğer her şey soyunduktan sonra kalanı temsil eder. Doğan güneş sonlardan sonra yeni başlangıçları temsil eder.",
        "yes_no_meaning": "No - but necessary change is coming.",
        "yes_no_meaning_tr": "Hayır - ama gerekli değişim geliyor."
    },
    {
        "id": 14,
        "name": "Temperance",
        "name_tr": "Denge",
        "image_url": "/assets/cards/temperance.jpg",
        "keywords": ["balance", "moderation", "patience", "purpose"],
        "keywords_tr": ["denge", "ölçülülük", "sabır", "amaç"],
        "meaning_upright": "Balance, moderation, patience, purpose, meaning, connecting with your guide, slow and steady progress.",
        "meaning_upright_tr": "Denge, ölçülülük, sabır, amaç, anlam, rehberinizle bağlantı kurma, yavaş ve istikrarlı ilerleme.",
        "meaning_reversed": "Imbalance, excess, self-healing, re-alignment, hasty decisions, lack of long-term vision.",
        "meaning_reversed_tr": "Dengesizlik, aşırılık, kendini iyileştirme, yeniden hizalama, aceleci kararlar, uzun vadeli vizyon eksikliği.",
        "description": "Temperance represents balance, moderation, and patience. It's about finding the middle path and connecting with your higher purpose.",
        "description_tr": "Denge dengeyi, ölçülülüğü ve sabrı temsil eder. Orta yolu bulma ve yüksek amacınızla bağlantı kurmakla ilgilidir.",
        "symbolism": "The angel pours water between two cups, representing the flow of life and the mixing of opposites. One foot on land and one in water represents balance.",
        "symbolism_tr": "Melek iki bardak arasında su döker, yaşamın akışını ve zıtlıkların karışımını temsil eder. Bir ayak karada bir ayak suda dengeyi temsil eder.",
        "yes_no_meaning": "Yes - through patience and moderation.",
        "yes_no_meaning_tr": "Evet - sabır ve ölçülülük yoluyla."
    },
    {
        "id": 15,
        "name": "The Devil",
        "name_tr": "Şeytan",
        "image_url": "/assets/cards/devil.jpg",
        "keywords": ["bondage", "addiction", "sexuality", "materialism"],
        "keywords_tr": ["bağımlılık", "alışkanlık", "cinsellik", "materyalizm"],
        "meaning_upright": "Bondage, addiction, sexuality, materialism, playfulness, commitment, open relationships, temptation.",
        "meaning_upright_tr": "Bağımlılık, alışkanlık, cinsellik, materyalizm, oyunculuk, bağlılık, açık ilişkiler, ayartma.",
        "meaning_reversed": "Releasing limiting beliefs, exploring dark thoughts, detachment, breaking free, power reclaimed.",
        "meaning_reversed_tr": "Sınırlayıcı inançları bırakma, karanlık düşünceleri keşfetme, kopma, özgürleşme, gücü geri alma.",
        "description": "The Devil represents bondage and materialism. It's about being trapped by your own limiting beliefs and addictions.",
        "description_tr": "Şeytan bağımlılığı ve materyalizmi temsil eder. Kendi sınırlayıcı inançlarınız ve bağımlılıklarınız tarafından tuzağa düşmekle ilgilidir.",
        "symbolism": "The chained figures show that bondage is often self-imposed. The inverted pentagram represents the material world dominating the spiritual.",
        "symbolism_tr": "Zincirli figürler bağımlılığın genellikle kendi kendine dayatıldığını gösterir. Ters pentagram maddi dünyanın ruhsala hakim olmasını temsil eder.",
        "yes_no_meaning": "No - beware of temptation and false promises.",
        "yes_no_meaning_tr": "Hayır - ayartmaya ve yalan vaatlere dikkat edin."
    },
    {
        "id": 16,
        "name": "The Tower",
        "name_tr": "Kule",
        "image_url": "/assets/cards/tower.jpg",
        "keywords": ["sudden change", "upheaval", "chaos", "revelation"],
        "keywords_tr": ["ani değişim", "altüst olma", "kaos", "vahiy"],
        "meaning_upright": "Sudden change, upheaval, chaos, revelation, awakening, disaster, destruction of false beliefs.",
        "meaning_upright_tr": "Ani değişim, altüst olma, kaos, vahiy, uyanış, felaket, yanlış inançların yıkımı.",
        "meaning_reversed": "Personal transformation, fear of change, averting disaster, resistance to change, delayed upheaval.",
        "meaning_reversed_tr": "Kişisel dönüşüm, değişim korkusu, felaketi önleme, değişime direnç, gecikmiş altüst olma.",
        "description": "The Tower represents sudden change and upheaval. It's about the destruction of false beliefs and structures.",
        "description_tr": "Kule ani değişimi ve altüst olmayı temsil eder. Yanlış inançların ve yapıların yıkımıyla ilgilidir.",
        "symbolism": "Lightning strikes the tower, representing sudden divine insight. Figures fall from the tower, representing the fall from grace and false security.",
        "symbolism_tr": "Şimşek kuleye çarpar, ani ilahi kavrayışı temsil eder. Figürler kuleden düşer, lütuftan düşüşü ve sahte güvenliği temsil eder.",
        "yes_no_meaning": "No - sudden upheaval is likely.",
        "yes_no_meaning_tr": "Hayır - ani altüst olma muhtemel."
    },
    {
        "id": 17,
        "name": "The Star",
        "name_tr": "Yıldız",
        "image_url": "/assets/cards/star.jpg",
        "keywords": ["hope", "faith", "purpose", "renewal"],
        "keywords_tr": ["umut", "inanç", "amaç", "yenilenme"],
        "meaning_upright": "Hope, faith, purpose, renewal, spirituality, healing, positivity, wish fulfillment, good health.",
        "meaning_upright_tr": "Umut, inanç, amaç, yenilenme, maneviyat, şifa, pozitiflik, dilek gerçekleşmesi, iyi sağlık.",
        "meaning_reversed": "Lack of faith, despair, self-trust, disconnection, missed opportunities, pessimism.",
        "meaning_reversed_tr": "İnanç eksikliği, umutsuzluk, kendine güven, bağlantı kopukluğu, kaçırılan fırsatlar, kötümserlik.",
        "description": "The Star represents hope, faith, and renewal. It's about spiritual healing and connection to your higher purpose.",
        "description_tr": "Yıldız umudu, inancı ve yenilenmeyi temsil eder. Ruhsal şifa ve yüksek amacınızla bağlantıyla ilgilidir.",
        "symbolism": "The woman pours water on land and in the pool, representing the conscious and subconscious minds. Seven small stars surround one large star representing chakras.",
        "symbolism_tr": "Kadın kara ve havuza su döker, bilinçli ve bilinçsiz aklı temsil eder. Yedi küçük yıldız bir büyük yıldızı çevreler, çakraları temsil eder.",
        "yes_no_meaning": "Yes - your wishes will be fulfilled.",
        "yes_no_meaning_tr": "Evet - dilekleriniz gerçekleşecek."
    },
    {
        "id": 18,
        "name": "The Moon",
        "name_tr": "Ay",
        "image_url": "/assets/cards/moon.jpg",
        "keywords": ["illusion", "fear", "anxiety", "subconscious"],
        "keywords_tr": ["illüzyon", "korku", "kaygı", "bilinçaltı"],
        "meaning_upright": "Illusion, fear, anxiety, subconscious, intuition, dreams, deception, confusion, insecurity.",
        "meaning_upright_tr": "İllüzyon, korku, kaygı, bilinçaltı, sezgi, rüyalar, aldatma, karmaşa, güvensizlik.",
        "meaning_reversed": "Release of fear, repressed emotion, inner confusion, self-deception, unveiling secrets.",
        "meaning_reversed_tr": "Korkudan kurtulma, bastırılmış duygu, iç karmaşa, kendini aldatma, sırları açığa çıkarma.",
        "description": "The Moon represents illusion, fear, and the subconscious mind. It's about navigating through confusion and trusting your intuition.",
        "description_tr": "Ay illüzyonu, korkuyu ve bilinçaltını temsil eder. Karmaşanın içinde yol bulma ve sezginize güvenmekle ilgilidir.",
        "symbolism": "Two towers represent the pillars of consciousness. The path between them leads to the unknown. The moon's face shows it's watching over the journey.",
        "symbolism_tr": "İki kule bilincin sütunlarını temsil eder. Aralarındaki yol bilinmezliğe götürür. Ayın yüzü yolculuğu izlediğini gösterir.",
        "yes_no_meaning": "No - things are not as they seem.",
        "yes_no_meaning_tr": "Hayır - işler göründüğü gibi değil."
    },
    {
        "id": 19,
        "name": "The Sun",
        "name_tr": "Güneş",
        "image_url": "/assets/cards/sun.jpg",
        "keywords": ["positivity", "fun", "warmth", "success"],
        "keywords_tr": ["pozitiflik", "eğlence", "sıcaklık", "başarı"],
        "meaning_upright": "Positivity, fun, warmth, success, vitality, joy, confidence, happiness, truth, optimism.",
        "meaning_upright_tr": "Pozitiflik, eğlence, sıcaklık, başarı, canlılık, neşe, güven, mutluluk, gerçek, iyimserlik.",
        "meaning_reversed": "Inner child, feeling down, overly optimistic, conceit, lack of success, pessimism, unrealistic expectations.",
        "meaning_reversed_tr": "İç çocuk, moralinin bozuk olması, aşırı iyimserlik, kibir, başarı eksikliği, kötümserlik, gerçekçi olmayan beklentiler.",
        "description": "The Sun represents positivity, success, and vitality. It's about joy, confidence, and the triumph of consciousness.",
        "description_tr": "Güneş pozitifliği, başarıyı ve canlılığı temsil eder. Neşe, güven ve bilincin zaferiyle ilgilidir.",
        "symbolism": "The child represents innocence and joy. The white horse represents purity and success. The sunflowers represent life and fertility.",
        "symbolism_tr": "Çocuk masumiyeti ve neşeyi temsil eder. Beyaz at saflığı ve başarıyı temsil eder. Ayçiçekleri yaşamı ve doğurganlığı temsil eder.",
        "yes_no_meaning": "Yes - success and happiness are assured.",
        "yes_no_meaning_tr": "Evet - başarı ve mutluluk garanti."
    },
    {
        "id": 20,
        "name": "Judgement",
        "name_tr": "Yargı",
        "image_url": "/assets/cards/judgement.jpg",
        "keywords": ["judgement", "rebirth", "inner calling", "absolution"],
        "keywords_tr": ["yargı", "yeniden doğuş", "iç çağrı", "bağışlanma"],
        "meaning_upright": "Judgement, rebirth, inner calling, absolution, higher purpose, spiritual awakening, redemption, evaluation.",
        "meaning_upright_tr": "Yargı, yeniden doğuş, iç çağrı, bağışlanma, yüksek amaç, ruhsal uyanış, kurtuluş, değerlendirme.",
        "meaning_reversed": "Self-doubt, harsh self-judgment, lack of self-awareness, missing the call, severe self-criticism.",
        "meaning_reversed_tr": "Kendinden şüphe, sert kendini yargılama, öz farkındalık eksikliği, çağrıyı kaçırma, şiddetli kendini eleştirme.",
        "description": "Judgement represents rebirth and inner calling. It's about spiritual awakening and answering your higher purpose.",
        "description_tr": "Yargı yeniden doğuşu ve iç çağrıyı temsil eder. Ruhsal uyanış ve yüksek amacınıza cevap vermekle ilgilidir.",
        "symbolism": "The angel Gabriel blows a trumpet, calling souls to their higher purpose. People rise from their graves, representing spiritual rebirth.",
        "symbolism_tr": "Melek Gabriel boru çalar, ruhları yüksek amaçlarına çağırır. İnsanlar mezarlarından kalkar, ruhsal yeniden doğuşu temsil eder.",
        "yes_no_meaning": "Yes - if you heed your inner calling.",
        "yes_no_meaning_tr": "Evet - eğer iç çağrınıza kulak verirseniz."
    },
    {
        "id": 21,
        "name": "The World",
        "name_tr": "Dünya",
        "image_url": "/assets/cards/world.jpg",
        "keywords": ["completion", "accomplishment", "travel", "success"],
        "keywords_tr": ["tamamlanma", "başarım", "seyahat", "başarı"],
        "meaning_upright": "Completion, accomplishment, travel, success, fulfillment, sense of belonging, wholeness.",
        "meaning_upright_tr": "Tamamlanma, başarım, seyahat, başarı, tatmin, aidiyet duygusu, bütünlük.",
        "meaning_reversed": "Incomplete goals, lack of closure, stagnation, failed plans, disappointment, seeking shortcuts.",
        "meaning_reversed_tr": "Tamamlanmamış hedefler, kapanış eksikliği, durgunluk, başarısız planlar, hayal kırıklığı, kestirme yol arayışı.",
        "description": "The World represents completion and accomplishment. It's about achieving your goals and reaching a state of wholeness.",
        "description_tr": "Dünya tamamlanmayı ve başarımı temsil eder. Hedeflerinize ulaşma ve bütünlük durumuna erişmekle ilgilidir.",
        "symbolism": "The dancing figure represents the completion of the journey. The wreath represents victory and success. The four creatures represent the four elements in harmony.",
        "symbolism_tr": "Dans eden figür yolculuğun tamamlanmasını temsil eder. Çelenk zaferi ve başarıyı temsil eder. Dört yaratık uyum içindeki dört elementi temsil eder.",
        "yes_no_meaning": "Yes - completion and success are within reach.",
        "yes_no_meaning_tr": "Evet - tamamlanma ve başarı erişilebilir mesafede."
    },
    {
        "id": 6,
        "name": "The Lovers",
        "image_url": "/assets/cards/lovers.jpg",
        "keywords": ["love", "harmony", "relationships", "values alignment"],
        "meaning_upright": "Love, harmony, relationships, values alignment, choices, partnerships, union, duality.",
        "meaning_reversed": "Disharmony, imbalance, misalignment of values, bad choices, indecision, inner conflicts.",
        "description": "The Lovers represents love, harmony, and relationships. It's about making choices and finding balance between opposites.",
        "symbolism": "The angel above represents divine blessing on the union. The tree of knowledge and tree of life represent conscious and subconscious choices.",
        "yes_no_meaning": "Yes - especially for matters of the heart."
    },
    {
        "id": 7,
        "name": "The Chariot",
        "image_url": "/assets/cards/chariot.jpg",
        "keywords": ["control", "willpower", "success", "determination"],
        "meaning_upright": "Control, willpower, success, determination, hard control, self-discipline, focus, action.",
        "meaning_reversed": "Lack of control, lack of direction, aggression, coercion, being driven by outside forces.",
        "description": "The Chariot represents control, willpower, and success. It's about overcoming obstacles through determination and focus.",
        "symbolism": "The two sphinxes represent opposing forces that must be controlled. The crown represents mastery and achievement.",
        "yes_no_meaning": "Yes - success through determination and focused effort."
    },
    {
        "id": 8,
        "name": "Strength",
        "image_url": "/assets/cards/strength.jpg",
        "keywords": ["strength", "courage", "persuasion", "influence"],
        "meaning_upright": "Strength, courage, persuasion, influence, compassion, self-control, gentle power, inner strength.",
        "meaning_reversed": "Self-doubt, weakness, insecurity, lack of self-discipline, low energy, raw emotion.",
        "description": "Strength represents inner strength, courage, and the power of gentleness. It's about taming the beast within through compassion.",
        "symbolism": "A woman gently closes a lion's mouth, representing the triumph of spiritual power over physical force. The infinity symbol represents unlimited potential.",
        "yes_no_meaning": "Yes - you have the inner strength to overcome challenges."
    },
    {
        "id": 9,
        "name": "The Hermit",
        "image_url": "/assets/cards/hermit.jpg",
        "keywords": ["soul searching", "seeking truth", "inner guidance"],
        "meaning_upright": "Soul searching, seeking truth, inner guidance, looking inward, spiritual journey, meditation, self-reflection.",
        "meaning_reversed": "Isolation, loneliness, withdrawal, seeking false truths, misguided advice, rejection of wisdom.",
        "description": "The Hermit represents soul searching and seeking truth. It's about looking inward for answers and spiritual guidance.",
        "symbolism": "The lantern contains a six-pointed star, representing wisdom. The staff represents authority and the rocky path represents the difficult journey of self-discovery.",
        "yes_no_meaning": "Maybe - look within for the answer."
    },
    {
        "id": 10,
        "name": "Wheel of Fortune",
        "image_url": "/assets/cards/wheel_of_fortune.jpg",
        "keywords": ["good luck", "karma", "life cycles", "destiny"],
        "meaning_upright": "Good luck, karma, life cycles, destiny, turning point, fate, fortune, unexpected events.",
        "meaning_reversed": "Bad luck, lack of control, clinging to control, unwillingness to change, breaking cycles.",
        "description": "The Wheel of Fortune represents good luck, karma, and life cycles. It's about the ever-changing nature of life and destiny.",
        "symbolism": "The wheel represents the cyclical nature of life. The creatures in the corners represent the four fixed signs of the zodiac.",
        "yes_no_meaning": "Yes - fortune is turning in your favor."
    },
    {
        "id": 11,
        "name": "Justice",
        "image_url": "/assets/cards/justice.jpg",
        "keywords": ["justice", "fairness", "truth", "cause and effect"],
        "meaning_upright": "Justice, fairness, truth, cause and effect, law, legal matters, balanced decisions, integrity.",
        "meaning_reversed": "Unfairness, lack of accountability, dishonesty, bias, avoiding responsibility, harsh judgment.",
        "description": "Justice represents fairness, truth, and cause and effect. It's about making balanced decisions and taking responsibility for actions.",
        "symbolism": "The scales represent balance and fairness. The sword represents the power of reason and justice. The pillars represent the balance between opposing forces.",
        "yes_no_meaning": "Yes - if your cause is just and fair."
    },
    {
        "id": 12,
        "name": "The Hanged Man",
        "image_url": "/assets/cards/hanged_man.jpg",
        "keywords": ["suspension", "restriction", "letting go", "sacrifice"],
        "meaning_upright": "Suspension, restriction, letting go, sacrifice, prophetic powers, divination, intuition, martyrdom.",
        "meaning_reversed": "Delays, resistance, stalling, indecision, lack of sacrifice, unwillingness to make necessary changes.",
        "description": "The Hanged Man represents suspension and letting go. It's about sacrifice and gaining new perspectives through surrender.",
        "symbolism": "Hanging upside down by one foot, he sees the world from a new perspective. The halo represents spiritual enlightenment gained through sacrifice.",
        "yes_no_meaning": "No - wait and reassess the situation."
    },
    {
        "id": 13,
        "name": "Death",
        "image_url": "/assets/cards/death.jpg",
        "keywords": ["endings", "beginnings", "change", "transformation"],
        "meaning_upright": "Endings, beginnings, change, transformation, transition, letting go, release, rebirth.",
        "meaning_reversed": "Resistance to change, personal transformation, inner purging, stagnation, decay, holding on.",
        "description": "Death represents endings and beginnings. It's about transformation and the natural cycle of death and rebirth.",
        "symbolism": "The skeleton represents what remains after everything else has been stripped away. The rising sun represents new beginnings after endings.",
        "yes_no_meaning": "No - but necessary change is coming."
    },
    {
        "id": 14,
        "name": "Temperance",
        "image_url": "/assets/cards/temperance.jpg",
        "keywords": ["balance", "moderation", "patience", "purpose"],
        "meaning_upright": "Balance, moderation, patience, purpose, meaning, connecting with your guide, slow and steady progress.",
        "meaning_reversed": "Imbalance, excess, self-healing, re-alignment, hasty decisions, lack of long-term vision.",
        "description": "Temperance represents balance, moderation, and patience. It's about finding the middle path and connecting with your higher purpose.",
        "symbolism": "The angel pours water between two cups, representing the flow of life and the mixing of opposites. One foot on land and one in water represents balance.",
        "yes_no_meaning": "Yes - through patience and moderation."
    },
    {
        "id": 15,
        "name": "The Devil",
        "image_url": "/assets/cards/devil.jpg",
        "keywords": ["bondage", "addiction", "sexuality", "materialism"],
        "meaning_upright": "Bondage, addiction, sexuality, materialism, playfulness, commitment, open relationships, temptation.",
        "meaning_reversed": "Releasing limiting beliefs, exploring dark thoughts, detachment, breaking free, power reclaimed.",
        "description": "The Devil represents bondage and materialism. It's about being trapped by your own limiting beliefs and addictions.",
        "symbolism": "The chained figures show that bondage is often self-imposed. The inverted pentagram represents the material world dominating the spiritual.",
        "yes_no_meaning": "No - beware of temptation and false promises."
    },
    {
        "id": 16,
        "name": "The Tower",
        "image_url": "/assets/cards/tower.jpg",
        "keywords": ["sudden change", "upheaval", "chaos", "revelation"],
        "meaning_upright": "Sudden change, upheaval, chaos, revelation, awakening, disaster, destruction of false beliefs.",
        "meaning_reversed": "Personal transformation, fear of change, averting disaster, resistance to change, delayed upheaval.",
        "description": "The Tower represents sudden change and upheaval. It's about the destruction of false beliefs and structures.",
        "symbolism": "Lightning strikes the tower, representing sudden divine insight. Figures fall from the tower, representing the fall from grace and false security.",
        "yes_no_meaning": "No - sudden upheaval is likely."
    },
    {
        "id": 17,
        "name": "The Star",
        "image_url": "/assets/cards/star.jpg",
        "keywords": ["hope", "faith", "purpose", "renewal"],
        "meaning_upright": "Hope, faith, purpose, renewal, spirituality, healing, positivity, wish fulfillment, good health.",
        "meaning_reversed": "Lack of faith, despair, self-trust, disconnection, missed opportunities, pessimism.",
        "description": "The Star represents hope, faith, and renewal. It's about spiritual healing and connection to your higher purpose.",
        "symbolism": "The woman pours water on land and in the pool, representing the conscious and subconscious minds. Seven small stars surround one large star representing chakras.",
        "yes_no_meaning": "Yes - your wishes will be fulfilled."
    },
    {
        "id": 18,
        "name": "The Moon",
        "image_url": "/assets/cards/moon.jpg",
        "keywords": ["illusion", "fear", "anxiety", "subconscious"],
        "meaning_upright": "Illusion, fear, anxiety, subconscious, intuition, dreams, deception, confusion, insecurity.",
        "meaning_reversed": "Release of fear, repressed emotion, inner confusion, self-deception, unveiling secrets.",
        "description": "The Moon represents illusion, fear, and the subconscious mind. It's about navigating through confusion and trusting your intuition.",
        "symbolism": "Two towers represent the pillars of consciousness. The path between them leads to the unknown. The moon's face shows it's watching over the journey.",
        "yes_no_meaning": "No - things are not as they seem."
    },
    {
        "id": 19,
        "name": "The Sun",
        "image_url": "/assets/cards/sun.jpg",
        "keywords": ["positivity", "fun", "warmth", "success"],
        "meaning_upright": "Positivity, fun, warmth, success, vitality, joy, confidence, happiness, truth, optimism.",
        "meaning_reversed": "Inner child, feeling down, overly optimistic, conceit, lack of success, pessimism, unrealistic expectations.",
        "description": "The Sun represents positivity, success, and vitality. It's about joy, confidence, and the triumph of consciousness.",
        "symbolism": "The child represents innocence and joy. The white horse represents purity and success. The sunflowers represent life and fertility.",
        "yes_no_meaning": "Yes - success and happiness are assured."
    },
    {
        "id": 20,
        "name": "Judgement",
        "image_url": "/assets/cards/judgement.jpg",
        "keywords": ["judgement", "rebirth", "inner calling", "absolution"],
        "meaning_upright": "Judgement, rebirth, inner calling, absolution, higher purpose, spiritual awakening, redemption, evaluation.",
        "meaning_reversed": "Self-doubt, harsh self-judgment, lack of self-awareness, missing the call, severe self-criticism.",
        "description": "Judgement represents rebirth and inner calling. It's about spiritual awakening and answering your higher purpose.",
        "symbolism": "The angel Gabriel blows a trumpet, calling souls to their higher purpose. People rise from their graves, representing spiritual rebirth.",
        "yes_no_meaning": "Yes - if you heed your inner calling."
    },
    {
        "id": 21,
        "name": "The World",
        "image_url": "/assets/cards/world.jpg",
        "keywords": ["completion", "accomplishment", "travel", "success"],
        "meaning_upright": "Completion, accomplishment, travel, success, fulfillment, sense of belonging, wholeness.",
        "meaning_reversed": "Incomplete goals, lack of closure, stagnation, failed plans, disappointment, seeking shortcuts.",
        "description": "The World represents completion and accomplishment. It's about achieving your goals and reaching a state of wholeness.",
        "symbolism": "The dancing figure represents the completion of the journey. The wreath represents victory and success. The four creatures represent the four elements in harmony.",
        "yes_no_meaning": "Yes - completion and success are within reach."
    }
]

# Deduplicate to exactly 22 unique cards by id
@lru_cache(maxsize=None)
def get_unique_major_arcana() -> List[Dict[str, Any]]:
    seen: Dict[int, Dict[str, Any]] = {}
    for c in MAJOR_ARCANA:
        cid = c.get('id')
        if cid is not None and cid not in seen:
            seen[cid] = c
    # return ordered by id
    return [seen[i] for i in sorted(seen.keys())]

# Map of ID -> local image path. We will send base64 only from detail endpoint
IMAGES_BY_ID: Dict[int, str] = {
    0: 'card_images/joker-karti.jpg',
    1: 'card_images/buyucu-karti.jpg',
    2: 'card_images/azize-karti.jpg',
    3: 'card_images/imparatorice-karti.jpg',
    4: 'card_images/imparator-karti.jpg',
    5: 'card_images/aziz-karti.jpg',
    6: 'card_images/asiklar-karti.jpg',
    7: 'card_images/araba-karti.jpg',
    8: 'card_images/guc-karti.jpg',
    9: 'card_images/ermis-karti.jpg',
    10: 'card_images/kader-carki-karti.jpg',
    11: 'card_images/adalet-karti.jpg',
    12: 'card_images/asilan-adam-karti.jpg',
    13: 'card_images/olum-karti.jpg',
    14: 'card_images/denge-karti.jpg',
    15: 'card_images/seytan-karti.jpg',
    16: 'card_images/kule-karti.jpg',
    17: 'card_images/yildiz-karti.jpg',
    18: 'card_images/ay-karti.jpg',
    19: 'card_images/gunes-karti.jpg',
    20: 'card_images/mahkeme-karti.jpg',
    21: 'card_images/dunya-karti.jpg',
}


# Sync image_url fields in MAJOR_ARCANA with local filenames from IMAGES_BY_ID
for _card in MAJOR_ARCANA:
    cid = _card.get('id')
    local_path = IMAGES_BY_ID.get(cid)
    if local_path:
        _card['image_url'] = local_path


# Reading Types Configuration
READING_TYPES = [
    {
        "id": "card_of_day",
        "name": "Card of the Day",
        "description": "The simplest Tarot in which you choose the card that will mark your day.",
        "card_count": 1,
        "positions": ["Your Day"]
    },
    {
        "id": "classic_tarot",
        "name": "Classic Tarot",
        "description": "A three-card spread that will give you the forecast for today and also offer you some advice on health.",
        "card_count": 3,
        "positions": ["Past/Foundation", "Present/Current Situation", "Future/Outcome"]
    },
    {
        "id": "path_of_day",
        "name": "The Path of the Day",
        "description": "Four-card spread to guess work, money and love for today.",
        "card_count": 4,
        "positions": ["Work", "Money", "Love", "General Advice"]
    },
    {
        "id": "couples_tarot",
        "name": "The Tarot of the Couples",
        "description": "This love Tarot predicts the future of any couple and offers advice on how to improve their relationship.",
        "card_count": 5,
        "positions": ["Your Feelings", "Partner's Feelings", "Current Relationship", "Challenges", "Future Together"]
    },
    {
        "id": "yes_no",
        "name": "Yes or No",
        "description": "Ask the Tarot a question for a direct and reasoned answer.",
        "card_count": 1,
        "positions": ["Answer"]
    }
]

# API Endpoints
@api_router.get("/")
async def root():
    return {"message": "Tarot API is running"}

@api_router.get("/cards", response_model=List[TarotCard])
async def get_all_cards(language: str = "en"):
    """Get all Major Arcana cards with language support"""
    cards = []
    for card_data in get_unique_major_arcana():
        # ensure IMAGES_BY_ID path exists for detail endpoint usage
        if card_data.get('id') in IMAGES_BY_ID:
            card_data['image_local'] = IMAGES_BY_ID[card_data['id']]
        if language == "tr":
            # Return Turkish version
            card = {
                "id": card_data["id"],
                "name": card_data.get("name_tr", card_data["name"]),
                "image_url": card_data["image_url"],
                "keywords": card_data.get("keywords_tr", card_data["keywords"]),
                "meaning_upright": card_data.get("meaning_upright_tr", card_data["meaning_upright"]),
                "meaning_reversed": card_data.get("meaning_reversed_tr", card_data["meaning_reversed"]),
                "description": card_data.get("description_tr", card_data["description"]),
                "symbolism": card_data.get("symbolism_tr", card_data["symbolism"]),
                "yes_no_meaning": card_data.get("yes_no_meaning_tr", card_data["yes_no_meaning"])
            }
        else:
            # Return English version (default)
            card = {
                "id": card_data["id"],
                "name": card_data["name"],
                "image_url": card_data["image_url"],
                "keywords": card_data["keywords"],
                "meaning_upright": card_data["meaning_upright"],
                "meaning_reversed": card_data["meaning_reversed"],
                "description": card_data["description"],
                "symbolism": card_data["symbolism"],
                "yes_no_meaning": card_data["yes_no_meaning"]
            }
        cards.append(TarotCard(**card))
    return cards

@api_router.get("/cards/{card_id}", response_model=TarotCard)
async def get_card(card_id: int, language: str = "en"):
    """Get a specific card by ID with language support. Includes base64 image."""
    for card_data in get_unique_major_arcana():
        if card_data["id"] == card_id:
            # Build base card dict with language
            if language == "tr":
                card = {
                    "id": card_data["id"],
                    "name": card_data.get("name_tr", card_data["name"]),
                    "image_url": card_data["image_url"],
                    "keywords": card_data.get("keywords_tr", card_data["keywords"]),
                    "meaning_upright": card_data.get("meaning_upright_tr", card_data["meaning_upright"]),
                    "meaning_reversed": card_data.get("meaning_reversed_tr", card_data["meaning_reversed"]),
                    "description": card_data.get("description_tr", card_data["description"]),
                    "symbolism": card_data.get("symbolism_tr", card_data["symbolism"]),
                    "yes_no_meaning": card_data.get("yes_no_meaning_tr", card_data["yes_no_meaning"])
                }
            else:
                card = {
                    "id": card_data["id"],
                    "name": card_data["name"],
                    "image_url": card_data["image_url"],
                    "keywords": card_data["keywords"],
                    "meaning_upright": card_data["meaning_upright"],
                    "meaning_reversed": card_data["meaning_reversed"],
                    "description": card_data["description"],
                    "symbolism": card_data["symbolism"],
                    "yes_no_meaning": card_data["yes_no_meaning"]
                }
            # Attach base64 image from local file if available
            local_path = IMAGES_BY_ID.get(card_id)
            card["image_base64"] = load_image_b64(local_path) if local_path else None
            return TarotCard(**card)
    raise HTTPException(status_code=404, detail="Card not found")

@api_router.get("/cards/{card_id}/image")
async def get_card_image(card_id: int):
    """Return raw image bytes for a card to be used as thumbnail in lists"""
    local_path = IMAGES_BY_ID.get(card_id)
    if not local_path:
        raise HTTPException(status_code=404, detail="Image not found")
    try:
        abs_path = (ROOT_DIR / local_path).resolve()
        if not abs_path.exists():
            raise HTTPException(status_code=404, detail="Image file missing")
        mime, _ = mimetypes.guess_type(str(abs_path))
        if not mime:
            mime = "image/jpeg"
        with open(abs_path, "rb") as f:
            data = f.read()
        return Response(content=data, media_type=mime)
    except HTTPException:
        raise
    except Exception as e:
        logging.warning(f"Failed to serve image for card {card_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to load image")

@api_router.get("/download/project-zip")
async def download_project_zip():
    """Serve the prepared project ZIP for download."""
    try:
        zip_name = "mystic-tarot-24-frontend-backend.zip"
        zip_path = (ROOT_DIR / ".." / zip_name).resolve()
        if not zip_path.exists():
            raise HTTPException(status_code=404, detail="Zip not found. Please ask to regenerate.")
        return FileResponse(path=str(zip_path), media_type="application/zip", filename=zip_name)
    except HTTPException:
        raise
    except Exception as e:
        logging.warning(f"Zip download failed: {e}")
        raise HTTPException(status_code=500, detail="Failed to serve zip")


@api_router.get("/reading-types", response_model=List[ReadingType])
async def get_reading_types():
    """Get all available reading types"""
    return [ReadingType(**reading_type) for reading_type in READING_TYPES]

@api_router.post("/reading/{reading_type}", response_model=TarotReading)
async def create_reading(reading_type: str, question: Optional[str] = None, language: str = "en", ai: Optional[str] = None, tone: Optional[str] = "gentle", length: Optional[str] = "medium"):
    """Create a new tarot reading with language support"""
    # Normalize enums
    tone_allowed = {"gentle", "analytical", "motivational", "spiritual", "direct"}
    length_allowed = {"short", "medium", "long"}
    if tone not in tone_allowed:
        tone = "gentle"
    if length not in length_allowed:
        length = "medium"
    ai_bypass = (ai == "off")

    # Find reading type configuration
    reading_config = None
    for rt in READING_TYPES:
        if rt["id"] == reading_type:
            reading_config = rt
            break
    
    if not reading_config:
        raise HTTPException(status_code=404, detail="Reading type not found")
    
    # Select random cards
    selected_cards = random.sample(get_unique_major_arcana(), reading_config["card_count"])
    
    # Create cards with positions - use appropriate language
    reading_cards = []
    for i, card_data in enumerate(selected_cards):
        # Use Turkish data if language is tr, otherwise English
        if language == "tr":
            card_info = {
                "id": card_data["id"],
                "name": card_data.get("name_tr", card_data["name"]),
                "image_url": card_data["image_url"],
                "keywords": card_data.get("keywords_tr", card_data["keywords"]),
                "meaning_upright": card_data.get("meaning_upright_tr", card_data["meaning_upright"]),
                "meaning_reversed": card_data.get("meaning_reversed_tr", card_data["meaning_reversed"]),
                "description": card_data.get("description_tr", card_data["description"]),
                "symbolism": card_data.get("symbolism_tr", card_data["symbolism"]),
                "yes_no_meaning": card_data.get("yes_no_meaning_tr", card_data["yes_no_meaning"])
            }
        else:
            card_info = {
                "id": card_data["id"],
                "name": card_data["name"],
                "image_url": card_data["image_url"],
                "keywords": card_data["keywords"],
                "meaning_upright": card_data["meaning_upright"],
                "meaning_reversed": card_data["meaning_reversed"],
                "description": card_data["description"],
                "symbolism": card_data["symbolism"],
                "yes_no_meaning": card_data["yes_no_meaning"]
            }
        
        card_with_position = {
            "card": card_info,
            "position": reading_config["positions"][i],
            "reversed": random.choice([True, False])  # Random orientation
        }
        reading_cards.append(card_with_position)
    
    # Generate interpretation based on reading type and language
    interpretation = generate_interpretation(reading_type, reading_cards, question, language)
    
    # Create reading object
    reading = TarotReading(
        reading_type=reading_type,
        cards=reading_cards,
        interpretation=interpretation
    )
    
    # Save to database
    await db.readings.insert_one(reading.dict())
    
    return reading

@api_router.get("/readings", response_model=List[TarotReading])
async def get_readings(limit: int = 10):
    """Get recent readings"""
    readings = await db.readings.find().sort("timestamp", -1).limit(limit).to_list(limit)
    return [TarotReading(**reading) for reading in readings]

def generate_interpretation(reading_type: str, cards: List[Dict], question: Optional[str] = None, language: str = "en", tone: str = "gentle", length: str = "medium", ai_bypass: bool = False) -> str:
    """Generate interpretation using AI if available; fallback to rule-based text.
    tone: gentle|analytical|motivational|spiritual|direct (AI only)
    length: short|medium|long (applies to both AI and fallback via post-processing)
    """
    import os, requests, json
    ai_key = os.getenv('EMERGENT_LLM_KEY')

    # Tone/Length guides for prompt
    TONE_GUIDE_TR = {
        "gentle": "Üslup: nazik, empatik, yargısız.",
        "analytical": "Üslup: analitik, kanıtsal, net yapı.",
        "motivational": "Üslup: motive edici, cesaretlendiren.",
        "spiritual": "Üslup: sezgisel, ritüel/dingin dil; aşırı determinizmden kaçın.",
        "direct": "Üslup: doğrudan, kısa ve net; dolandırmadan öner."
    }
    LENGTH_GUIDE_TR = {
        "short": "Yaklaşık 100 kelime (±%20).",
        "medium": "Yaklaşık 200 kelime (±%20).",
        "long": "Yaklaşık 350 kelime (±%20)."
    }

    TARGET_WORDS = {"short": 100, "medium": 200, "long": 350}

    def postprocess_length(text: str) -> str:
        """Trim text to approx target word count (only trims if longer)"""
        try:
            target = TARGET_WORDS.get(length, 200)
            words = text.split()
            max_words = int(target * 1.2)
            if len(words) > max_words:
                # trim on sentence boundary if possible
                sentences = [s.strip() for s in text.replace('\n', ' ').split('.') if s.strip()]
                out = []
                count = 0
                for s in sentences:
                    wc = len(s.split())
                    if count + wc <= max_words:
                        out.append(s)
                        count += wc
                    else:
                        break
                txt = '. '.join(out)
                if txt:
                    if not txt.endswith('.'):
                        txt += '.'
                    return txt
                return ' '.join(words[:max_words])
            return text
        except Exception:
            return text

    # Build AI prompt summary from provided cards
    def build_prompt() -> str:
        lang_line = "Lütfen yanıtı Türkçe yaz." if language == "tr" else "Please respond in English."
        rt = reading_type
        if language == "tr":
            rt = {
                "card_of_day": "Günün Kartı",
                "classic_tarot": "Klasik Tarot",
                "path_of_day": "Günün Yolu",
                "yes_no": "Evet/Hayır",
                "couples_tarot": "Çiftler Tarot"
            }.get(reading_type, reading_type)
        lines = [
            f"Okuma türü: {rt}",
            f"Dil: {'Türkçe' if language=='tr' else 'English'}",
        ]
        if question:
            lines.append(("Soru: " if language=="tr" else "Question: ") + str(question))
        lines.append("Kartlar:")
        for idx, item in enumerate(cards, 1):
            c = item["card"]
            pos = item.get("position", f"Card {idx}")
            rev = item.get("reversed", False)
            meaning_key = f"meaning_{'reversed' if rev else 'upright'}"
            meaning = c.get(meaning_key, "")
            name = c.get("name", "")
            kw = ", ".join(c.get("keywords", [])[:4])
            if language == "tr":
                lines.append(f"- {pos}: {name}{' (Ters)' if rev else ''} | Anahtar kelimeler: {kw} | Özet: {meaning}")
            else:
                lines.append(f"- {pos}: {name}{' (Reversed)' if rev else ''} | Keywords: {kw} | Summary: {meaning}")
        if language == "tr":
            # Tone and length instructions
            tone_line = TONE_GUIDE_TR.get(tone, TONE_GUIDE_TR['gentle'])
            len_line = LENGTH_GUIDE_TR.get(length, LENGTH_GUIDE_TR['medium'])
            lines.append(tone_line)
            lines.append(len_line)
            lines.append("Biçim: 1 cümle 'bugünün teması' + 3 kısa madde (Aşk/İş/Para) + 1 onay cümlesi.")
            lines.append("Kaçın: kesin kader söylemleri, korku dili. Öner: uygulanabilir, nazik rehberlik.")
        else:
            # English guidance
            tone_map_en = {
                "gentle": "Tone: gentle, empathetic, non-judgmental.",
                "analytical": "Tone: analytical, evidence-based, structured.",
                "motivational": "Tone: motivational, encouraging.",
                "spiritual": "Tone: intuitive, calm, avoid determinism.",
                "direct": "Tone: direct, concise, no beating around the bush."
            }
            length_map_en = {
                "short": "About 100 words (±20%).",
                "medium": "About 200 words (±20%).",
                "long": "About 350 words (±20%)."
            }
            lines.append(tone_map_en.get(tone, tone_map_en['gentle']))
            lines.append(length_map_en.get(length, length_map_en['medium']))
            lines.append("Format: 1-sentence 'theme of the day' + 3 short bullets (Love/Work/Money) + 1 closing sentence.")
            lines.append("Avoid deterministic/fear language. Provide actionable, kind guidance.")
        lines.append(lang_line)
        return "\n".join(lines)

    # Try AI if key exists and not bypassed
    if ai_key and not ai_bypass:
        try:
            payload = {
                "model": os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
                "messages": [
                    {"role": "system", "content": "You are an expert Tarot interpreter."},
                    {"role": "user", "content": build_prompt()}
                ],
                "temperature": float(os.getenv("OPENAI_TEMPERATURE", "0.7")),
                "max_tokens": int(os.getenv("OPENAI_MAX_TOKENS", "600"))
            }
            headers = {
                "Authorization": f"Bearer {ai_key}",
                "Content-Type": "application/json"
            }
            url = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1") + "/chat/completions"
            resp = requests.post(url, headers=headers, data=json.dumps(payload), timeout=20)
            if resp.status_code == 200:
                data = resp.json()
                if data.get("choices"):
                    content = data["choices"][0]["message"]["content"]
                    if content and isinstance(content, str):
                        return postprocess_length(content.strip())
            # fall through on non-200 or empty content
        except Exception as e:
            logging.warning(f"AI interpretation failed, falling back. Error: {e}")

    # Fallback: original rule-based interpretation
    interpretation = ""
    
    if reading_type == "card_of_day":
        card = cards[0]["card"]
        reversed = cards[0]["reversed"]
        
        # Use language-specific meaning
        meaning_key = f"meaning_{'reversed' if reversed else 'upright'}"
        if language == "tr":
            meaning_key += "_tr"
        meaning = card.get(meaning_key, card['meaning_reversed' if reversed else 'meaning_upright'])
        
        if language == "tr":
            interpretation = f"Bugünün kartınız {card['name']}{'(Ters)' if reversed else ''}.\n\n{meaning}\n\nBu kart bugün {', '.join(card['keywords'][:2])} konularına odaklanmanız gerektiğini önerir. {card['description']}"
        else:
            interpretation = f"Your card for today is {card['name']}{'(Reversed)' if reversed else ''}.\n\n{meaning}\n\nThis card suggests that today you should focus on {', '.join(card['keywords'][:2])}. {card['description']}"
    
    elif reading_type == "classic_tarot":
        if language == "tr":
            interpretation = "**Klasik Üç Kart Falı**\n\n"
        else:
            interpretation = "**Classic Three-Card Reading**\n\n"
            
        for i, card_data in enumerate(cards):
            card = card_data["card"]
            position = card_data["position"]
            reversed = card_data["reversed"]
            
            # Use language-specific meaning
            meaning_key = f"meaning_{'reversed' if reversed else 'upright'}"
            if language == "tr":
                meaning_key += "_tr"
            meaning = card.get(meaning_key, card['meaning_reversed' if reversed else 'meaning_upright'])
            
            interpretation += f"**{position}: {card['name']}{'(Ters)' if reversed and language == 'tr' else '(Reversed)' if reversed else ''}**\n{meaning}\n\n"
        
        if language == "tr":
            interpretation += "**Sağlık Önerisi**: Dengeye odaklanın ve vücudunuzun ihtiyaçlarını dinleyin. Kartlar hem fiziksel hem de duygusal sağlığa dikkat etmenizi öneriyor."
        else:
            interpretation += "**Health Advice**: Focus on balance and listen to your body's needs. The cards suggest paying attention to both physical and emotional well-being."
    
    elif reading_type == "path_of_day":
        if language == "tr":
            interpretation = "**Günün Yolu - Dört Alan Falı**\n\n"
            advice_areas = ["iş ortamına", "finansal kararlara", "romantik bağlantılara", "genel yaşam yönüne"]
        else:
            interpretation = "**Path of the Day - Four Areas Reading**\n\n"
            advice_areas = ["work environment", "financial decisions", "romantic connections", "overall life direction"]
            
        for i, card_data in enumerate(cards):
            card = card_data["card"]
            position = card_data["position"]
            reversed = card_data["reversed"]
            
            # Use language-specific meaning
            meaning_key = f"meaning_{'reversed' if reversed else 'upright'}"
            if language == "tr":
                meaning_key += "_tr"
            meaning = card.get(meaning_key, card['meaning_reversed' if reversed else 'meaning_upright'])
            
            interpretation += f"**{position}: {card['name']}{'(Ters)' if reversed and language == 'tr' else '(Reversed)' if reversed else ''}**\n{meaning}\n"
            if language == "tr":
                interpretation += f"Bugün {advice_areas[i]} odaklanın.\n\n"
            else:
                interpretation += f"Focus on {advice_areas[i]} today.\n\n"
    
    elif reading_type == "couples_tarot":
        if language == "tr":
            interpretation = "**Çiftler Tarot Falı**\n\n"
            relationship_aspects = [
                "ilişkideki duygusal durumunuz",
                "partnerinizin perspektifi ve hisleri", 
                "ikiniz arasındaki mevcut dinamik",
                "dikkat gerektiren engeller",
                "ilişkinizin potansiyel geleceği"
            ]
        else:
            interpretation = "**Couples Tarot Reading**\n\n"
            relationship_aspects = [
                "your emotional state in the relationship",
                "your partner's perspective and feelings", 
                "the current dynamic between you both",
                "obstacles that need attention",
                "the potential future of your relationship"
            ]
            
        for i, card_data in enumerate(cards):
            card = card_data["card"]
            position = card_data["position"]
            reversed = card_data["reversed"]
            
            # Use language-specific meaning
            meaning_key = f"meaning_{'reversed' if reversed else 'upright'}"
            if language == "tr":
                meaning_key += "_tr"
            meaning = card.get(meaning_key, card['meaning_reversed' if reversed else 'meaning_upright'])
            
            interpretation += f"**{position}: {card['name']}{'(Ters)' if reversed and language == 'tr' else '(Reversed)' if reversed else ''}**\n{meaning}\n"
            if language == "tr":
                interpretation += f"Bu {relationship_aspects[i]} ile ilgilidir.\n\n"
            else:
                interpretation += f"This relates to {relationship_aspects[i]}.\n\n"
    
    elif reading_type == "yes_no":
        card = cards[0]["card"]
        reversed = cards[0]["reversed"]
        
        # Use language-specific meaning
        meaning_key = f"meaning_{'reversed' if reversed else 'upright'}"
        if language == "tr":
            meaning_key += "_tr"
        meaning = card.get(meaning_key, card['meaning_reversed' if reversed else 'meaning_upright'])
        
        if reversed:
            yes_no_answer = "Hayır" if language == "tr" else "No"
        else:
            # Use language-specific yes_no_meaning
            yes_no_key = "yes_no_meaning_tr" if language == "tr" else "yes_no_meaning"
            yes_no_answer = card.get(yes_no_key, card["yes_no_meaning"])
        
        if language == "tr":
            interpretation = f"**Soru**: {question or 'Sorunuz'}\n\n**Cevap**: {yes_no_answer}\n\n**Kart**: {card['name']}{'(Ters)' if reversed else ''}\n\n**Gerekçe**: {meaning}"
        else:
            interpretation = f"**Question**: {question or 'Your question'}\n\n**Answer**: {yes_no_answer}\n\n**Card**: {card['name']}{'(Reversed)' if reversed else ''}\n\n**Reasoning**: {meaning}"
    
    return interpretation

# Include the router in the main app
app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()