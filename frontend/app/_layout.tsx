import { View } from 'react-native';
import { StatusBar } from 'expo-status-bar';

export default function RootLayout() {
  return (
    <>
      <StatusBar style="light" backgroundColor="#0a0a0a" />
      <View style={{ flex: 1 }}>
        {/* Children will be rendered here */}
      </View>
    </>
  );
}