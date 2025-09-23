import { Slot } from 'expo-router';
import { StatusBar } from 'expo-status-bar';
import { useEffect } from 'react';
// import { maybeAskATT } from '@/lib/att'; // Temporarily disabled for web preview

export default function RootLayout() {
  useEffect(() => {
    // ATT temporarily disabled for development
    // maybeAskATT();
  }, []);

  return (
    <>
      <StatusBar style="light" backgroundColor="#0a0a0a" />
      <Slot />
    </>
  );
}