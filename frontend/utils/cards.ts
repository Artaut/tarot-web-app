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
  return `https://mystic-tarot-24.preview.emergentagent.com/cards/${slug}`;
}

// Native/Expo scheme URL
export function appSchemeUrl(id: CardId) {
  const slug = cardSlugFromId(id);
  return `mystictarot://cards/${slug}`;
}
