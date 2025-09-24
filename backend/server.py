from fastapi import FastAPI, APIRouter, HTTPException
from fastapi.responses import JSONResponse, Response, FileResponse
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any, Tuple, Literal
import uuid
from datetime import datetime
import random
import base64
import mimetypes
from functools import lru_cache

load_dotenv()

ROOT_DIR = Path(__file__).parent.resolve()

app = FastAPI()
api_router = APIRouter(prefix="/api")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client["tarot_db"]

# Models
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

# Major Arcana minimal data (22 unique cards). Turkish fields may be absent; frontend falls back.
MAJOR_ARCANA: List[Dict[str, Any]] = [
    {"id": 0,  "name": "The Fool",         "image_url": "", "keywords": [], "meaning_upright": "", "meaning_reversed": "", "description": "", "symbolism": "", "yes_no_meaning": ""},
    {"id": 1,  "name": "The Magician",     "image_url": "", "keywords": [], "meaning_upright": "", "meaning_reversed": "", "description": "", "symbolism": "", "yes_no_meaning": ""},
    {"id": 2,  "name": "The High Priestess","image_url": "", "keywords": [], "meaning_upright": "", "meaning_reversed": "", "description": "", "symbolism": "", "yes_no_meaning": ""},
    {"id": 3,  "name": "The Empress",      "image_url": "", "keywords": [], "meaning_upright": "", "meaning_reversed": "", "description": "", "symbolism": "", "yes_no_meaning": ""},
    {"id": 4,  "name": "The Emperor",      "image_url": "", "keywords": [], "meaning_upright": "", "meaning_reversed": "", "description": "", "symbolism": "", "yes_no_meaning": ""},
    {"id": 5,  "name": "The Hierophant",   "image_url": "", "keywords": [], "meaning_upright": "", "meaning_reversed": "", "description": "", "symbolism": "", "yes_no_meaning": ""},
    {"id": 6,  "name": "The Lovers",       "image_url": "", "keywords": [], "meaning_upright": "", "meaning_reversed": "", "description": "", "symbolism": "", "yes_no_meaning": ""},
    {"id": 7,  "name": "The Chariot",      "image_url": "", "keywords": [], "meaning_upright": "", "meaning_reversed": "", "description": "", "symbolism": "", "yes_no_meaning": ""},
    {"id": 8,  "name": "Strength",         "image_url": "", "keywords": [], "meaning_upright": "", "meaning_reversed": "", "description": "", "symbolism": "", "yes_no_meaning": ""},
    {"id": 9,  "name": "The Hermit",       "image_url": "", "keywords": [], "meaning_upright": "", "meaning_reversed": "", "description": "", "symbolism": "", "yes_no_meaning": ""},
    {"id": 10, "name": "Wheel of Fortune", "image_url": "", "keywords": [], "meaning_upright": "", "meaning_reversed": "", "description": "", "symbolism": "", "yes_no_meaning": ""},
    {"id": 11, "name": "Justice",          "image_url": "", "keywords": [], "meaning_upright": "", "meaning_reversed": "", "description": "", "symbolism": "", "yes_no_meaning": ""},
    {"id": 12, "name": "The Hanged Man",   "image_url": "", "keywords": [], "meaning_upright": "", "meaning_reversed": "", "description": "", "symbolism": "", "yes_no_meaning": ""},
    {"id": 13, "name": "Death",            "image_url": "", "keywords": [], "meaning_upright": "", "meaning_reversed": "", "description": "", "symbolism": "", "yes_no_meaning": ""},
    {"id": 14, "name": "Temperance",       "image_url": "", "keywords": [], "meaning_upright": "", "meaning_reversed": "", "description": "", "symbolism": "", "yes_no_meaning": ""},
    {"id": 15, "name": "The Devil",        "image_url": "", "keywords": [], "meaning_upright": "", "meaning_reversed": "", "description": "", "symbolism": "", "yes_no_meaning": ""},
    {"id": 16, "name": "The Tower",        "image_url": "", "keywords": [], "meaning_upright": "", "meaning_reversed": "", "description": "", "symbolism": "", "yes_no_meaning": ""},
    {"id": 17, "name": "The Star",         "image_url": "", "keywords": [], "meaning_upright": "", "meaning_reversed": "", "description": "", "symbolism": "", "yes_no_meaning": ""},
    {"id": 18, "name": "The Moon",         "image_url": "", "keywords": [], "meaning_upright": "", "meaning_reversed": "", "description": "", "symbolism": "", "yes_no_meaning": ""},
    {"id": 19, "name": "The Sun",          "image_url": "", "keywords": [], "meaning_upright": "", "meaning_reversed": "", "description": "", "symbolism": "", "yes_no_meaning": ""},
    {"id": 20, "name": "Judgement",        "image_url": "", "keywords": [], "meaning_upright": "", "meaning_reversed": "", "description": "", "symbolism": "", "yes_no_meaning": ""},
    {"id": 21, "name": "The World",        "image_url": "", "keywords": [], "meaning_upright": "", "meaning_reversed": "", "description": "", "symbolism": "", "yes_no_meaning": ""},
]

# Reading types minimal config
READING_TYPES: List[Dict[str, Any]] = [
    {"id": "card_of_day", "name": "Card of the Day", "description": "", "card_count": 1, "positions": ["Your Day"]},
    {"id": "classic_tarot", "name": "Classic Tarot", "description": "", "card_count": 3, "positions": ["Past", "Present", "Future"]},
    {"id": "path_of_day", "name": "Path of the Day", "description": "", "card_count": 4, "positions": ["Work", "Money", "Love", "Advice"]},
    {"id": "couples_tarot", "name": "Couples Tarot", "description": "", "card_count": 5, "positions": ["You", "Partner", "Bond", "Obstacle", "Outcome"]},
    {"id": "yes_no", "name": "Yes or No", "description": "", "card_count": 1, "positions": ["Answer"]},
]

# Deduplicate to exactly 22 unique cards by id
@lru_cache(maxsize=None)
def get_unique_major_arcana() -> List[Dict[str, Any]]:
    seen: Dict[int, Dict[str, Any]] = {}
    for c in MAJOR_ARCANA:
        cid = c.get('id')
        if cid is not None and cid not in seen:
            seen[cid] = c
    return [seen[i] for i in sorted(seen.keys())]

# Map ID -> local image path
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

# Sync image_url in MAJOR_ARCANA
for _card in MAJOR_ARCANA:
    cid = _card.get('id')
    local_path = IMAGES_BY_ID.get(cid)
    if local_path:
        _card['image_url'] = local_path

@api_router.get("/cards/{card_id}", response_model=TarotCard)
async def get_card(card_id: int, language: str = "en"):
    for card_data in get_unique_major_arcana():
        if card_data["id"] == card_id:
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
            local_path = IMAGES_BY_ID.get(card_id)
            card["image_base64"] = load_image_b64(local_path) if local_path else None
            return TarotCard(**card)
    raise HTTPException(status_code=404, detail="Card not found")

@api_router.get("/cards/{card_id}/image")
async def get_card_image(card_id: int):
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

# Telemetry logging
TelemetryEventName = Literal[
    "reading_begin",
    "reading_result",
    "ai_toggle",
    "tone_change",
    "length_change",
    "share_click",
    "paywall_view",
    "purchase_attempt",
    "purchase_success",
    "purchase_error",
    "restore_success",
]


class TelemetryEvent(BaseModel):
    event: TelemetryEventName
    ts: Optional[str] = None
    sessionId: Optional[str] = None
    userIdHash: Optional[str] = None
    lang: Optional[Literal["tr","en"]] = None
    type: Optional[str] = None
    mode: Optional[Literal["ai","rule","fallback"]] = None
    aiEnabled: Optional[bool] = None
    tone: Optional[Literal["gentle","analytical","motivational","spiritual","direct"]] = None
    length: Optional[Literal["short","medium","long"]] = None
    durationMs: Optional[int] = None
    questionPresent: Optional[bool] = None

class LogPayload(BaseModel):
    events: List[TelemetryEvent] = Field(default_factory=list)

from fastapi import BackgroundTasks, Request
import json

@api_router.post("/log", status_code=204)
async def log_events(payload: LogPayload, request: Request, bg: BackgroundTasks):
    def _persist_events(p: LogPayload, client_meta: Dict[str, Any]):
        try:
            logs_dir = ROOT_DIR / "logs"
            logs_dir.mkdir(exist_ok=True)
            fname = datetime.utcnow().strftime("telemetry-%Y%m%d.jsonl")
            path = logs_dir / fname
            with open(path, "a", encoding="utf-8") as f:
                for ev in p.events:
                    data = ev.dict()
                    data["ts"] = data.get("ts") or datetime.utcnow().isoformat()
                    data["id"] = str(uuid.uuid4())
                    data["client"] = client_meta
                    keep = (data.get("event") == "reading_result") or (hash(data["id"]) % 2 == 0)
                    if keep:
                        f.write(json.dumps(data, ensure_ascii=False) + "\n")
        except Exception as e:
            logging.warning(f"Failed to persist telemetry: {e}")

    ua = request.headers.get("user-agent", "")
    client_meta = {"ua": ua[:160]}
    bg.add_task(_persist_events, payload, client_meta)
    return Response(status_code=204)

@api_router.get("/reading-types", response_model=List[ReadingType])
async def get_reading_types():
    return [ReadingType(**reading_type) for reading_type in READING_TYPES]

@api_router.get("/cards", response_model=List[TarotCard])
async def get_cards(language: str = "en"):
    cards = []
    for card_data in get_unique_major_arcana():
        if card_data.get('id') in IMAGES_BY_ID:
            card_data['image_local'] = IMAGES_BY_ID[card_data['id']]
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
                "yes_no_meaning": card_data.get("yes_no_meaning_tr", card_data["yes_no_meaning"]),
                "image_base64": None
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
                "yes_no_meaning": card_data["yes_no_meaning"],
                "image_base64": None
            }
        cards.append(card)
    return cards

@api_router.post("/reading/{reading_type}", response_model=TarotReading)
async def create_reading(reading_type: str, question: Optional[str] = None, language: str = "en", ai: Optional[str] = None, tone: Optional[str] = "gentle", length: Optional[str] = "medium"):
    # Normalize enums
    tone_allowed = {"gentle", "analytical", "motivational", "spiritual", "direct"}
    length_allowed = {"short", "medium", "long"}
    if tone not in tone_allowed:
        tone = "gentle"
    if length not in length_allowed:
        length = "medium"
    ai_bypass = (ai == "off")

    # Find reading type
    reading_config = None
    for rt in READING_TYPES:
        if rt["id"] == reading_type:
            reading_config = rt
            break
    if not reading_config:
        raise HTTPException(status_code=404, detail="Reading type not found")

    selected_cards = random.sample(get_unique_major_arcana(), reading_config["card_count"])

    reading_cards = []
    for i, card_data in enumerate(selected_cards):
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
            "reversed": random.choice([True, False])
        }
        reading_cards.append(card_with_position)

    interpretation_text, mode = generate_interpretation(
        reading_type, reading_cards, question, language, tone, length, ai_bypass
    )

    reading = TarotReading(
        reading_type=reading_type,
        cards=reading_cards,
        interpretation=interpretation_text,
        mode=mode
    )

    # Persist
    await db.readings.insert_one(reading.dict())

    return reading

# Readings list
@api_router.get("/readings", response_model=List[TarotReading])
async def get_readings(limit: int = 10):
    readings = await db.readings.find().sort("timestamp", -1).limit(limit).to_list(limit)
    return [TarotReading(**reading) for reading in readings]

# AI-powered interpretation function
import requests as _requests

def generate_interpretation(reading_type: str, cards: List[Dict], question: Optional[str] = None, language: str = "en", tone: str = "gentle", length: str = "medium", ai_bypass: bool = False) -> Tuple[str, str]:
    """Generate interpretation using AI if available; fallback to rule-based text.
    tone: gentle|analytical|motivational|spiritual|direct (AI only)
    length: short|medium|long (applies to both AI and fallback via post-processing)
    Returns (text, mode)
    """
    ai_key = os.getenv('EMERGENT_LLM_KEY')

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
        try:
            target = TARGET_WORDS.get(length, 200)
            words = text.split()
            max_words = int(target * 1.2)
            if len(words) > max_words:
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
            tone_line = TONE_GUIDE_TR.get(tone, TONE_GUIDE_TR['gentle'])
            len_line = LENGTH_GUIDE_TR.get(length, LENGTH_GUIDE_TR['medium'])
            lines.append(tone_line)
            lines.append(len_line)
            lines.append("Biçim: 1 cümle 'bugünün teması' + 3 kısa madde (Aşk/İş/Para) + 1 onay cümlesi.")
            lines.append("Kaçın: kesin kader söylemleri, korku dili. Öner: uygulanabilir, nazik rehberlik.")
        else:
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

    # AI path
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
            resp = _requests.post(url, headers=headers, data=json.dumps(payload), timeout=20)
            if resp.status_code == 200:
                data = resp.json()
                if data.get("choices"):
                    content = data["choices"][0]["message"]["content"]
                    if content and isinstance(content, str):
                        return postprocess_length(content.strip()), "ai"
        except Exception as e:
            logging.warning(f"AI interpretation failed, falling back. Error: {e}")
            # continue to fallback
        # fallback mode
        text = rule_based_interpretation(reading_type, cards, language)
        return postprocess_length(text), "fallback"

    # Rule mode
    text = rule_based_interpretation(reading_type, cards, language)
    return postprocess_length(text), "rule"

# Extracted rule-based interpretation (original logic) for reuse
def rule_based_interpretation(reading_type: str, cards: List[Dict], language: str) -> str:
    interpretation = ""
    if reading_type == "card_of_day":
        card = cards[0]["card"]
        reversed = cards[0]["reversed"]
        meaning_key = f"meaning_{'reversed' if reversed else 'upright'}"
        if language == "tr":
            meaning_key += "_tr"
        meaning = card.get(meaning_key, card['meaning_reversed' if reversed else 'meaning_upright'])
        if language == "tr":
            interpretation = f"Bugünün kartınız {card['name']}{'(Ters)' if reversed else ''}.\n\n{meaning}\n\nBu kart bugün {', '.join(card['keywords'][:2])} konularına odaklanmanız gerektiğini önerir. {card['description']}"
        else:
            interpretation = f"Your card for today is {card['name']}{'(Reversed)' if reversed else ''}.\n\n{meaning}\n\nThis card suggests that today you should focus on {', '.join(card['keywords'][:2])}. {card['description']}"
    elif reading_type == "classic_tarot":
        interpretation = "**Klasik Üç Kart Falı**\n\n" if language == "tr" else "**Classic Three-Card Reading**\n\n"
        for i, card_data in enumerate(cards):
            card = card_data["card"]
            position = card_data["position"]
            reversed = card_data["reversed"]
            meaning_key = f"meaning_{'reversed' if reversed else 'upright'}"
            if language == "tr":
                meaning_key += "_tr"
            meaning = card.get(meaning_key, card['meaning_reversed' if reversed else 'meaning_upright'])
            interpretation += f"**{position}: {card['name']}{'(Ters)' if reversed and language == 'tr' else '(Reversed)' if reversed else ''}**\n{meaning}\n\n"
        interpretation += ("**Sağlık Önerisi**: Dengeye odaklanın ve vücudunuzun ihtiyaçlarını dinleyin. Kartlar hem fiziksel hem de duygusal sağlığa dikkat etmenizi öneriyor."
                           if language == "tr" else
                           "**Health Advice**: Focus on balance and listen to your body's needs. The cards suggest paying attention to both physical and emotional well-being.")
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
            meaning_key = f"meaning_{'reversed' if reversed else 'upright'}"
            if language == "tr":
                meaning_key += "_tr"
            meaning = card.get(meaning_key, card['meaning_reversed' if reversed else 'meaning_upright'])
            interpretation += f"**{position}: {card['name']}{'(Ters)' if reversed and language == 'tr' else '(Reversed)' if reversed else ''}**\n{meaning}\n"
            interpretation += (f"Bugün {advice_areas[i]} odaklanın.\n\n" if language == "tr" else f"Focus on {advice_areas[i]} today.\n\n")
    elif reading_type == "couples_tarot":
        interpretation = "**Çiftler Tarot Falı**\n\n" if language == "tr" else "**Couples Tarot Reading**\n\n"
        for i, card_data in enumerate(cards):
            card = card_data["card"]
            position = card_data["position"]
            reversed = card_data["reversed"]
            meaning_key = f"meaning_{'reversed' if reversed else 'upright'}"
            if language == "tr":
                meaning_key += "_tr"
            meaning = card.get(meaning_key, card['meaning_reversed' if reversed else 'meaning_upright'])
            interpretation += f"**{position}: {card['name']}{'(Ters)' if reversed and language == 'tr' else '(Reversed)' if reversed else ''}**\n{meaning}\n\n"
        interpretation += ("Bu yorum, ilişki bağınızı güçlendirmek adına karşılıklı anlayış, net iletişim ve ortak hedefler üzerinde durmanızı önerir."
                           if language == "tr" else
                           "This reading suggests strengthening your bond through mutual understanding, clear communication, and shared goals.")
    elif reading_type == "yes_no":
        card = cards[0]["card"]
        interpretation = (f"**Evet/Hayır Yorumu**\n\n{card.get('yes_no_meaning_tr', card.get('yes_no_meaning', 'Belirsiz'))}"
                           if language == "tr" else
                           f"**Yes/No Interpretation**\n\n{card.get('yes_no_meaning', card.get('yes_no_meaning_tr', 'Unclear'))}")
    else:
        interpretation = ("Seçilen fal türü için yorum oluşturulamadı." if language == "tr" else "Could not generate interpretation for the selected reading type.")
    return interpretation

# Root & include
app.include_router(api_router)

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()