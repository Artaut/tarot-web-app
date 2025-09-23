import React, { useState, useEffect } from 'react';
import {
  View,
  Text,
  StyleSheet,
  TouchableOpacity,
  SafeAreaView,
  ScrollView,
  TextInput,
  Alert,
  ActivityIndicator,
  Dimensions,
  Animated,
} from 'react-native';
import { LinearGradient } from 'expo-linear-gradient';
import { Ionicons } from '@expo/vector-icons';
import { useLocalSearchParams, router } from 'expo-router';

const { width, height } = Dimensions.get('window');
const CARD_WIDTH = width * 0.25;
const CARD_HEIGHT = CARD_WIDTH * 1.5;

// Dil desteği
const translations = {
  en: {
    questionRequired: "Question Required",
    questionRequiredMessage: "Please enter your question for the tarot reading.",
    error: "Error",
    errorMessage: "Failed to get your tarot reading. Please try again.",
    askQuestion: "Ask your question:",
    questionPlaceholder: "What would you like to know?",
    beginReading: "Begin Reading",
    yourReading: "Your {readingName}",
    interpretation: "Interpretation",
    newReading: "New Reading",
    reversed: "Reversed",
    readingNotFound: "Reading type not found",
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
    }
  },
  tr: {
    questionRequired: "Soru Gerekli",
    questionRequiredMessage: "Lütfen tarot falı için sorunuzu girin.",
    error: "Hata",
    errorMessage: "Tarot falınız alınamadı. Lütfen tekrar deneyin.",
    askQuestion: "Sorunuzu sorun:",
    questionPlaceholder: "Ne öğrenmek istiyorsunuz?",
    beginReading: "Falı Başlat",
    yourReading: "{readingName} Falınız",
    interpretation: "Yorum",
    newReading: "Yeni Fal",
    reversed: "Ters",
    readingNotFound: "Fal türü bulunamadı",
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
    }
  }
};

interface TarotCard {
  id: number;
  name: string;
  image_url: string;
  keywords: string[];
  meaning_upright: string;
  meaning_reversed: string;
  description: string;
  symbolism: string;
  yes_no_meaning: string;
}

interface ReadingCard {
  card: TarotCard;
  position: string;
  reversed: boolean;
}

interface TarotReading {
  id: string;
  reading_type: string;
  cards: ReadingCard[];
  interpretation: string;
  timestamp: string;
}

export default function ReadingScreen() {
  const { type } = useLocalSearchParams<{ type: string }>();
  const [language, setLanguage] = useState('tr'); // Varsayılan Türkçe
  const t = translations[language];
  
  const [question, setQuestion] = useState('');
  const [aiEnabled, setAiEnabled] = useState(true);
  const [reading, setReading] = useState<TarotReading | null>(null);
  const [loading, setLoading] = useState(false);
  const [showCards, setShowCards] = useState(false);
  const [cardAnimations, setCardAnimations] = useState<Animated.Value[]>([]);

  const BACKEND_URL = process.env.EXPO_PUBLIC_BACKEND_URL;

  // Okuma türü konfigürasyonu
  const readingConfig = type ? t.readings[type as keyof typeof t.readings] : null;
  const needsQuestion = type === 'yes_no';

  const toggleLanguage = () => {
    setLanguage(language === 'en' ? 'tr' : 'en');
  };

  useEffect(() => {
    if (reading && reading.cards) {
      const animations = reading.cards.map(() => new Animated.Value(0));
      setCardAnimations(animations);
      
      // Animate cards appearing one by one
      animations.forEach((anim, index) => {
        Animated.timing(anim, {
          toValue: 1,
          duration: 600,
          delay: index * 300,
          useNativeDriver: true,
        }).start();
      });
    }
  }, [reading]);

  const handleStartReading = async () => {
    if (needsQuestion && !question.trim()) {
      Alert.alert(t.questionRequired, t.questionRequiredMessage);
      return;
    }

    setLoading(true);
    try {
      let url = `${BACKEND_URL}/api/reading/${type}?language=${language}`;
      if (needsQuestion) {
        url += `&question=${encodeURIComponent(question)}`;
      }
      
      const response = await fetch(url, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
      });

      if (!response.ok) {
        throw new Error('Failed to get reading');
      }

      const readingData = await response.json();
      setReading(readingData);
      setShowCards(true);
    } catch (error) {
      console.error('Error getting reading:', error);
      Alert.alert(t.error, t.errorMessage);
    } finally {
      setLoading(false);
    }
  };

  const renderCard = (cardData: ReadingCard, index: number) => {
    const animatedStyle = cardAnimations[index] ? {
      opacity: cardAnimations[index],
      transform: [
        {
          translateY: cardAnimations[index].interpolate({
            inputRange: [0, 1],
            outputRange: [50, 0],
          }),
        },
        {
          rotateY: cardData.reversed ? '180deg' : '0deg',
        },
      ],
    } : {};

    return (
      <Animated.View key={index} style={[styles.cardContainer, animatedStyle]}>
        <View style={[styles.card, cardData.reversed && styles.cardReversed]}>
          <LinearGradient
            colors={['#2D1B69', '#1A1A2E']}
            style={styles.cardGradient}
          >
            <Text style={styles.cardNumber}>{cardData.card.id}</Text>
            <Text style={styles.cardName}>{cardData.card.name}</Text>
            {cardData.reversed && <Text style={styles.reversedLabel}>{t.reversed}</Text>}
          </LinearGradient>
        </View>
        <Text style={styles.positionLabel}>{cardData.position}</Text>
      </Animated.View>
    );
  };

  if (!readingConfig) {
    return (
      <SafeAreaView style={styles.container}>
        <Text style={styles.errorText}>{t.readingNotFound}</Text>
      </SafeAreaView>
    );
  }

  return (
    <SafeAreaView style={styles.container}>
      <LinearGradient colors={['#0a0a0a', '#1a1a2e', '#16213e']} style={styles.background}>
        <ScrollView showsVerticalScrollIndicator={false}>
          {!showCards ? (
            <View style={styles.setupContainer}>
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

              {/* Back to Home Button */}
              <View style={styles.backButtonContainer}>
                <TouchableOpacity 
                  style={styles.backButton}
                  onPress={() => router.push('/')}
                  activeOpacity={0.7}
                >
                  <Ionicons name="arrow-back" size={20} color="white" />
                  <Text style={styles.backButtonText}>
                    {language === 'en' ? 'Home' : 'Ana Sayfa'}
                  </Text>
                </TouchableOpacity>
              </View>

              <LinearGradient
                colors={['#4C63D2', '#7C4DFF']} // Varsayılan renk
                style={styles.headerGradient}
                start={{ x: 0, y: 0 }}
                end={{ x: 1, y: 1 }}
              >
                <Text style={styles.readingTitle}>{readingConfig.name}</Text>
                <Text style={styles.readingDescription}>{readingConfig.description}</Text>
              </LinearGradient>

              {needsQuestion && (
                <View style={styles.questionContainer}>
                  <Text style={styles.questionLabel}>{t.askQuestion}</Text>
                  <TextInput
                    style={styles.questionInput}
                    placeholder={t.questionPlaceholder}
                    placeholderTextColor="rgba(255,255,255,0.5)"
                    value={question}
                    onChangeText={setQuestion}
                    multiline
                    textAlignVertical="top"
                  />
                </View>
              )}

              <TouchableOpacity
                style={styles.startButton}
                onPress={handleStartReading}
                disabled={loading}
              >
                <LinearGradient
                  colors={['#4C63D2', '#7C4DFF']} // Varsayılan renk
                  style={styles.startButtonGradient}
                >
                  {loading ? (
                    <ActivityIndicator color="white" size="small" />
                  ) : (
                    <>
                      <Ionicons name="flash" size={24} color="white" />
                      <Text style={styles.startButtonText}>{t.beginReading}</Text>
                    </>
                  )}
                </LinearGradient>
              </TouchableOpacity>
            </View>
          ) : reading ? (
            <View style={styles.readingContainer}>
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

              {/* Back to Home Button */}
              <View style={styles.backButtonContainer}>
                <TouchableOpacity 
                  style={styles.backButton}
                  onPress={() => router.push('/')}
                  activeOpacity={0.7}
                >
                  <Ionicons name="arrow-back" size={20} color="white" />
                  <Text style={styles.backButtonText}>
                    {language === 'en' ? 'Home' : 'Ana Sayfa'}
                  </Text>
                </TouchableOpacity>
              </View>

              <Text style={styles.readingResultTitle}>
                {t.yourReading.replace('{readingName}', readingConfig.name)}
              </Text>
              
              <View style={styles.cardsDisplay}>
                {reading.cards.map((cardData, index) => renderCard(cardData, index))}
              </View>

              <View style={styles.interpretationContainer}>
                <Text style={styles.interpretationTitle}>{t.interpretation}</Text>
                <Text style={styles.interpretationText}>{reading.interpretation}</Text>
              </View>

              <TouchableOpacity
                style={styles.newReadingButton}
                onPress={() => {
                  setShowCards(false);
                  setReading(null);
                  setQuestion('');
                }}
              >
                <LinearGradient
                  colors={['#4A4A4A', '#2A2A2A']}
                  style={styles.newReadingButtonGradient}
                >
                  <Ionicons name="refresh" size={20} color="white" />
                  <Text style={styles.newReadingButtonText}>{t.newReading}</Text>
                </LinearGradient>
              </TouchableOpacity>
            </View>
          ) : null}
        </ScrollView>
      </LinearGradient>
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
  languageContainer: {
    alignItems: 'flex-end',
    paddingHorizontal: 20,
    paddingTop: 10,
  },
  languageButton: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: 'rgba(255,255,255,0.1)',
    paddingHorizontal: 12,
    paddingVertical: 6,
    borderRadius: 20,
  },
  languageText: {
    color: 'white',
    fontSize: 14,
    fontWeight: '600',
    marginLeft: 6,
  },
  backButtonContainer: {
    paddingHorizontal: 20,
    paddingTop: 10,
    paddingBottom: 10,
  },
  backButton: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: 'rgba(255,255,255,0.1)',
    paddingHorizontal: 16,
    paddingVertical: 10,
    borderRadius: 25,
    alignSelf: 'flex-start',
  },
  backButtonText: {
    color: 'white',
    fontSize: 14,
    fontWeight: '600',
    marginLeft: 8,
  },
  setupContainer: {
    flex: 1,
    padding: 20,
  },
  headerGradient: {
    padding: 24,
    borderRadius: 16,
    marginBottom: 30,
    alignItems: 'center',
  },
  readingTitle: {
    fontSize: 28,
    fontWeight: 'bold',
    color: 'white',
    textAlign: 'center',
    marginBottom: 12,
  },
  readingDescription: {
    fontSize: 16,
    color: 'rgba(255,255,255,0.9)',
    textAlign: 'center',
    lineHeight: 24,
  },
  questionContainer: {
    marginBottom: 30,
  },
  questionLabel: {
    fontSize: 18,
    color: 'white',
    marginBottom: 12,
    fontWeight: '600',
  },
  questionInput: {
    backgroundColor: 'rgba(255,255,255,0.1)',
    borderRadius: 12,
    padding: 16,
    color: 'white',
    fontSize: 16,
    minHeight: 100,
    borderWidth: 1,
    borderColor: 'rgba(255,255,255,0.2)',
  },
  startButton: {
    borderRadius: 16,
    overflow: 'hidden',
    elevation: 8,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.3,
    shadowRadius: 8,
  },
  startButtonGradient: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    padding: 18,
  },
  startButtonText: {
    color: 'white',
    fontSize: 18,
    fontWeight: '600',
    marginLeft: 8,
  },
  readingContainer: {
    padding: 20,
  },
  readingResultTitle: {
    fontSize: 24,
    fontWeight: 'bold',
    color: 'white',
    textAlign: 'center',
    marginBottom: 30,
  },
  cardsDisplay: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    justifyContent: 'center',
    marginBottom: 30,
  },
  cardContainer: {
    alignItems: 'center',
    margin: 8,
  },
  card: {
    width: CARD_WIDTH,
    height: CARD_HEIGHT,
    borderRadius: 12,
    overflow: 'hidden',
    elevation: 8,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.3,
    shadowRadius: 8,
  },
  cardReversed: {
    transform: [{ rotateX: '180deg' }],
  },
  cardGradient: {
    flex: 1,
    padding: 12,
    justifyContent: 'space-between',
    alignItems: 'center',
  },
  cardNumber: {
    fontSize: 16,
    color: 'rgba(255,255,255,0.7)',
    fontWeight: '600',
  },
  cardName: {
    fontSize: 12,
    color: 'white',
    textAlign: 'center',
    fontWeight: '500',
    lineHeight: 16,
  },
  reversedLabel: {
    fontSize: 10,
    color: '#FF6B6B',
    fontWeight: '600',
  },
  positionLabel: {
    fontSize: 12,
    color: 'rgba(255,255,255,0.8)',
    textAlign: 'center',
    marginTop: 8,
    fontWeight: '500',
  },
  interpretationContainer: {
    backgroundColor: 'rgba(255,255,255,0.05)',
    borderRadius: 16,
    padding: 20,
    marginBottom: 30,
  },
  interpretationTitle: {
    fontSize: 20,
    color: 'white',
    fontWeight: '600',
    marginBottom: 16,
    textAlign: 'center',
  },
  interpretationText: {
    fontSize: 14,
    color: 'rgba(255,255,255,0.9)',
    lineHeight: 22,
  },
  newReadingButton: {
    borderRadius: 12,
    overflow: 'hidden',
  },
  newReadingButtonGradient: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    padding: 16,
  },
  newReadingButtonText: {
    color: 'white',
    fontSize: 16,
    fontWeight: '600',
    marginLeft: 8,
  },
  errorText: {
    color: 'white',
    fontSize: 18,
    textAlign: 'center',
    marginTop: 50,
  },
});