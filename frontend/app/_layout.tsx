import { Stack } from 'expo-router';
import { StatusBar } from 'expo-status-bar';

export default function RootLayout() {
  return (
    <>
      <StatusBar style="light" backgroundColor="#0a0a0a" />
      <Stack
        screenOptions={{
          headerStyle: {
            backgroundColor: '#0a0a0a',
          },
          headerTintColor: '#fff',
          headerTitleStyle: {
            fontWeight: 'bold',
          },
        }}
      >
        <Stack.Screen 
          name="index" 
          options={{ 
            title: 'Daily Tarot',
            headerShown: false 
          }} 
        />
        <Stack.Screen 
          name="reading/[type]" 
          options={{ 
            title: 'Tarot Reading',
            headerBackTitle: 'Back'
          }} 
        />
        <Stack.Screen 
          name="cards/index" 
          options={{ 
            title: 'Card Meanings',
            headerBackTitle: 'Back'
          }} 
        />
        <Stack.Screen 
          name="cards/[id]" 
          options={{ 
            title: 'Card Details',
            headerBackTitle: 'Back'
          }} 
        />
        <Stack.Screen 
          name="quiz/index" 
          options={{ 
            title: 'Tarot Quiz',
            headerBackTitle: 'Back'
          }} 
        />
      </Stack>
    </>
  );
}