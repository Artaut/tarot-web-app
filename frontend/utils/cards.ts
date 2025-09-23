export type CardId =
  | "fool" | "magician" | "high_priestess" | "empress" | "emperor"
  | "hierophant" | "lovers" | "chariot" | "strength" | "hermit"
  | "wheel_of_fortune" | "justice" | "hanged_man" | "death" | "temperance"
  | "devil" | "tower" | "star" | "moon" | "sun" | "judgement" | "world";

export const CARD_SLUGS: Record<CardId, string> = {
  fool:"deli",
  magician:"buyucu",
  high_priestess:"azize",
  empress:"imparatorice",
  emperor:"imparator",
  hierophant:"aziz",
  lovers:"asiklar",
  chariot:"savas-arabasi",
  strength:"guc",
  hermit:"ermis",
  wheel_of_fortune:"kader-carki",
  justice:"adalet",
  hanged_man:"asilan-adam",
  death:"olum",
  temperance:"denge",
  devil:"seytan",
  tower:"kule",
  star:"yildiz",
  moon:"ay",
  sun:"gunes",
  judgement:"yargi",
  world:"dunya",
};

const SLUG_TO_ID = Object.fromEntries(
  Object.entries(CARD_SLUGS).map(([id, slug]) => [slug, id as CardId])
) as Record<string, CardId>;

export function cardSlugFromId(id: CardId) {
  return CARD_SLUGS[id];
}

export function cardIdFromSlug(slug: string): CardId | null {
  return SLUG_TO_ID[slug] ?? null;
}

// Web URL (universal link)
export function webCardUrl(id: CardId) {
  const slug = cardSlugFromId(id);
  return `https://divinereader.preview.emergentagent.com/cards/${slug}`;
}

// Native/Expo scheme URL
export function appSchemeUrl(id: CardId) {
  const slug = cardSlugFromId(id);
  return `mystictarot://cards/${slug}`;
}

// Numeric (0..21) -> CardId mapping (RWS order)
export const NUMERIC_ID_TO_CARD_ID: CardId[] = [
  "fool",             // 0
  "magician",         // 1
  "high_priestess",   // 2
  "empress",          // 3
  "emperor",          // 4
  "hierophant",       // 5
  "lovers",           // 6
  "chariot",          // 7
  "strength",         // 8
  "hermit",           // 9
  "wheel_of_fortune", // 10
  "justice",          // 11
  "hanged_man",       // 12
  "death",            // 13
  "temperance",       // 14
  "devil",            // 15
  "tower",            // 16
  "star",             // 17
  "moon",             // 18
  "sun",              // 19
  "judgement",        // 20
  "world"             // 21
];

export function cardIdFromNumeric(n: number): CardId | null {
  if (Number.isInteger(n) && n >= 0 && n < NUMERIC_ID_TO_CARD_ID.length) {
    return NUMERIC_ID_TO_CARD_ID[n];
  }
  return null;
}
