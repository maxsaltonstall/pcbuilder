/**
 * Spell type definitions for D&D 3.5
 */

export interface SpellLevel {
  [className: string]: number | string | null;
}

export interface Spell {
  id?: string;
  name: string;
  school: string;
  subschool?: string | null;
  descriptors?: string[];
  level: SpellLevel;
  components: string | string[];
  castingTime: string;
  range: string;
  target?: string | null;
  area?: string | null;
  effect?: string | null;
  duration: string;
  savingThrow?: string;
  spellResistance?: string;
  description?: string | null;
  source: string;
}

export interface SpellcastingInfo {
  className: string;
  casterLevel: number;
  spellsKnownByLevel: { [level: number]: number };
  spellsPerDayByLevel: { [level: number]: number };
  highestSpellLevel: number;
}

export interface CharacterSpells {
  spellcastingClasses: SpellcastingInfo[];
  spellsKnown?: Spell[];
  spellsPrepared?: Spell[];
}
