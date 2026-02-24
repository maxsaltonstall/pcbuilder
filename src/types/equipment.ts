/**
 * Equipment type definitions for D&D 3.5
 */

/**
 * Equipment slots for worn items
 */
export type EquipmentSlot =
  | 'head'
  | 'headband'
  | 'eyes'
  | 'neck'
  | 'shoulders'
  | 'body'
  | 'torso'
  | 'arms'
  | 'hands'
  | 'ring-left'
  | 'ring-right'
  | 'waist'
  | 'feet'
  | 'main-hand'
  | 'off-hand'
  | 'none'; // For consumables, wondrous items without slots, etc.

/**
 * Weapon categories
 */
export type WeaponCategory = 'simple' | 'martial' | 'exotic';

/**
 * Weapon types
 */
export type WeaponType = 'melee' | 'ranged';

/**
 * Damage types
 */
export type DamageType = 'slashing' | 'piercing' | 'bludgeoning';

/**
 * Weapon size categories
 */
export type WeaponSize = 'light' | 'one-handed' | 'two-handed';

/**
 * Weapon definition
 */
export interface Weapon {
  id: string;
  name: string;
  category: WeaponCategory;
  type: WeaponType;
  size: WeaponSize;
  damage: string; // e.g., "1d8", "2d6"
  damageType: DamageType[];
  critical: string; // e.g., "19-20/x2", "x3"
  range?: number; // In feet, for ranged weapons
  cost: number; // In gold pieces
  weight: number; // In pounds
  special?: string[]; // Special properties
  source: string;
}

/**
 * Armor types
 */
export type ArmorType = 'light' | 'medium' | 'heavy' | 'shield';

/**
 * Armor definition
 */
export interface Armor {
  id: string;
  name: string;
  type: ArmorType;
  armorBonus: number;
  maxDexBonus?: number; // undefined means no limit
  armorCheckPenalty: number;
  arcaneSpellFailure: number; // Percentage
  speed30: number; // Movement speed when base is 30 ft.
  speed20: number; // Movement speed when base is 20 ft.
  cost: number; // In gold pieces
  weight: number; // In pounds
  source: string;
}

/**
 * Magic item bonus types
 */
export type BonusType = 
  | 'enhancement'
  | 'deflection'
  | 'natural-armor'
  | 'shield'
  | 'armor'
  | 'insight'
  | 'luck'
  | 'morale'
  | 'competence'
  | 'resistance'
  | 'sacred'
  | 'profane';

/**
 * Ability score bonuses from items
 */
export interface AbilityBonus {
  ability: 'strength' | 'dexterity' | 'constitution' | 'intelligence' | 'wisdom' | 'charisma';
  bonus: number;
  bonusType: BonusType;
}

/**
 * Magic item definition
 */
export interface MagicItem {
  id: string;
  name: string;
  slot: EquipmentSlot;
  
  // Base item (if applicable)
  baseWeapon?: string; // Weapon ID
  baseArmor?: string; // Armor ID
  
  // Bonuses
  enhancementBonus?: number; // For weapons/armor
  abilityBonuses?: AbilityBonus[];
  acBonus?: number; // Total AC bonus (for rings of protection, etc.)
  savingThrowBonus?: number; // Bonus to all saves (for cloaks of resistance, etc.)
  skillBonuses?: Record<string, number>; // Skill ID -> bonus
  
  // Effects
  effects?: string[]; // Special magical effects
  
  // Pricing
  cost: number; // In gold pieces
  marketPrice?: number; // If different from cost
  
  source: string;
  description?: string;
}

/**
 * Character's equipped items
 */
export interface CharacterEquipment {
  weapons: {
    mainHand?: Weapon | MagicItem;
    offHand?: Weapon | MagicItem;
  };
  armor?: Armor | MagicItem;
  shield?: Armor | MagicItem;
  
  // Magic item slots
  head?: MagicItem;
  headband?: MagicItem;
  eyes?: MagicItem;
  neck?: MagicItem;
  shoulders?: MagicItem;
  body?: MagicItem;
  torso?: MagicItem;
  arms?: MagicItem;
  hands?: MagicItem;
  ringLeft?: MagicItem;
  ringRight?: MagicItem;
  waist?: MagicItem;
  feet?: MagicItem;
  
  // Consumables and other items
  other?: MagicItem[];
  
  // Total wealth value
  totalValue: number;
}

/**
 * Wealth by level from DMG Table 5-1
 */
export const WEALTH_BY_LEVEL: Record<number, number> = {
  1: 0,
  2: 900,
  3: 2700,
  4: 5400,
  5: 9000,
  6: 13000,
  7: 19000,
  8: 27000,
  9: 36000,
  10: 49000,
  11: 66000,
  12: 88000,
  13: 110000,
  14: 150000,
  15: 200000,
  16: 260000,
  17: 340000,
  18: 440000,
  19: 580000,
  20: 760000,
  // Epic levels
  21: 1000000,
  22: 1300000,
  23: 1700000,
  24: 2200000,
  25: 2850000,
  26: 3700000,
  27: 4800000,
  28: 6200000,
  29: 8000000,
  30: 10400000,
  31: 13500000,
  32: 17500000,
  33: 22750000,
  34: 29500000,
  35: 38500000,
  36: 50000000,
  37: 65000000,
  38: 84500000,
  39: 110000000,
  40: 143000000,
};

/**
 * Equipment recommendation for a character build
 */
export interface EquipmentRecommendation {
  totalBudget: number;
  allocations: {
    weapons: number;
    armor: number;
    abilityItems: number;
    protectionItems: number;
    utilityItems: number;
    consumables: number;
  };
  recommendedItems: MagicItem[];
  reasoning: string;
}
