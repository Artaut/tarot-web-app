// frontend/lib/rc.ts
import { Platform } from 'react-native';

type RNPurchases = typeof import('react-native-purchases');
let Purchases: RNPurchases["default"] | null = null;

try {
  if (Platform.OS !== 'web') {
    // Native ortamda dinamik yükle, web'de hiç yükleme
    Purchases = require('react-native-purchases').default;
  }
} catch (_) {
  Purchases = null;
}

export const rcAvailable = !!Purchases && Platform.OS !== 'web';

export async function rcConfigure(opts: { apiKey?: string | null; appUserID?: string | null }) {
  if (!rcAvailable || !opts.apiKey) return;
  const { LOG_LEVEL } = require('react-native-purchases');
  (Purchases as any).setLogLevel?.(LOG_LEVEL?.WARN ?? 2);
  await (Purchases as any).configure?.({
    apiKey: opts.apiKey,
    appUserID: opts.appUserID ?? undefined,
  });
}

export async function rcGetCustomerInfo() {
  if (!rcAvailable) return null;
  return (Purchases as any).getCustomerInfo();
}

export async function rcGetOfferings() {
  if (!rcAvailable) return null;
  return (Purchases as any).getOfferings();
}

export async function rcPurchasePackage(pkg: any) {
  if (!rcAvailable) throw new Error('Purchases not available on this platform');
  return (Purchases as any).purchasePackage(pkg);
}

export async function rcRestorePurchases() {
  if (!rcAvailable) return null;
  return (Purchases as any).restorePurchases();
}