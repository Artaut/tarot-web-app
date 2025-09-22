import React, { useState } from 'react';
import {
  View,
  Text,
  StyleSheet,
  TouchableOpacity,
  SafeAreaView,
  ScrollView,
  Alert,
} from 'react-native';
import { LinearGradient } from 'expo-linear-gradient';
import { Ionicons } from '@expo/vector-icons';

// Dil desteği
const translations = {
  en: {
    title: "Tarot Quiz Game",
    subtitle: "Master the 22 Major Arcana with 198 questions across 3 levels of difficulty",
    questionsTotal: "198 Questions Total",
    difficultyLevels: "3 Difficulty Levels", 
    majorArcanaCards: "22 Major Arcana Cards",
    chooseLevel: "Choose Your Level",
    learningTips: "Learning Tips",
    footerText: "Learn while you play! Master the ancient art of Tarot reading.",
    startQuiz: "Start Quiz",
    comingSoon: "Quiz Feature",
    comingSoonMessage: "The {difficulty} quiz with 198 questions across 3 difficulty levels is coming soon! This will help you master the 22 Major Arcana cards.",
    levels: {
      beginner: {
        name: "Beginner",
        description: "Learn the basics of the Major Arcana"
      },
      intermediate: {
        name: "Intermediate", 
        description: "Test your knowledge of card meanings"
      },
      advanced: {
        name: "Advanced",
        description: "Master the deep symbolism and interpretations"
      }
    },
    tips: [
      "Start with the Card Meanings section to familiarize yourself with each card",
      "Practice different reading types to understand card contexts",
      "Progress through difficulty levels gradually for best results"
    ]
  },
  tr: {
    title: "Tarot Quiz Oyunu",
    subtitle: "3 zorluk seviyesinde 198 soru ile 22 Büyük Arkana'yı öğrenin",
    questionsTotal: "Toplam 198 Soru",
    difficultyLevels: "3 Zorluk Seviyesi",
    majorArcanaCards: "22 Büyük Arkana Kartı", 
    chooseLevel: "Seviyenizi Seçin",
    learningTips: "Öğrenme İpuçları",
    footerText: "Oynarken öğrenin! Kadim Tarot okuma sanatında ustalaşın.",
    startQuiz: "Quiz'e Başla",
    comingSoon: "Quiz Özelliği",
    comingSoonMessage: "{difficulty} seviyesindeki 198 soruluk quiz yakında geliyor! Bu özellik 22 Büyük Arkana kartını öğrenmenize yardımcı olacak.",
    levels: {
      beginner: {
        name: "Başlangıç",
        description: "Büyük Arkana'nın temellerini öğrenin"
      },
      intermediate: {
        name: "Orta Seviye",
        description: "Kart anlamları bilginizi test edin"
      },
      advanced: {
        name: "İleri Seviye", 
        description: "Derin sembolizm ve yorumlamalarda ustalaşın"
      }
    },
    tips: [
      "Her kartı tanımak için önce Kart Anlamları bölümüyle başlayın",
      "Kart bağlamlarını anlamak için farklı fal türlerini deneyin",
      "En iyi sonuçlar için zorluk seviyelerinde kademeli olarak ilerleyin"
    ]
  }
};

const DIFFICULTY_LEVELS = [
  {
    id: 'beginner',
    questions: 66,
    color: ['#4CAF50', '#388E3C'],
    icon: 'school-outline' as keyof typeof Ionicons.glyphMap,
  },
  {
    id: 'intermediate', 
    questions: 66,
    color: ['#FF9800', '#F57C00'],
    icon: 'library-outline' as keyof typeof Ionicons.glyphMap,
  },
  {
    id: 'advanced',
    questions: 66,
    color: ['#F44336', '#D32F2F'],
    icon: 'flash-outline' as keyof typeof Ionicons.glyphMap,
  },
];

export default function QuizScreen() {
  const [language, setLanguage] = useState('tr'); // Varsayılan Türkçe
  const t = translations[language];

  const toggleLanguage = () => {
    setLanguage(language === 'en' ? 'tr' : 'en');
  };

  const handleDifficultySelect = (difficultyId: string) => {
    const difficultyName = t.levels[difficultyId as keyof typeof t.levels].name;
    Alert.alert(
      t.comingSoon,
      t.comingSoonMessage.replace('{difficulty}', difficultyName),
      [{ text: 'OK', style: 'default' }]
    );
  };

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

          {/* Header */}
          <View style={styles.header}>
            <View style={styles.iconContainer}>
              <Ionicons name="school" size={48} color="#9C88FF" />
            </View>
            <Text style={styles.title}>{t.title}</Text>
            <Text style={styles.subtitle}>{t.subtitle}</Text>
          </View>

          {/* Quiz Info */}
          <View style={styles.infoContainer}>
            <View style={styles.infoCard}>
              <LinearGradient
                colors={['rgba(156, 136, 255, 0.1)', 'rgba(124, 77, 255, 0.1)']}
                style={styles.infoCardGradient}
              >
                <View style={styles.infoRow}>
                  <Ionicons name="help-circle" size={24} color="#9C88FF" />
                  <Text style={styles.infoText}>{t.questionsTotal}</Text>
                </View>
                <View style={styles.infoRow}>
                  <Ionicons name="layers" size={24} color="#9C88FF" />
                  <Text style={styles.infoText}>{t.difficultyLevels}</Text>
                </View>
                <View style={styles.infoRow}>
                  <Ionicons name="star" size={24} color="#9C88FF" />
                  <Text style={styles.infoText}>{t.majorArcanaCards}</Text>
                </View>
              </LinearGradient>
            </View>
          </View>

          {/* Difficulty Levels */}
          <View style={styles.levelsContainer}>
            <Text style={styles.sectionTitle}>{t.chooseLevel}</Text>
            
            {DIFFICULTY_LEVELS.map((level, index) => (
              <TouchableOpacity
                key={level.id}
                style={styles.levelCard}
                onPress={() => handleDifficultySelect(level.id)}
                activeOpacity={0.7}
              >
                <LinearGradient
                  colors={level.color}
                  style={styles.levelCardGradient}
                  start={{ x: 0, y: 0 }}
                  end={{ x: 1, y: 1 }}
                >
                  <View style={styles.levelCardContent}>
                    <View style={styles.levelHeader}>
                      <Ionicons 
                        name={level.icon} 
                        size={32} 
                        color="white" 
                        style={styles.levelIcon}
                      />
                      <View style={styles.questionsBadge}>
                        <Text style={styles.questionsText}>{level.questions} Q</Text>
                      </View>
                    </View>
                    
                    <Text style={styles.levelTitle}>
                      {t.levels[level.id as keyof typeof t.levels].name}
                    </Text>
                    <Text style={styles.levelDescription}>
                      {t.levels[level.id as keyof typeof t.levels].description}
                    </Text>
                    
                    <View style={styles.levelFooter}>
                      <Text style={styles.levelAction}>{t.startQuiz}</Text>
                      <Ionicons name="arrow-forward" size={20} color="rgba(255,255,255,0.8)" />
                    </View>
                  </View>
                </LinearGradient>
              </TouchableOpacity>
            ))}
          </View>

          {/* Learning Tips */}
          <View style={styles.tipsContainer}>
            <Text style={styles.sectionTitle}>{t.learningTips}</Text>
            
            <View style={styles.tipCard}>
              <LinearGradient
                colors={['rgba(255, 255, 255, 0.05)', 'rgba(255, 255, 255, 0.02)']}
                style={styles.tipCardGradient}
              >
                {t.tips.map((tip, index) => (
                  <View key={index} style={styles.tipRow}>
                    <Ionicons 
                      name={index === 0 ? "bulb" : index === 1 ? "refresh" : "trending-up"} 
                      size={20} 
                      color={index === 0 ? "#FFD700" : index === 1 ? "#4CAF50" : "#2196F3"} 
                    />
                    <Text style={styles.tipText}>{tip}</Text>
                  </View>
                ))}
              </LinearGradient>
            </View>
          </View>

          {/* Footer */}
          <View style={styles.footer}>
            <Text style={styles.footerText}>{t.footerText}</Text>
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
  header: {
    padding: 20,
    alignItems: 'center',
  },
  iconContainer: {
    marginBottom: 16,
  },
  title: {
    fontSize: 28,
    fontWeight: 'bold',
    color: '#FFFFFF',
    textAlign: 'center',
    marginBottom: 12,
  },
  subtitle: {
    fontSize: 16,
    color: 'rgba(255,255,255,0.7)',
    textAlign: 'center',
    lineHeight: 24,
    paddingHorizontal: 20,
  },
  infoContainer: {
    paddingHorizontal: 20,
    marginBottom: 30,
  },
  infoCard: {
    borderRadius: 16,
    overflow: 'hidden',
  },
  infoCardGradient: {
    padding: 20,
  },
  infoRow: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 12,
  },
  infoText: {
    fontSize: 16,
    color: 'white',
    marginLeft: 12,
    fontWeight: '500',
  },
  levelsContainer: {
    paddingHorizontal: 20,
    marginBottom: 30,
  },
  sectionTitle: {
    fontSize: 22,
    fontWeight: '600',
    color: '#FFFFFF',
    marginBottom: 20,
    textAlign: 'center',
  },
  levelCard: {
    marginBottom: 16,
    borderRadius: 16,
    overflow: 'hidden',
    elevation: 8,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.3,
    shadowRadius: 8,
  },
  levelCardGradient: {
    padding: 20,
  },
  levelCardContent: {
    flex: 1,
  },
  levelHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 12,
  },
  levelIcon: {
    marginRight: 12,
  },
  questionsBadge: {
    backgroundColor: 'rgba(255,255,255,0.2)',
    borderRadius: 12,
    paddingHorizontal: 8,
    paddingVertical: 4,
  },
  questionsText: {
    color: 'white',
    fontSize: 12,
    fontWeight: '600',
  },
  levelTitle: {
    fontSize: 20,
    fontWeight: 'bold',
    color: '#FFFFFF',
    marginBottom: 8,
  },
  levelDescription: {
    fontSize: 14,
    color: 'rgba(255,255,255,0.9)',
    lineHeight: 20,
    marginBottom: 16,
  },
  levelFooter: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
  },
  levelAction: {
    fontSize: 14,
    color: 'rgba(255,255,255,0.8)',
    fontWeight: '500',
  },
  tipsContainer: {
    paddingHorizontal: 20,
    marginBottom: 30,
  },
  tipCard: {
    borderRadius: 12,
    overflow: 'hidden',
  },
  tipCardGradient: {
    padding: 20,
  },
  tipRow: {
    flexDirection: 'row',
    alignItems: 'flex-start',
    marginBottom: 16,
  },
  tipText: {
    fontSize: 14,
    color: 'rgba(255,255,255,0.8)',
    marginLeft: 12,
    flex: 1,
    lineHeight: 20,
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