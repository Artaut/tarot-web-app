import React, { useState, useEffect } from 'react';
import {
  View,
  Text,
  StyleSheet,
  FlatList,
  TouchableOpacity,
  SafeAreaView,
  ActivityIndicator,
  Alert,
} from 'react-native';
import { LinearGradient } from 'expo-linear-gradient';
import { Image as ExpoImage } from 'expo-image';
import { Ionicons } from '@expo/vector-icons';
import { router } from 'expo-router';

// Dil desteği
const translations = {
  en: {
    title: "Major Arcana",
    subtitle: "The 22 cards representing life's major themes and lessons",
    loading: "Loading Major Arcana Cards...",
    error: "Error",
    errorMessage: "Failed to load tarot cards. Please try again."
  },
  tr: {
    title: "Büyük Arkana",
    subtitle: "Hayatın ana temalarını ve derslerini temsil eden 22 kart",
    loading: "Büyük Arkana Kartları Yükleniyor...",
    error: "Hata",
    errorMessage: "Tarot kartları yüklenemedi. Lütfen tekrar deneyin."
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

export default function CardsListScreen() {
  const [cards, setCards] = useState<TarotCard[]>([]);
  const [loading, setLoading] = useState(true);
  const [language, setLanguage] = useState('tr'); // Varsayılan Türkçe
  const t = translations[language];

  const BACKEND_URL = process.env.EXPO_PUBLIC_BACKEND_URL;

  const toggleLanguage = () => {
    setLanguage(language === 'en' ? 'tr' : 'en');
  };

  useEffect(() => {
    fetchCards();
  }, [language]); // language değiştiğinde kartları yeniden yükle

  const fetchCards = async () => {
    try {
      const response = await fetch(`${BACKEND_URL}/api/cards?language=${language}`);
      if (!response.ok) {
        throw new Error('Failed to fetch cards');
      }
      const cardsData = await response.json();
      setCards(cardsData);
    } catch (error) {
      console.error('Error fetching cards:', error);
      Alert.alert(t.error, t.errorMessage);
    } finally {
      setLoading(false);
    }
  };

  const getCardImageUrl = (id: number) => `${BACKEND_URL}/api/cards/${id}/image`;

  const fetchCards_real = async () => {
    try {
      const response = await fetch(`${BACKEND_URL}/api/cards?language=${language}`);
      if (!response.ok) {
        throw new Error('Failed to fetch cards');
      }
      const cardsData = await response.json();
      setCards(cardsData);
    } catch (error) {
      console.error('Error fetching cards:', error);
      Alert.alert(t.error, t.errorMessage);
    } finally {
      setLoading(false);
    }
  };

  const handleCardPress = (card: TarotCard) => {
    router.push(`/cards/${card.id}`);
  };

  const renderCard = ({ item }: { item: TarotCard }) => (
    <TouchableOpacity
      style={styles.cardItem}
      onPress={() => handleCardPress(item)}
      activeOpacity={0.7}
    >
      <LinearGradient
        colors={['#2D1B69', '#1A1A2E', '#0F0F23']}
        style={styles.cardGradient}
        start={{ x: 0, y: 0 }}
        end={{ x: 1, y: 1 }}
      >
        <View style={styles.cardHeader}>
          <View style={styles.cardNumberContainer}>
            <Text style={styles.cardNumber}>{item.id}</Text>
          </View>
          <Ionicons name="chevron-forward" size={24} color="rgba(255,255,255,0.6)" />
        </View>
        
        <Text style={styles.cardName}>{item.name}</Text>
        
        <View style={styles.keywordsContainer}>
          {item.keywords.slice(0, 3).map((keyword, index) => (
            <View key={index} style={styles.keywordBadge}>
              <Text style={styles.keywordText}>{keyword}</Text>
            </View>
          ))}
        </View>
        
        <Text style={styles.cardDescription} numberOfLines={2}>
          {item.description}
        </Text>
      </LinearGradient>
    </TouchableOpacity>
  );

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

  return (
    <SafeAreaView style={styles.container}>
      <LinearGradient colors={['#0a0a0a', '#1a1a2e', '#16213e']} style={styles.background}>
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

        <View style={styles.header}>
          <Text style={styles.title}>{t.title}</Text>
          <Text style={styles.subtitle}>{t.subtitle}</Text>
        </View>
        
        <FlatList
          data={cards}
          renderItem={renderCard}
          keyExtractor={(item) => item.id.toString()}
          contentContainerStyle={styles.listContainer}
          showsVerticalScrollIndicator={false}
        />
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
  header: {
    padding: 20,
    alignItems: 'center',
  },
  title: {
    fontSize: 28,
    fontWeight: 'bold',
    color: '#FFFFFF',
    textAlign: 'center',
    marginBottom: 8,
  },
  subtitle: {
    fontSize: 16,
    color: 'rgba(255,255,255,0.7)',
    textAlign: 'center',
    lineHeight: 24,
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
  listContainer: {
    paddingHorizontal: 20,
    paddingBottom: 20,
  },
  cardItem: {
    marginBottom: 16,
    borderRadius: 16,
    overflow: 'hidden',
    elevation: 8,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.3,
    shadowRadius: 8,
  },
  cardGradient: {
    padding: 20,
  },
  cardHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 12,
  },
  cardNumberContainer: {
    backgroundColor: 'rgba(255,255,255,0.1)',
    borderRadius: 20,
    paddingHorizontal: 12,
    paddingVertical: 6,
  },
  cardNumber: {
    color: 'white',
    fontSize: 14,
    fontWeight: '600',
  },
  cardName: {
    fontSize: 22,
    fontWeight: 'bold',
    color: '#FFFFFF',
    marginBottom: 12,
  },
  keywordsContainer: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    marginBottom: 12,
  },
  keywordBadge: {
    backgroundColor: 'rgba(124, 77, 255, 0.2)',
    borderRadius: 12,
    paddingHorizontal: 8,
    paddingVertical: 4,
    marginRight: 8,
    marginBottom: 4,
  },
  keywordText: {
    color: '#9C88FF',
    fontSize: 12,
    fontWeight: '500',
  },
  cardDescription: {
    fontSize: 14,
    color: 'rgba(255,255,255,0.8)',
    lineHeight: 20,
  },
});