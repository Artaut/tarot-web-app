import { Slot } from 'expo-router';
import { StatusBar } from 'expo-status-bar';
import { useEffect } from 'react';
import { initRevenueCat } from '@/lib/premium';

export default function RootLayout() {
  useEffect(() => {
    // Erken RevenueCat initialization
    initRevenueCat().catch(err => console.warn('[RC init]', err));
  }, []);

  return (
    <>
      <StatusBar style="light" backgroundColor="#0a0a0a" />
      <Slot />
    </>
  );
}