import { Slot } from 'expo-router';
import { StatusBar } from 'expo-status-bar';
import { useEffect } from 'react';
import { Platform } from 'react-native';
import { initRevenueCat } from '@/lib/premium';

// RevenueCat API Keys (Test keys - replace with actual keys for production)
const REVENUECAT_API_KEY_IOS = "appl_your_ios_key_here";
const REVENUECAT_API_KEY_ANDROID = "goog_your_android_key_here";

export default function RootLayout() {
  useEffect(() => {
    async function initializeApp() {
      try {
        // Initialize RevenueCat based on platform
        const apiKey = Platform.OS === 'ios' ? REVENUECAT_API_KEY_IOS : REVENUECAT_API_KEY_ANDROID;
        await initRevenueCat(apiKey);
        console.log('RevenueCat initialized successfully');
      } catch (error) {
        console.log('RevenueCat initialization skipped or failed:', error);
        // This is expected in development/web environments
      }
    }

    initializeApp();
  }, []);

  return (
    <>
      <StatusBar style="light" backgroundColor="#0a0a0a" />
      <Slot />
    </>
  );
}