import React from 'react';
import { 
  View, 
  Text, 
  StyleSheet, 
  ScrollView, 
  TouchableOpacity, 
  SafeAreaView,
  StatusBar,
  Alert,
  Dimensions
} from 'react-native';
import { Ionicons } from '@expo/vector-icons';

const { width, height } = Dimensions.get('window');

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
  const handlePress = (name: string) => {
    Alert.alert('Coming Soon!', `${name} feature will be available soon!`);
  };

  return (
    <SafeAreaView style={styles.container}>
      <StatusBar barStyle="light-content" backgroundColor="#0a0a0a" />
      
      <View style={styles.background}>
        <ScrollView showsVerticalScrollIndicator={false}>
          {/* Header */}
          <View style={styles.header}>
            <Text style={styles.title}>Daily Tarot</Text>
            <Text style={styles.subtitle}>Discover your destiny through the ancient wisdom of tarot</Text>
          </View>

          {/* Reading Types */}
          <View style={styles.readingsContainer}>
            <Text style={styles.sectionTitle}>Choose Your Reading</Text>
            
            {readingTypes.map((reading, index) => (
              <TouchableOpacity
                key={reading.id}
                style={[styles.readingCard, { backgroundColor: reading.color }]}
                onPress={() => handlePress(reading.name)}
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
                  
                  <Text style={styles.readingTitle}>{reading.name}</Text>
                  <Text style={styles.readingDescription}>{reading.description}</Text>
                  
                  <View style={styles.readingFooter}>
                    <Text style={styles.readingAction}>Tap to begin</Text>
                    <Ionicons name="arrow-forward" size={20} color="rgba(255,255,255,0.8)" />
                  </View>
                </View>
              </TouchableOpacity>
            ))}
          </View>

          {/* Additional Features */}
          <View style={styles.featuresContainer}>
            <Text style={styles.sectionTitle}>Learn & Explore</Text>
            
            <TouchableOpacity
              style={[styles.featureCard, { backgroundColor: '#5D4037' }]}
              onPress={() => handlePress('Card Meanings')}
              activeOpacity={0.7}
            >
              <Ionicons name="library" size={28} color="#FFAB91" />
              <View style={styles.featureTextContainer}>
                <Text style={styles.featureTitle}>Card Meanings</Text>
                <Text style={styles.featureDescription}>Explore the 22 Major Arcana cards and their meanings</Text>
              </View>
              <Ionicons name="chevron-forward" size={24} color="rgba(255,255,255,0.6)" />
            </TouchableOpacity>

            <TouchableOpacity
              style={[styles.featureCard, { backgroundColor: '#3F51B5' }]}
              onPress={() => handlePress('Tarot Quiz Game')}
              activeOpacity={0.7}
            >
              <Ionicons name="school" size={28} color="#8C9EFF" />
              <View style={styles.featureTextContainer}>
                <Text style={styles.featureTitle}>Tarot Quiz Game</Text>
                <Text style={styles.featureDescription}>Test your knowledge with 198 questions across 3 levels</Text>
              </View>
              <Ionicons name="chevron-forward" size={24} color="rgba(255,255,255,0.6)" />
            </TouchableOpacity>
          </View>

          {/* Footer */}
          <View style={styles.footer}>
            <Text style={styles.footerText}>
              Anticipate your future with the wisdom of the ancient Tarot
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