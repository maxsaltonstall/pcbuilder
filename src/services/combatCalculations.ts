import { LevelProgression } from '../types/classes';
import { AbilityScores } from '../types/character';
import { getAbilityModifier } from './skillCalculator';

export interface CombatStats {
  hp: number;
  ac: number;
  touchAC: number;
  flatFootedAC: number;
  initiative: number;
  meleeAttack: string;
  rangedAttack: string;
  baseAttackBonus: number;
  saves: {
    fortitude: number;
    reflex: number;
    will: number;
  };
}

export interface SpellSlots {
  casterLevel: number;
  spellsPerDay: Record<number, number>; // spell level -> slots
  spellsKnown?: Record<number, number>; // for spontaneous casters
  casterClass: string;
}

/**
 * Calculate hit points for character
 * Assumes average HP rolls (for consistency in optimization)
 */
export function calculateHP(
  progression: LevelProgression[],
  abilityScores: AbilityScores
): number {
  let totalHP = 0;
  const conMod = getAbilityModifier(abilityScores.constitution);

  progression.forEach((level, index) => {
    const hitDie = level.class.hitDie || 8;
    const characterLevel = index + 1;

    // First level: max HP
    // Subsequent levels: average (rounded up) + CON mod
    if (characterLevel === 1) {
      totalHP += hitDie + conMod;
    } else {
      const averageRoll = Math.ceil(hitDie / 2 + 1);
      totalHP += averageRoll + conMod;
    }
  });

  // Minimum 1 HP per level
  return Math.max(totalHP, progression.length);
}

/**
 * Calculate Armor Class
 * Base AC calculation without equipment (except assumed magic items)
 */
export function calculateAC(
  abilityScores: AbilityScores,
  assumeMagicItems: boolean,
  characterLevel: number
): { ac: number; touchAC: number; flatFootedAC: number; breakdown: string } {
  const dexMod = getAbilityModifier(abilityScores.dexterity);

  // Base AC = 10 + armor + shield + DEX + natural armor + deflection + misc
  let armorBonus = 0;
  let shieldBonus = 0;
  let naturalArmorBonus = 0;
  let deflectionBonus = 0;

  // Assume wealth-appropriate magic items
  if (assumeMagicItems) {
    // Armor bonus (masterwork/magic armor)
    if (characterLevel >= 3) armorBonus = 5; // Chain shirt +1
    if (characterLevel >= 5) armorBonus = 6; // Chain shirt +2
    if (characterLevel >= 8) armorBonus = 7; // Breastplate +2
    if (characterLevel >= 12) armorBonus = 8; // Breastplate +3

    // Shield bonus (for melee builds)
    if (characterLevel >= 4) shieldBonus = 2; // Light shield
    if (characterLevel >= 10) shieldBonus = 3; // Light shield +1

    // Amulet of Natural Armor
    if (characterLevel >= 6) naturalArmorBonus = 1;
    if (characterLevel >= 10) naturalArmorBonus = 2;
    if (characterLevel >= 15) naturalArmorBonus = 3;

    // Ring of Protection
    if (characterLevel >= 5) deflectionBonus = 1;
    if (characterLevel >= 10) deflectionBonus = 2;
    if (characterLevel >= 15) deflectionBonus = 3;
  }

  const totalAC = 10 + armorBonus + shieldBonus + dexMod + naturalArmorBonus + deflectionBonus;
  const touchAC = 10 + dexMod + deflectionBonus; // No armor/shield/natural
  const flatFootedAC = 10 + armorBonus + shieldBonus + naturalArmorBonus + deflectionBonus; // No DEX

  const breakdown = `10 base + ${armorBonus} armor + ${shieldBonus} shield + ${dexMod} DEX + ${naturalArmorBonus} natural + ${deflectionBonus} deflection`;

  return { ac: totalAC, touchAC, flatFootedAC, breakdown };
}

/**
 * Calculate initiative
 */
export function calculateInitiative(
  abilityScores: AbilityScores,
  hasImprovedInitiative: boolean
): number {
  const dexMod = getAbilityModifier(abilityScores.dexterity);
  const featBonus = hasImprovedInitiative ? 4 : 0;
  return dexMod + featBonus;
}

/**
 * Calculate attack bonuses
 */
export function calculateAttackBonuses(
  baseAttackBonus: number,
  abilityScores: AbilityScores,
  feats: string[]
): { melee: string; ranged: string } {
  const strMod = getAbilityModifier(abilityScores.strength);
  const dexMod = getAbilityModifier(abilityScores.dexterity);

  // Check for relevant feats
  const hasWeaponFocus = feats.some(f => f.toLowerCase().includes('weapon focus'));
  const weaponFocusBonus = hasWeaponFocus ? 1 : 0;

  // Format with iterative attacks for BAB 6+
  const formatAttack = (bab: number, mod: number, focus: number) => {
    const total = bab + mod + focus;
    if (bab >= 16) {
      return `+${total}/+${total - 5}/+${total - 10}/+${total - 15}`;
    } else if (bab >= 11) {
      return `+${total}/+${total - 5}/+${total - 10}`;
    } else if (bab >= 6) {
      return `+${total}/+${total - 5}`;
    }
    return `+${total}`;
  };

  return {
    melee: formatAttack(baseAttackBonus, strMod, weaponFocusBonus),
    ranged: formatAttack(baseAttackBonus, dexMod, weaponFocusBonus),
  };
}

/**
 * Calculate spell slots for caster classes
 */
export function calculateSpellSlots(
  progression: LevelProgression[],
  abilityScores: AbilityScores
): SpellSlots[] {
  const casterLevels = new Map<string, number>();

  // Track caster levels by class
  progression.forEach(level => {
    const className = level.class.name;
    // Identify common caster classes
    const casterClasses = [
      'Wizard', 'Sorcerer', 'Cleric', 'Druid', 'Bard',
      'Paladin', 'Ranger', 'Psion', 'Wilder', 'Psychic Warrior'
    ];

    if (casterClasses.some(c => className.includes(c))) {
      casterLevels.set(className, (casterLevels.get(className) || 0) + 1);
    }
  });

  const spellSlots: SpellSlots[] = [];

  // Generate spell slots for each caster class
  casterLevels.forEach((level, className) => {
    const slots = getSpellSlotsForClass(className, level, abilityScores);
    if (slots) {
      spellSlots.push({
        casterLevel: level,
        spellsPerDay: slots.spellsPerDay,
        spellsKnown: slots.spellsKnown,
        casterClass: className,
      });
    }
  });

  return spellSlots;
}

/**
 * Get spell slots for specific class and level
 */
function getSpellSlotsForClass(
  className: string,
  level: number,
  abilityScores: AbilityScores
): { spellsPerDay: Record<number, number>; spellsKnown?: Record<number, number> } | null {
  // Determine casting stat
  let castingStat: keyof AbilityScores = 'intelligence';
  if (className.includes('Cleric') || className.includes('Druid') || className.includes('Ranger')) {
    castingStat = 'wisdom';
  } else if (className.includes('Sorcerer') || className.includes('Bard') || className.includes('Paladin')) {
    castingStat = 'charisma';
  }

  const castingMod = getAbilityModifier(abilityScores[castingStat]);
  const spellsPerDay: Record<number, number> = {};

  // Full casters (Wizard, Sorcerer, Cleric, Druid)
  const isFullCaster = ['Wizard', 'Sorcerer', 'Cleric', 'Druid'].some(c => className.includes(c));

  if (isFullCaster) {
    // Base slots by level (simplified - would need full tables)
    if (level >= 1) spellsPerDay[0] = 3; // Cantrips
    if (level >= 1) spellsPerDay[1] = 1 + Math.max(0, castingMod);
    if (level >= 3) spellsPerDay[2] = 1 + Math.max(0, castingMod - 1);
    if (level >= 5) spellsPerDay[3] = 1 + Math.max(0, castingMod - 2);
    if (level >= 7) spellsPerDay[4] = 1 + Math.max(0, castingMod - 3);
    if (level >= 9) spellsPerDay[5] = 1 + Math.max(0, castingMod - 4);
    if (level >= 11) spellsPerDay[6] = 1 + Math.max(0, castingMod - 5);
    if (level >= 13) spellsPerDay[7] = 1 + Math.max(0, castingMod - 6);
    if (level >= 15) spellsPerDay[8] = 1 + Math.max(0, castingMod - 7);
    if (level >= 17) spellsPerDay[9] = 1 + Math.max(0, castingMod - 8);
  }

  return Object.keys(spellsPerDay).length > 0 ? { spellsPerDay } : null;
}

/**
 * Calculate all combat stats at once
 */
export function calculateCombatStats(
  progression: LevelProgression[],
  abilityScores: AbilityScores,
  assumeMagicItems: boolean,
  feats: string[]
): CombatStats {
  const characterLevel = progression.length;
  const finalLevel = progression[progression.length - 1];

  const hp = calculateHP(progression, abilityScores);
  const { ac, touchAC, flatFootedAC } = calculateAC(abilityScores, assumeMagicItems, characterLevel);
  const initiative = calculateInitiative(abilityScores, feats.includes('improved-initiative'));
  const { melee, ranged } = calculateAttackBonuses(finalLevel.baseAttackBonus, abilityScores, feats);

  // Add ability modifiers to saves
  const conMod = getAbilityModifier(abilityScores.constitution);
  const dexMod = getAbilityModifier(abilityScores.dexterity);
  const wisMod = getAbilityModifier(abilityScores.wisdom);

  return {
    hp,
    ac,
    touchAC,
    flatFootedAC,
    initiative,
    meleeAttack: melee,
    rangedAttack: ranged,
    baseAttackBonus: finalLevel.baseAttackBonus,
    saves: {
      fortitude: finalLevel.saves.fortitude + conMod,
      reflex: finalLevel.saves.reflex + dexMod,
      will: finalLevel.saves.will + wisMod,
    },
  };
}
