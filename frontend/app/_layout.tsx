import { Slot } from 'expo-router';
import { StatusBar } from 'expo-status-bar';
import { useEffect } from 'react';
import { maybeAskATT } from '@/lib/att';

export default function RootLayout() {
  useEffect(() => {
    // Kısa bir bilgilendirme UI'ından sonra çağırabilirsiniz
    maybeAskATT();
  }, []);

  return (
    <>
      <StatusBar style="light" backgroundColor="#0a0a0a" />
      <Slot />
    </>
  );
}