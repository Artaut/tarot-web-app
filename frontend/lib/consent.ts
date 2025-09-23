// Dynamic require to avoid bundler error when native module isn't available
let ConsentMod: any = null;
try {
  ConsentMod = require("react-native-google-mobile-ads/consent");
} catch (e) {
  ConsentMod = null;
}

const Consent = ConsentMod?.Consent ?? {
  requestInfoUpdate: async () => {},
  getConsentStatus: async () => 'obtained'
};

const ConsentStatus = ConsentMod?.ConsentStatus ?? {
  REQUIRED: 'required',
  OBTAINED: 'obtained'
};

const ConsentForm = ConsentMod?.ConsentForm ?? {
  load: async () => ({ show: async () => {} })
};

export async function initConsent() {
  try {
    await Consent.requestInfoUpdate({});
    let status = await Consent.getConsentStatus();
    if (status === ConsentStatus.REQUIRED) {
      const form = await ConsentForm.load();
      await form.show();
      status = await Consent.getConsentStatus();
    }
    const personalized = (status === ConsentStatus.OBTAINED);
    return { personalized };
  } catch (error) {
    // Fallback: assume consent obtained for non-native environments
    return { personalized: true };
  }
}