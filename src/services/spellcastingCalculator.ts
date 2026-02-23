/**
 * Spellcasting Calculator
 * Determines spells known and spells per day for spellcasting characters
 */

import { LevelProgression } from '../types/classes';
import { AbilityScores } from '../types/character';
import { SpellcastingInfo, CharacterSpells } from '../types/spells';

// Spellcasting progression types
type CastingType = 'full' | 'partial' | 'none';

// Classes with spellcasting and their casting type
const SPELLCASTING_CLASSES: Record<string, CastingType> = {
  // Full casters (9th level spells at level 17-20)
  'wizard': 'full',
  'sorcerer': 'full',
  'cleric': 'full',
  'druid': 'full',
  'bard': 'partial', // 6th level spells at 16

  // Partial casters
  'paladin': 'partial', // 4th level spells at 16
  'ranger': 'partial', // 4th level spells at 16

  // Prestige classes that advance spellcasting
  'arcane-trickster': 'full',
  'mystic-theurge': 'full',
  'eldritch-knight': 'partial',
  'arcane-archer': 'partial',
};

function getCastingType(classId: string): CastingType {
  return SPELLCASTING_CLASSES[classId.toLowerCase()] || 'none';
}

function getHighestSpellLevel(casterLevel: number, castingType: CastingType): number {
  if (castingType === 'none') return 0;

  if (castingType === 'full') {
    // Full casters: level 1 = 0th + 1st, level 3 = 2nd, level 5 = 3rd, etc.
    return Math.min(9, Math.floor((casterLevel + 1) / 2));
  }

  // Partial casters (bard, paladin, ranger)
  if (casterLevel < 1) return 0;
  if (casterLevel < 4) return 1;
  if (casterLevel < 7) return 2;
  if (casterLevel < 10) return 3;
  if (casterLevel < 13) return 4;
  if (casterLevel < 16) return 5;
  return 6;
}

function getSpellsPerDay(
  className: string,
  casterLevel: number,
  spellLevel: number,
  abilityModifier: number
): number {
  const castingType = getCastingType(className);
  if (castingType === 'none') return 0;

  // Simplified spells per day (actual values vary by class)
  // This is an approximation - real D&D 3.5 has detailed tables

  if (spellLevel === 0) {
    // Cantrips/Orisons - unlimited for most classes in 3.5
    if (className === 'wizard' || className === 'cleric') return Infinity;
    return 3 + abilityModifier; // For classes with limited cantrips
  }

  const highestLevel = getHighestSpellLevel(casterLevel, castingType);
  if (spellLevel > highestLevel) return 0;

  // Base spells per day
  let baseSpells = 0;
  if (castingType === 'full') {
    baseSpells = 3 + (casterLevel >= spellLevel * 2 - 1 ? 1 : 0);
  } else {
    baseSpells = casterLevel >= 4 + (spellLevel - 1) * 3 ? 1 : 0;
    baseSpells += casterLevel >= 8 + (spellLevel - 1) * 3 ? 1 : 0;
  }

  // Bonus spells from high ability scores
  const bonusSpells = abilityModifier >= spellLevel ? Math.floor((abilityModifier - spellLevel + 1) / 4) + 1 : 0;

  return Math.max(0, baseSpells + bonusSpells);
}

function getSpellsKnown(
  className: string,
  casterLevel: number,
  spellLevel: number
): number {
  const castingType = getCastingType(className);
  if (castingType === 'none') return 0;

  // Wizards and Clerics prepare spells (know all spells in book/domain)
  if (className === 'wizard' || className === 'cleric' || className === 'druid') {
    return Infinity; // They can prepare any spell
  }

  // Sorcerers and Bards have limited spells known
  if (className === 'sorcerer' || className === 'bard') {
    const highestLevel = getHighestSpellLevel(casterLevel, castingType);
    if (spellLevel > highestLevel) return 0;

    // Simplified progression - actual D&D 3.5 has detailed tables
    if (spellLevel === 0) return 4 + Math.floor(casterLevel / 2);
    return 2 + Math.floor(casterLevel / 4);
  }

  // Other classes (paladin, ranger) prepare spells
  return Infinity;
}

export function calculateSpellcasting(
  levelProgression: LevelProgression[],
  abilityScores: AbilityScores
): CharacterSpells | undefined {
  const spellcastingClasses: SpellcastingInfo[] = [];

  // Group levels by class to calculate caster level
  const classLevels = new Map<string, number>();
  levelProgression.forEach(level => {
    const current = classLevels.get(level.class.id) || 0;
    classLevels.set(level.class.id, current + 1);
  });

  // Determine spellcasting for each class
  classLevels.forEach((levels, classId) => {
    const castingType = getCastingType(classId);
    if (castingType === 'none') return;

    const casterLevel = levels;
    const highestSpellLevel = getHighestSpellLevel(casterLevel, castingType);

    if (highestSpellLevel === 0) return;

    // Determine casting ability
    let castingAbility: keyof AbilityScores = 'intelligence';
    if (classId === 'cleric' || classId === 'druid' || classId === 'ranger') {
      castingAbility = 'wisdom';
    } else if (classId === 'sorcerer' || classId === 'bard' || classId === 'paladin') {
      castingAbility = 'charisma';
    }

    const abilityModifier = Math.floor((abilityScores[castingAbility] - 10) / 2);

    // Calculate spells per day and known for each level
    const spellsPerDayByLevel: { [level: number]: number } = {};
    const spellsKnownByLevel: { [level: number]: number } = {};

    for (let spellLevel = 0; spellLevel <= highestSpellLevel; spellLevel++) {
      spellsPerDayByLevel[spellLevel] = getSpellsPerDay(classId, casterLevel, spellLevel, abilityModifier);
      spellsKnownByLevel[spellLevel] = getSpellsKnown(classId, casterLevel, spellLevel);
    }

    spellcastingClasses.push({
      className: classId,
      casterLevel,
      spellsKnownByLevel,
      spellsPerDayByLevel,
      highestSpellLevel,
    });
  });

  if (spellcastingClasses.length === 0) return undefined;

  return {
    spellcastingClasses,
    // Future: populate spellsKnown/spellsPrepared from spell database
  };
}
