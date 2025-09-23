// App Tracking Transparency (ATT) for iOS
// Dynamic require to avoid bundler error when native module isn't available

let TrackingTransparency: any = null;
try {
  TrackingTransparency = require('expo-tracking-transparency');
} catch (e) {
  // Module not available - this is expected in Expo Go/Web
  TrackingTransparency = null;
}

export async function maybeAskATT(): Promise<boolean> {
  try {
    if (!TrackingTransparency?.requestTrackingPermissionsAsync) {
      // ATT not available (Expo Go, Web, or module not installed)
      return false;
    }
    
    const { status } = await TrackingTransparency.requestTrackingPermissionsAsync();
    const trackingAllowed = status === 'granted';
    return trackingAllowed;
  } catch (error) {
    // Gracefully handle any errors
    return false;
  }
}