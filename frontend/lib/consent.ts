import { Consent, ConsentStatus, ConsentForm } from "react-native-google-mobile-ads/consent";

export async function initConsent() {
  await Consent.requestInfoUpdate({});
  let status = await Consent.getConsentStatus();
  if (status === ConsentStatus.REQUIRED) {
    const form = await ConsentForm.load();
    await form.show();
    status = await Consent.getConsentStatus();
  }
  const personalized = (status === ConsentStatus.OBTAINED);
  return { personalized };
}