// frontend/lib/premium.ts
import { Platform } from 'react-native';
import { useEffect, useState } from 'react';
import AsyncStorage from "@react-native-async-storage/async-storage";
import 'react-native-get-random-values';
import { v4 as uuid } from "uuid";
import { rcAvailable, rcConfigure, rcGetCustomerInfo, rcGetOfferings } from '@/lib/rc';

const STORAGE_KEY = "appUserId";
let _started = false;

export async function getOrCreateAppUserId() {
  let id = await AsyncStorage.getItem(STORAGE_KEY);
  if (!id) {
    id = uuid();
    await AsyncStorage.setItem(STORAGE_KEY, id);
  }
  return id;
}

export async function initRevenueCat() {
  if (_started) return;

  const apiKey = Platform.select({
    android: process.env.EXPO_PUBLIC_RC_ANDROID_KEY,
    ios: process.env.EXPO_PUBLIC_RC_IOS_KEY,
    default: null,
  }) as string | null;

  // Web veya anahtar yoksa sessizce geç
  if (!apiKey || !rcAvailable) return;

  _started = true;
  try {
    const appUserId = await getOrCreateAppUserId();
    await rcConfigure({ apiKey, appUserID: appUserId });
  } catch (err) {
    _started = false;
    if (typeof __DEV__ !== "undefined" && __DEV__) {
      console.warn("RevenueCat initialization failed", err);
    }
  }
}

export function useEntitlements() {
  const [state, setState] = useState({
    loading: true,
    isPremium: false,
    hasNoAds: false,
    error: null as string | null,
  });

  useEffect(() => {
    let alive = true;
    (async () => {
      try {
        await initRevenueCat();
        if (!rcAvailable) {
          if (alive) setState({ loading: false, isPremium: false, hasNoAds: false, error: null });
          return;
        }
        const info = await rcGetCustomerInfo();
        const ent = info?.entitlements?.active ?? {};
        const isPremium = !!ent['premium'];
        const hasNoAds = !!ent['no_ads'] || isPremium;
        if (alive) setState({ loading: false, isPremium, hasNoAds, error: null });
      } catch (e: any) {
        if (alive) setState({ loading: false, isPremium: false, hasNoAds: false, error: String(e?.message ?? e) });
      }
    })();
    return () => { alive = false; };
  }, []);

  return state;
}

export type OfferingPick = {
  monthly?: any | null;
  annual?: any | null;
};

function pickPackageByType(packages: any[] | undefined | null, packageType: string) {
  if (!Array.isArray(packages)) return null;
  return packages.find((pkg) => pkg?.packageType === packageType) ?? null;
}

function pickPackageFromOffering(offering: any, packageType: string) {
  if (!offering) return null;
  const directKey = packageType.toLowerCase();
  return (
    offering?.[directKey] ??
    pickPackageByType(offering?.availablePackages, packageType) ??
    pickPackageByType(offering?.packages, packageType)
  );
}

function collectOfferings(offerings: any) {
  if (!offerings?.all) return [] as any[];
  const all = offerings.all as Record<string, any>;
  return Object.values(all).filter(Boolean);
}

function isOfferingPick(value: any): value is OfferingPick {
  if (!value || typeof value !== "object") return false;
  return "monthly" in value || "annual" in value;
}

function findPackage(offerings: any, packageType: string) {
  const fromCurrent = pickPackageFromOffering(offerings?.current, packageType);
  if (fromCurrent) return fromCurrent;

  for (const offering of collectOfferings(offerings)) {
    const pkg = pickPackageFromOffering(offering, packageType);
    if (pkg) return pkg;
  }

  return (
    pickPackageByType(offerings?.availablePackages, packageType) ??
    pickPackageByType(offerings?.packages, packageType)
  );
}

export function normalizeOfferingPick(offerings: any): OfferingPick {
  if (!offerings) return { monthly: null, annual: null };
  if (isOfferingPick(offerings)) {
    return {
      monthly: offerings.monthly ?? null,
      annual: offerings.annual ?? null,
    };
  }

  const monthly = findPackage(offerings, "MONTHLY");
  const annual = findPackage(offerings, "ANNUAL");

  return { monthly: monthly ?? null, annual: annual ?? null };
}

export async function loadOfferings(): Promise<OfferingPick | null> {
  await initRevenueCat();
  if (!rcAvailable) return null;

  try {
    const offerings: any = await rcGetOfferings();
    return normalizeOfferingPick(offerings);
  } catch (err) {
    if (typeof __DEV__ !== "undefined" && __DEV__) {
      console.warn("RevenueCat offerings failed", err);
    }
    return { monthly: null, annual: null };
  }
}
