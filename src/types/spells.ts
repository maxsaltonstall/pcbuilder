/**
 * Spell type definitions for D&D 3.5
 */

/**
 * Spell schools in D&D 3.5
 */
export type SpellSchool =
  | 'abjuration'
  | 'conjuration'
  | 'divination'
  | 'enchantment'
  | 'evocation'
  | 'illusion'
  | 'necromancy'
  | 'transmutation'
  | 'universal';

/**
 * Spell components
 */
export type SpellComponent = 'V' | 'S' | 'M' | 'F' | 'DF' | 'XP';

/**
 * Casting classes that can learn spells
 */
export type CasterClass =
  | 'wizard'
  | 'sorcerer'
  | 'cleric'
  | 'druid'
  | 'bard'
  | 'paladin'
  | 'ranger';

export interface SpellLevel {
  [className: string]: number | string | null | undefined;
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

/**
 * Spell slots by spell level (0-9)
 */
export interface SpellSlots {
  [spellLevel: number]: number;
}

/**
 * Spell progression table entry for a class
 */
export interface SpellProgression {
  classLevel: number;
  spellsPerDay: SpellSlots;
  spellsKnown?: SpellSlots; // For spontaneous casters (Sorcerer/Bard)
}
