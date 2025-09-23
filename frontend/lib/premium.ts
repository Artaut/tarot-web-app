// Dynamic require to avoid bundler error when native module isn't available
let Purchases: any = null;
try {
  Purchases = require("react-native-purchases").default;
} catch (e) {
  // RevenueCat not available - create mock for web environment
  Purchases = {
    configure: async () => {},
    setLogLevel: async () => {},
    getCustomerInfo: async () => ({ entitlements: { active: {} } }),
    addCustomerInfoUpdateListener: () => ({ remove: () => {} }),
    getOfferings: async () => ({ current: null }),
    LOG_LEVEL: { VERBOSE: 'verbose' }
  };
}

import AsyncStorage from "@react-native-async-storage/async-storage";
import { useEffect, useState } from "react";
import 'react-native-get-random-values';
import { v4 as uuid } from "uuid";

const STORAGE_KEY = "appUserId";

export async function getOrCreateAppUserId() {
  let id = await AsyncStorage.getItem(STORAGE_KEY);
  if (!id) {
    id = uuid();
    await AsyncStorage.setItem(STORAGE_KEY, id);
  }
  return id;
}

export async function initRevenueCat(publicApiKey: string) {
  try {
    const appUserId = await getOrCreateAppUserId();
    await Purchases.configure({ apiKey: publicApiKey, appUserID: appUserId });
    if (__DEV__) {
      await Purchases.setLogLevel(Purchases.LOG_LEVEL.VERBOSE);
    }
    return appUserId;
  } catch (error) {
    // Gracefully handle initialization errors (e.g., in web environment)
    console.log('RevenueCat initialization skipped (not available in current environment)');
    return await getOrCreateAppUserId();
  }
}

export function useEntitlements() {
  const [loading, setLoading] = useState(true);
  const [isPremium, setIsPremium] = useState(false);
  const [hasNoAds, setHasNoAds] = useState(false);

  async function refresh() {
    try {
      const info = await Purchases.getCustomerInfo();
      setIsPremium(!!info.entitlements.active.premium);
      setHasNoAds(!!info.entitlements.active.no_ads);
    } catch (error) {
      // Default to non-premium in case of errors
      setIsPremium(false);
      setHasNoAds(false);
    }
  }

  useEffect(() => {
    (async () => { 
      try { 
        await refresh(); 
      } finally { 
        setLoading(false); 
      } 
    })();
    
    let listener: any = null;
    try {
      listener = Purchases.addCustomerInfoUpdateListener(refresh);
    } catch (error) {
      // Listener not available, that's okay
    }
    
    return () => listener?.remove?.();
  }, []);

  return { loading, isPremium, hasNoAds, refresh };
}

export type OfferingPick = {
  monthly?: any | null;
  annual?: any | null;
};

export async function loadOfferings(): Promise<OfferingPick> {
  try {
    const offerings = await Purchases.getOfferings();
    return {
      monthly: offerings.current?.monthly ?? null,
      annual: offerings.current?.annual ?? null,
    };
  } catch (error) {
    // Return empty offerings if not available
    return {
      monthly: null,
      annual: null,
    };
  }
}