import React, { useState, useEffect } from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  SafeAreaView,
  ActivityIndicator,
  Alert,
  Dimensions,
  TouchableOpacity,
} from 'react-native';
import { LinearGradient } from 'expo-linear-gradient';
import { Image as ExpoImage } from 'expo-image';
import { Image as RNImage } from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { useLocalSearchParams } from 'expo-router';
import Animated, { useSharedValue, useAnimatedStyle, withTiming, withSpring } from 'react-native-reanimated';
import { TapGestureHandler } from 'react-native-gesture-handler';
import * as Haptics from 'expo-haptics';
import { Audio } from 'expo-av';

const { width } = Dimensions.get('window');
const CARD_WIDTH = width * 0.4;
const CARD_HEIGHT = CARD_WIDTH * 1.5;

// Dil desteği
const translations = {
  en: {
    loading: "Loading card details...",
    error: "Error",
    errorMessage: "Failed to load card details. Please try again.",
    cardNotFound: "Card not found",
    keywords: "Keywords",
    description: "Description",
    uprightMeaning: "Upright Meaning",
    reversedMeaning: "Reversed Meaning",
    symbolism: "Symbolism",
    yesNoReading: "Yes/No Reading"
  },
  tr: {
    loading: "Kart detayları yükleniyor...",
    error: "Hata",
    errorMessage: "Kart detayları yüklenemedi. Lütfen tekrar deneyin.",
    cardNotFound: "Kart bulunamadı",
    keywords: "Anahtar Kelimeler",
    description: "Açıklama",
    uprightMeaning: "Düz Anlam",
    reversedMeaning: "Ters Anlam",
    symbolism: "Sembolizm",
    yesNoReading: "Evet/Hayır Falı"
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
  image_base64?: string | null;
}

export default function CardDetailScreen() {
  const { id } = useLocalSearchParams<{ id: string }>();
  const [card, setCard] = useState<TarotCard | null>(null);
  const [imageError, setImageError] = useState(false);
  const [loading, setLoading] = useState(true);
  const [language, setLanguage] = useState('tr'); // Varsayılan Türkçe
  const t = translations[language];

  const BACKEND_URL = process.env.EXPO_PUBLIC_BACKEND_URL;

  const toggleLanguage = () => {
    setLanguage(language === 'en' ? 'tr' : 'en');
  };

  useEffect(() => {
    if (id) {
      fetchCard();
    }
  }, [id, language]); // language değiştiğinde de yeniden yükle

  const fetchCard = async () => {
    try {
      const response = await fetch(`${BACKEND_URL}/api/cards/${id}?language=${language}&_=${Date.now()}`);
      if (!response.ok) {
        throw new Error('Failed to fetch card');
      }
      const cardData = await response.json();
      console.log('Card detail response', {
        id: cardData?.id,
        name: cardData?.name,
        hasImage: !!cardData?.image_base64,
        imagePrefix: cardData?.image_base64 ? cardData.image_base64.slice(0, 30) : null,
      });
      setImageError(false);
      setCard(cardData);
    } catch (error) {
      console.error('Error fetching card:', error);
      Alert.alert(t.error, t.errorMessage);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <SafeAreaView style={styles.container}>
        <LinearGradient colors={['#0a0a0a', '#1a1a2e', '#16213e']} style={styles.background}>
          <View style={styles.loadingContainer}>
            <ActivityIndicator size="large" color="#7C4DFF" />
            <Text style={styles.loadingText}>{t.loading}</Text>
          </View>
        </LinearGradient>
      </SafeAreaView>
    );
  }

  if (!card) {
    return (
      <SafeAreaView style={styles.container}>
        <LinearGradient colors={['#0a0a0a', '#1a1a2e', '#16213e']} style={styles.background}>
          <View style={styles.errorContainer}>
            <Ionicons name="alert-circle" size={64} color="#FF6B6B" />
            <Text style={styles.errorText}>{t.cardNotFound}</Text>
          </View>
        </LinearGradient>
      </SafeAreaView>
    );
  }

  return (
    <SafeAreaView style={styles.container}>
      <LinearGradient colors={['#0a0a0a', '#1a1a2e', '#16213e']} style={styles.background}>
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

          {/* Card Visual with Image */}
          <View style={styles.cardDisplay}>
            <View style={styles.card}>
              {card.image_base64 && !imageError ? (
                <View style={styles.cardImageWrapper}>
                  <ExpoImage
                    key={card.image_base64?.slice(0,20) || String(card.id)}
                    source={{ uri: card.image_base64 }}
                    style={styles.cardImage}
                    contentFit="cover"
                    transition={200}
                    onError={() => setImageError(true)}
                  />
                </View>
              ) : card.image_base64 && imageError ? (
                <View style={styles.cardImageWrapper}>
                  <RNImage
                    source={{ uri: card.image_base64 }}
                    style={styles.cardImage}
                    resizeMode="cover"
                    onError={() => setImageError(true)}
                  />
                </View>
              ) : (
                <LinearGradient
                  colors={['#2D1B69', '#1A1A2E']}
                  style={styles.cardGradient}
                >
                  <Text style={styles.cardNumber}>{card.id}</Text>
                  <Text style={styles.cardNameOnCard}>{card.name}</Text>
                </LinearGradient>
              )}
            </View>
          </View>

          {/* Card Information */}
          <View style={styles.content}>
            <Text style={styles.cardTitle}>{card.name}</Text>
            
            {/* Keywords */}
            <View style={styles.section}>
              <Text style={styles.sectionTitle}>{t.keywords}</Text>
              <View style={styles.keywordsContainer}>
                {card.keywords.map((keyword, index) => (
                  <View key={index} style={styles.keywordBadge}>
                    <Text style={styles.keywordText}>{keyword}</Text>
                  </View>
                ))}
              </View>
            </View>

            {/* Description */}
            <View style={styles.section}>
              <Text style={styles.sectionTitle}>{t.description}</Text>
              <Text style={styles.sectionText}>{card.description}</Text>
            </View>

            {/* Upright Meaning */}
            <View style={styles.section}>
              <View style={styles.meaningHeader}>
                <Ionicons name="arrow-up" size={20} color="#4CAF50" />
                <Text style={[styles.sectionTitle, { color: '#4CAF50' }]}>{t.uprightMeaning}</Text>
              </View>
              <Text style={styles.sectionText}>{card.meaning_upright}</Text>
            </View>

            {/* Reversed Meaning */}
            <View style={styles.section}>
              <View style={styles.meaningHeader}>
                <Ionicons name="arrow-down" size={20} color="#FF6B6B" />
                <Text style={[styles.sectionTitle, { color: '#FF6B6B' }]}>{t.reversedMeaning}</Text>
              </View>
              <Text style={styles.sectionText}>{card.meaning_reversed}</Text>
            </View>

            {/* Symbolism */}
            <View style={styles.section}>
              <Text style={styles.sectionTitle}>{t.symbolism}</Text>
              <Text style={styles.sectionText}>{card.symbolism}</Text>
            </View>

            {/* Yes/No Meaning */}
            <View style={styles.section}>
              <Text style={styles.sectionTitle}>{t.yesNoReading}</Text>
              <View style={styles.yesNoContainer}>
                <Text style={styles.sectionText}>{card.yes_no_meaning}</Text>
              </View>
            </View>
          </View>

          {/* Debug Panel (geçici) */}
          <View style={styles.debugPanel}>
            <Text style={styles.debugTitle}>Görsel Durumu (geçici tanılama)</Text>
            <Text style={styles.debugText}>hasImage: {card.image_base64 ? 'evet' : 'hayır'}</Text>
            <Text style={styles.debugText}>prefix: {card.image_base64 ? card.image_base64.slice(0, 30) + '…' : '-'}</Text>
            <Text style={styles.debugText}>imageError: {imageError ? 'evet' : 'hayır'}</Text>
            <TouchableOpacity
              onPress={() => { setImageError(false); fetchCard(); }}
              style={styles.debugButton}
              activeOpacity={0.7}
            >
              <Text style={styles.debugButtonText}>Görseli yeniden yükle</Text>
            </TouchableOpacity>
          </View>
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
  loadingContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
  loadingText: {
    color: 'rgba(255,255,255,0.7)',
    fontSize: 16,
    marginTop: 16,
  },
  errorContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
  errorText: {
    color: '#FF6B6B',
    fontSize: 18,
    marginTop: 16,
    textAlign: 'center',
  },
  cardDisplay: {
    alignItems: 'center',
    paddingVertical: 30,
  },
  card: {
    width: CARD_WIDTH,
    height: CARD_HEIGHT,
    borderRadius: 16,
    overflow: 'hidden',
    elevation: 12,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 6 },
    shadowOpacity: 0.4,
    shadowRadius: 12,
  },
  cardGradient: {
    flex: 1,
    padding: 16,
    justifyContent: 'space-between',
    alignItems: 'center',
  },
  cardImageWrapper: {
    flex: 1,
    borderRadius: 16,
    overflow: 'hidden',
    backgroundColor: '#0f0f15',
  },
  cardImage: {
    width: '100%',
    height: '100%',
  },
  cardNumber: {
    fontSize: 24,
    color: 'rgba(255,255,255,0.7)',
    fontWeight: 'bold',
  },
  cardNameOnCard: {
    fontSize: 16,
    color: 'white',
    textAlign: 'center',
    fontWeight: '600',
    lineHeight: 20,
  },
  content: {
    padding: 20,
  },
  cardTitle: {
    fontSize: 32,
    fontWeight: 'bold',
    color: '#FFFFFF',
    textAlign: 'center',
    marginBottom: 30,
  },
  section: {
    marginBottom: 24,
  },
  sectionTitle: {
    fontSize: 20,
    fontWeight: '600',
    color: '#FFFFFF',
    marginBottom: 12,
  },
  sectionText: {
    fontSize: 16,
    color: 'rgba(255,255,255,0.9)',
    lineHeight: 24,
  },
  keywordsContainer: {
    flexDirection: 'row',
    flexWrap: 'wrap',
  },
  keywordBadge: {
    backgroundColor: 'rgba(124, 77, 255, 0.2)',
    borderRadius: 16,
    paddingHorizontal: 12,
    paddingVertical: 6,
    marginRight: 8,
    marginBottom: 8,
  },
  keywordText: {
    color: '#9C88FF',
    fontSize: 14,
    fontWeight: '500',
  },
  meaningHeader: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 12,
  },
  yesNoContainer: {
    backgroundColor: 'rgba(255,255,255,0.05)',
    borderRadius: 12,
    padding: 16,
  },
});