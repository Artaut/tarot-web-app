// Dynamic require to avoid bundler error when native module isn't available
let TrackingTransparency: any = null;
try {
  TrackingTransparency = require('expo-tracking-transparency');
} catch (e) {
  TrackingTransparency = null;
}

export async function maybeAskATT() {
  try {
    if (!TrackingTransparency?.requestTrackingPermissionsAsync) {
      // ATT not available (Expo Go, Web, or module not installed)
      return false;
    }
    
    const { status } = await TrackingTransparency.requestTrackingPermissionsAsync();
    const trackingAllowed = status === 'granted';
    return trackingAllowed;
  } catch {
    return false;
  }
}