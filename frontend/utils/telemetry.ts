type ReadingTelemetryEvent = "reading_begin" | "reading_result" | "ai_toggle" | "tone_change" | "length_change";
type MonetizationTelemetryEvent =
  | "share_click"
  | "paywall_view"
  | "purchase_start"
  | "purchase_success"
  | "purchase_fail"
  | "restore_success";

export type TelemetryEvent = {
  event: ReadingTelemetryEvent | MonetizationTelemetryEvent;
  ts?: string;                 // ISO
  sessionId?: string;          // UUID v4 önerilir
  userIdHash?: string | null;  // opsiyonel (PII yok; salted hash)
  lang?: "tr" | "en";
  type?: string;               // reading type (e.g., "card_of_day", "yes_no")
  mode?: "ai" | "rule" | "fallback";
  aiEnabled?: boolean;
  tone?: "gentle" | "analytical" | "motivational" | "spiritual" | "direct";
  length?: "short" | "medium" | "long";
  durationMs?: number;         // reading_begin → reading_result süresi
  questionPresent?: boolean;   // metni loglama, sadece var/yok
};

export async function logEvent(ev: TelemetryEvent) {
  try {
    const ts = new Date().toISOString();
    const body = JSON.stringify({ events: [{ ts, ...ev }] });
    const base = process.env.EXPO_PUBLIC_BACKEND_URL;
    if (!base) return;
    const url = `${base}/api/log`;
    await fetch(url, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body,
    });
  } catch (e) {
    // sessizce yut
  }
}