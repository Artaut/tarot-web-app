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

const DIFFICULTY_LEVELS = [
  {
    id: 'beginner',
    name: 'Beginner',
    description: 'Learn the basics of the Major Arcana',
    questions: 66,
    color: ['#4CAF50', '#388E3C'],
    icon: 'school-outline' as keyof typeof Ionicons.glyphMap,
  },
  {
    id: 'intermediate',
    name: 'Intermediate',
    description: 'Test your knowledge of card meanings',
    questions: 66,
    color: ['#FF9800', '#F57C00'],
    icon: 'library-outline' as keyof typeof Ionicons.glyphMap,
  },
  {
    id: 'advanced',
    name: 'Advanced',
    description: 'Master the deep symbolism and interpretations',
    questions: 66,
    color: ['#F44336', '#D32F2F'],
    icon: 'flash-outline' as keyof typeof Ionicons.glyphMap,
  },
];

export default function QuizScreen() {
  const handleDifficultySelect = (difficulty: string) => {
    Alert.alert(
      'Quiz Feature',
      `The ${difficulty} quiz with 198 questions across 3 difficulty levels is coming soon! This will help you master the 22 Major Arcana cards.`,
      [{ text: 'OK', style: 'default' }]
    );
  };

  return (
    <SafeAreaView style={styles.container}>
      <LinearGradient colors={['#0a0a0a', '#1a1a2e', '#16213e']} style={styles.background}>
        <ScrollView showsVerticalScrollIndicator={false}>
          {/* Header */}
          <View style={styles.header}>
            <View style={styles.iconContainer}>
              <Ionicons name="school" size={48} color="#9C88FF" />
            </View>
            <Text style={styles.title}>Tarot Quiz Game</Text>
            <Text style={styles.subtitle}>
              Master the 22 Major Arcana with 198 questions across 3 levels of difficulty
            </Text>
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
                  <Text style={styles.infoText}>198 Questions Total</Text>
                </View>
                <View style={styles.infoRow}>
                  <Ionicons name="layers" size={24} color="#9C88FF" />
                  <Text style={styles.infoText}>3 Difficulty Levels</Text>
                </View>
                <View style={styles.infoRow}>
                  <Ionicons name="star" size={24} color="#9C88FF" />
                  <Text style={styles.infoText}>22 Major Arcana Cards</Text>
                </View>
              </LinearGradient>
            </View>
          </View>

          {/* Difficulty Levels */}
          <View style={styles.levelsContainer}>
            <Text style={styles.sectionTitle}>Choose Your Level</Text>
            
            {DIFFICULTY_LEVELS.map((level, index) => (
              <TouchableOpacity
                key={level.id}
                style={styles.levelCard}
                onPress={() => handleDifficultySelect(level.name)}
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
                    
                    <Text style={styles.levelTitle}>{level.name}</Text>
                    <Text style={styles.levelDescription}>{level.description}</Text>
                    
                    <View style={styles.levelFooter}>
                      <Text style={styles.levelAction}>Start Quiz</Text>
                      <Ionicons name="arrow-forward" size={20} color="rgba(255,255,255,0.8)" />
                    </View>
                  </View>
                </LinearGradient>
              </TouchableOpacity>
            ))}
          </View>

          {/* Learning Tips */}
          <View style={styles.tipsContainer}>
            <Text style={styles.sectionTitle}>Learning Tips</Text>
            
            <View style={styles.tipCard}>
              <LinearGradient
                colors={['rgba(255, 255, 255, 0.05)', 'rgba(255, 255, 255, 0.02)']}
                style={styles.tipCardGradient}
              >
                <View style={styles.tipRow}>
                  <Ionicons name="bulb" size={20} color="#FFD700" />
                  <Text style={styles.tipText}>
                    Start with the Card Meanings section to familiarize yourself with each card
                  </Text>
                </View>
                
                <View style={styles.tipRow}>
                  <Ionicons name="refresh" size={20} color="#4CAF50" />
                  <Text style={styles.tipText}>
                    Practice different reading types to understand card contexts
                  </Text>
                </View>
                
                <View style={styles.tipRow}>
                  <Ionicons name="trending-up" size={20} color="#2196F3" />
                  <Text style={styles.tipText}>
                    Progress through difficulty levels gradually for best results
                  </Text>
                </View>
              </LinearGradient>
            </View>
          </View>

          {/* Footer */}
          <View style={styles.footer}>
            <Text style={styles.footerText}>
              Learn while you play! Master the ancient art of Tarot reading.
            </Text>
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