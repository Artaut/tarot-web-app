import { requestTrackingPermissionsAsync } from 'expo-tracking-transparency';

export async function maybeAskATT() {
  try {
    const { status } = await requestTrackingPermissionsAsync();
    const trackingAllowed = status === 'granted';
    return trackingAllowed;
  } catch {
    return false;
  }
}