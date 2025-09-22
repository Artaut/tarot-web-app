import React, { useState } from 'react';
import { 
  View, 
  Text, 
  StyleSheet, 
  ScrollView, 
  TouchableOpacity, 
  SafeAreaView,
  StatusBar,
  Dimensions
} from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { router } from 'expo-router';

const { width, height } = Dimensions.get('window');

// Dil desteği
const translations = {
  en: {
    title: "Daily Tarot",
    subtitle: "Discover your destiny through the ancient wisdom of tarot",
    chooseReading: "Choose Your Reading",
    learnExplore: "Learn & Explore",
    tapToBegin: "Tap to begin",
    footerText: "Anticipate your future with the wisdom of the ancient Tarot",
    readings: {
      card_of_day: {
        name: "Card of the Day",
        description: "The simplest Tarot in which you choose the card that will mark your day."
      },
      classic_tarot: {
        name: "Classic Tarot", 
        description: "A three-card spread that will give you the forecast for today and also offer you some advice on health."
      },
      path_of_day: {
        name: "The Path of the Day",
        description: "Four-card spread to guess work, money and love for today."
      },
      couples_tarot: {
        name: "The Tarot of the Couples",
        description: "This love Tarot predicts the future of any couple and offers advice on how to improve their relationship."
      },
      yes_no: {
        name: "Yes or No",
        description: "Ask the Tarot a question for a direct and reasoned answer."
      }
    },
    features: {
      cardMeanings: {
        title: "Card Meanings",
        description: "Explore the 22 Major Arcana cards and their meanings"
      },
      quiz: {
        title: "Tarot Quiz Game", 
        description: "Test your knowledge with 198 questions across 3 levels"
      }
    }
  },
  tr: {
    title: "Günlük Tarot",
    subtitle: "Tarot'un kadim bilgeliği ile kaderinizi keşfedin",
    chooseReading: "Falınızı Seçin",
    learnExplore: "Öğren & Keşfet", 
    tapToBegin: "Başlamak için dokunun",
    footerText: "Kadim Tarot bilgeliği ile geleceğinizi öngörün",
    readings: {
      card_of_day: {
        name: "Günün Kartı",
        description: "Gününüzü belirleyecek kartı seçtiğiniz en basit Tarot falı."
      },
      classic_tarot: {
        name: "Klasik Tarot",
        description: "Bugün için öngörü veren ve sağlık konusunda tavsiye sunan üç kartlı yayılım."
      },
      path_of_day: {
        name: "Günün Yolu",
        description: "Bugün için iş, para ve aşk konularını tahmin eden dört kartlı yayılım."
      },
      couples_tarot: {
        name: "Çiftler Tarot'u",
        description: "Bu aşk Tarot'u herhangi bir çiftin geleceğini öngörür ve ilişkilerini geliştirme konusunda tavsiye verir."
      },
      yes_no: {
        name: "Evet ya da Hayır",
        description: "Tarot'a bir soru sorun ve doğrudan, mantıklı bir cevap alın."
      }
    },
    features: {
      cardMeanings: {
        title: "Kart Anlamları",
        description: "22 Büyük Arkana kartını ve anlamlarını keşfedin"
      },
      quiz: {
        title: "Tarot Quiz Oyunu",
        description: "3 seviyede 198 soru ile bilginizi test edin"
      }
    }
  }
};

const readingTypes = [
  {
    id: 'card_of_day',
    name: 'Card of the Day',
    description: 'The simplest Tarot in which you choose the card that will mark your day.',
    icon: 'sunny-outline' as keyof typeof Ionicons.glyphMap,
    cardCount: 1,
    color: '#FF6B35'
  },
  {
    id: 'classic_tarot',
    name: 'Classic Tarot',
    description: 'A three-card spread that will give you the forecast for today and also offer you some advice on health.',
    icon: 'library-outline' as keyof typeof Ionicons.glyphMap,
    cardCount: 3,
    color: '#4C63D2'
  },
  {
    id: 'path_of_day',
    name: 'The Path of the Day',
    description: 'Four-card spread to guess work, money and love for today.',
    icon: 'compass-outline' as keyof typeof Ionicons.glyphMap,
    cardCount: 4,
    color: '#00C851'
  },
  {
    id: 'couples_tarot',
    name: 'The Tarot of the Couples',
    description: 'This love Tarot predicts the future of any couple and offers advice on how to improve their relationship.',
    icon: 'heart-outline' as keyof typeof Ionicons.glyphMap,
    cardCount: 5,
    color: '#E91E63'
  },
  {
    id: 'yes_no',
    name: 'Yes or No',
    description: 'Ask the Tarot a question for a direct and reasoned answer.',
    icon: 'help-circle-outline' as keyof typeof Ionicons.glyphMap,
    cardCount: 1,
    color: '#9C27B0'
  }
];

export default function HomeScreen() {
  const [language, setLanguage] = useState('tr'); // Varsayılan Türkçe
  const t = translations[language];

  const toggleLanguage = () => {
    setLanguage(language === 'en' ? 'tr' : 'en');
  };

  return (
    <SafeAreaView style={styles.container}>
      <StatusBar barStyle="light-content" backgroundColor="#0a0a0a" />
      
      <View style={styles.background}>
        <ScrollView showsVerticalScrollIndicator={false}>
          {/* Language Toggle Button */}
          <View style={styles.languageContainer}>
            <TouchableOpacity 
              style={styles.languageButton}
              onPress={toggleLanguage}
              activeOpacity={0.7}
            >
              <Ionicons name="language" size={20} color="white" />
              <Text style={styles.languageText}>
                {language === 'en' ? 'TR' : 'EN'}
              </Text>
            </TouchableOpacity>
          </View>

          {/* Header */}
          <View style={styles.header}>
            <Text style={styles.title}>{t.title}</Text>
            <Text style={styles.subtitle}>{t.subtitle}</Text>
          </View>

          {/* Reading Types */}
          <View style={styles.readingsContainer}>
            <Text style={styles.sectionTitle}>{t.chooseReading}</Text>
            
            {readingTypes.map((reading, index) => (
              <TouchableOpacity
                key={reading.id}
                style={[styles.readingCard, { backgroundColor: reading.color }]}
                onPress={() => router.push(`/reading/${reading.id}`)}
                activeOpacity={0.7}
              >
                <View style={styles.readingCardContent}>
                  <View style={styles.readingCardHeader}>
                    <Ionicons 
                      name={reading.icon} 
                      size={32} 
                      color="white" 
                      style={styles.readingIcon}
                    />
                    <View style={styles.cardCountBadge}>
                      <Text style={styles.cardCountText}>{reading.cardCount}</Text>
                    </View>
                  </View>
                  
                  <Text style={styles.readingTitle}>
                    {t.readings[reading.id].name}
                  </Text>
                  <Text style={styles.readingDescription}>
                    {t.readings[reading.id].description}
                  </Text>
                  
                  <View style={styles.readingFooter}>
                    <Text style={styles.readingAction}>{t.tapToBegin}</Text>
                    <Ionicons name="arrow-forward" size={20} color="rgba(255,255,255,0.8)" />
                  </View>
                </View>
              </TouchableOpacity>
            ))}
          </View>

          {/* Additional Features */}
          <View style={styles.featuresContainer}>
            <Text style={styles.sectionTitle}>{t.learnExplore}</Text>
            
            <TouchableOpacity
              style={[styles.featureCard, { backgroundColor: '#5D4037' }]}
              onPress={() => router.push('/cards')}
              activeOpacity={0.7}
            >
              <Ionicons name="library" size={28} color="#FFAB91" />
              <View style={styles.featureTextContainer}>
                <Text style={styles.featureTitle}>{t.features.cardMeanings.title}</Text>
                <Text style={styles.featureDescription}>{t.features.cardMeanings.description}</Text>
              </View>
              <Ionicons name="chevron-forward" size={24} color="rgba(255,255,255,0.6)" />
            </TouchableOpacity>

            <TouchableOpacity
              style={[styles.featureCard, { backgroundColor: '#3F51B5' }]}
              onPress={() => router.push('/quiz')}
              activeOpacity={0.7}
            >
              <Ionicons name="school" size={28} color="#8C9EFF" />
              <View style={styles.featureTextContainer}>
                <Text style={styles.featureTitle}>{t.features.quiz.title}</Text>
                <Text style={styles.featureDescription}>{t.features.quiz.description}</Text>
              </View>
              <Ionicons name="chevron-forward" size={24} color="rgba(255,255,255,0.6)" />
            </TouchableOpacity>
          </View>

          {/* Footer */}
          <View style={styles.footer}>
            <Text style={styles.footerText}>
              {t.footerText}
            </Text>
          </View>
        </ScrollView>
      </View>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#0a0a0a',
  },
  background: {
    flex: 1,
  },
  header: {
    paddingHorizontal: 20,
    paddingTop: 20,
    paddingBottom: 30,
    alignItems: 'center',
  },
  title: {
    fontSize: 36,
    fontWeight: 'bold',
    color: '#FFFFFF',
    textAlign: 'center',
    marginBottom: 8,
    letterSpacing: 1,
  },
  subtitle: {
    fontSize: 16,
    color: 'rgba(255,255,255,0.7)',
    textAlign: 'center',
    lineHeight: 24,
    paddingHorizontal: 20,
  },
  readingsContainer: {
    paddingHorizontal: 20,
    marginBottom: 30,
  },
  sectionTitle: {
    fontSize: 24,
    fontWeight: '600',
    color: '#FFFFFF',
    marginBottom: 20,
    textAlign: 'center',
  },
  readingCard: {
    marginBottom: 16,
    borderRadius: 16,
    overflow: 'hidden',
    elevation: 8,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.3,
    shadowRadius: 8,
    padding: 20,
  },
  readingCardContent: {
    flex: 1,
  },
  readingCardHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 12,
  },
  readingIcon: {
    marginRight: 12,
  },
  cardCountBadge: {
    backgroundColor: 'rgba(255,255,255,0.2)',
    borderRadius: 12,
    paddingHorizontal: 8,
    paddingVertical: 4,
  },
  cardCountText: {
    color: 'white',
    fontSize: 12,
    fontWeight: '600',
  },
  readingTitle: {
    fontSize: 20,
    fontWeight: 'bold',
    color: '#FFFFFF',
    marginBottom: 8,
  },
  readingDescription: {
    fontSize: 14,
    color: 'rgba(255,255,255,0.9)',
    lineHeight: 20,
    marginBottom: 16,
  },
  readingFooter: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
  },
  readingAction: {
    fontSize: 14,
    color: 'rgba(255,255,255,0.8)',
    fontWeight: '500',
  },
  featuresContainer: {
    paddingHorizontal: 20,
    marginBottom: 30,
  },
  featureCard: {
    marginBottom: 12,
    borderRadius: 12,
    overflow: 'hidden',
    padding: 16,
    flexDirection: 'row',
    alignItems: 'center',
  },
  featureTextContainer: {
    flex: 1,
    marginLeft: 16,
  },
  featureTitle: {
    fontSize: 16,
    fontWeight: '600',
    color: '#FFFFFF',
    marginBottom: 4,
  },
  featureDescription: {
    fontSize: 12,
    color: 'rgba(255,255,255,0.7)',
    lineHeight: 16,
  },
  footer: {
    paddingHorizontal: 20,
    paddingBottom: 40,
    alignItems: 'center',
  },
  footerText: {
    fontSize: 14,
    color: 'rgba(255,255,255,0.5)',
    textAlign: 'center',
    fontStyle: 'italic',
  },
});