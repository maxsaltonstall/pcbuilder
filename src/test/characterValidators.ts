import { LevelProgression, isPrestigeClass } from '../types/classes';
import { AbilityScores } from '../types/character';
import { canTakeFeat } from '../services/prerequisiteValidator';
import featsData from '@data/feats.json';

export interface ValidationResult {
  valid: boolean;
  errors: string[];
}

/**
 * Validate that total levels match requested level
 */
export function validateTotalLevels(
  progression: LevelProgression[],
  expectedLevel: number
): ValidationResult {
  const errors: string[] = [];

  if (progression.length !== expectedLevel) {
    errors.push(
      `Expected ${expectedLevel} levels, got ${progression.length}`
    );
  }

  // Check sequential level numbering
  progression.forEach((level, index) => {
    if (level.levelNumber !== index + 1) {
      errors.push(
        `Level ${index + 1} has incorrect levelNumber: ${level.levelNumber}`
      );
    }
  });

  return {
    valid: errors.length === 0,
    errors,
  };
}

/**
 * Validate that all feats have prerequisites met when gained
 */
export function validateFeatPrerequisites(
  progression: LevelProgression[],
  abilityScores: AbilityScores
): ValidationResult {
  const errors: string[] = [];

  const abilityScoresRecord = {
    str: abilityScores.strength,
    dex: abilityScores.dexterity,
    con: abilityScores.constitution,
    int: abilityScores.intelligence,
    wis: abilityScores.wisdom,
    cha: abilityScores.charisma,
  };

  for (let i = 0; i < progression.length; i++) {
    const level = progression[i];
    if (!level.featGained) continue;

    const feat = featsData.find(f => f.id === level.featGained);
    if (!feat) {
      errors.push(`Unknown feat at level ${level.levelNumber}: ${level.featGained}`);
      continue;
    }

    // Check prerequisites at this point in progression
    const progressionSoFar = progression.slice(0, i + 1);
    const result = canTakeFeat(level.featGained, progressionSoFar, abilityScoresRecord);

    if (!result.valid) {
      errors.push(
        `Feat "${feat.name}" at level ${level.levelNumber} has unmet prerequisites: ${result.errors.join(', ')}`
      );
    }
  }

  return {
    valid: errors.length === 0,
    errors,
  };
}

/**
 * Validate prestige classes entered at correct levels
 */
export function validatePrestigeRequirements(
  progression: LevelProgression[]
): ValidationResult {
  const errors: string[] = [];

  for (let i = 0; i < progression.length; i++) {
    const level = progression[i];
    if (!isPrestigeClass(level.class)) continue;

    // First level of this prestige class
    const isFirstLevel = i === 0 || progression[i - 1].class.id !== level.class.id;
    if (!isFirstLevel) continue;

    // Check if requirements are met
    const progressionBefore = progression.slice(0, i);

    // For now, just check that it's not the first level of the character
    if (i === 0) {
      errors.push(
        `Prestige class "${level.class.name}" cannot be taken at level 1`
      );
    }

    // TODO: Add more specific prerequisite checks using prerequisiteValidator
  }

  return {
    valid: errors.length === 0,
    errors,
  };
}

/**
 * Validate skill points calculated correctly
 */
export function validateSkillPoints(
  progression: LevelProgression[]
): ValidationResult {
  const errors: string[] = [];

  for (const level of progression) {
    if (level.skillPoints < 1) {
      errors.push(
        `Level ${level.levelNumber} has invalid skill points: ${level.skillPoints} (minimum is 1)`
      );
    }

    // First level should have 4x multiplier
    if (level.levelNumber === 1 && level.skillPoints < 4) {
      errors.push(
        `Level 1 should have at least 4 skill points (with 4x multiplier), got ${level.skillPoints}`
      );
    }
  }

  return {
    valid: errors.length === 0,
    errors,
  };
}

/**
 * Validate BAB progression
 */
export function validateBAB(progression: LevelProgression[]): ValidationResult {
  const errors: string[] = [];

  // BAB should never decrease
  let previousBAB = 0;
  for (const level of progression) {
    if (level.baseAttackBonus < previousBAB) {
      errors.push(
        `BAB decreased at level ${level.levelNumber}: ${previousBAB} -> ${level.baseAttackBonus}`
      );
    }
    previousBAB = level.baseAttackBonus;
  }

  // Check final BAB is reasonable
  const finalLevel = progression[progression.length - 1];
  const maxBAB = finalLevel.levelNumber; // Good progression = +1/level
  if (finalLevel.baseAttackBonus > maxBAB) {
    errors.push(
      `BAB at level ${finalLevel.levelNumber} exceeds maximum: ${finalLevel.baseAttackBonus} > ${maxBAB}`
    );
  }

  return {
    valid: errors.length === 0,
    errors,
  };
}

/**
 * Validate saving throw progression
 */
export function validateSaves(progression: LevelProgression[]): ValidationResult {
  const errors: string[] = [];

  // Saves should never decrease
  let previousFort = 0;
  let previousRef = 0;
  let previousWill = 0;

  for (const level of progression) {
    if (level.saves.fortitude < previousFort) {
      errors.push(
        `Fort save decreased at level ${level.levelNumber}: ${previousFort} -> ${level.saves.fortitude}`
      );
    }
    if (level.saves.reflex < previousRef) {
      errors.push(
        `Ref save decreased at level ${level.levelNumber}: ${previousRef} -> ${level.saves.reflex}`
      );
    }
    if (level.saves.will < previousWill) {
      errors.push(
        `Will save decreased at level ${level.levelNumber}: ${previousWill} -> ${level.saves.will}`
      );
    }

    previousFort = level.saves.fortitude;
    previousRef = level.saves.reflex;
    previousWill = level.saves.will;
  }

  return {
    valid: errors.length === 0,
    errors,
  };
}

/**
 * Validate ability score increases occur at correct levels
 */
export function validateAbilityIncreases(
  progression: LevelProgression[]
): ValidationResult {
  const errors: string[] = [];

  // Ability increases should occur at levels 4, 8, 12, 16, 20, 24, 28
  const expectedLevels = [4, 8, 12, 16, 20, 24, 28];
  const actualLevels = progression
    .filter(l => l.abilityIncrease)
    .map(l => l.levelNumber);

  const maxLevel = progression.length;
  const expectedForThisLevel = expectedLevels.filter(l => l <= maxLevel);

  if (actualLevels.length !== expectedForThisLevel.length) {
    errors.push(
      `Expected ${expectedForThisLevel.length} ability increases for level ${maxLevel}, got ${actualLevels.length}`
    );
  }

  // Check they're at the right levels
  for (const expectedLevel of expectedForThisLevel) {
    if (!actualLevels.includes(expectedLevel)) {
      errors.push(`Missing ability increase at level ${expectedLevel}`);
    }
  }

  // Check no increases at wrong levels
  for (const actualLevel of actualLevels) {
    if (!expectedLevels.includes(actualLevel)) {
      errors.push(`Unexpected ability increase at level ${actualLevel}`);
    }
  }

  return {
    valid: errors.length === 0,
    errors,
  };
}

/**
 * Validate entire character progression
 */
export function validateCharacter(
  progression: LevelProgression[],
  expectedLevel: number,
  abilityScores: AbilityScores
): ValidationResult {
  const errors: string[] = [];

  // Run all validators
  const totalLevelsResult = validateTotalLevels(progression, expectedLevel);
  const featPrereqsResult = validateFeatPrerequisites(progression, abilityScores);
  const prestigeResult = validatePrestigeRequirements(progression);
  const skillPointsResult = validateSkillPoints(progression);
  const babResult = validateBAB(progression);
  const savesResult = validateSaves(progression);
  const abilityIncreasesResult = validateAbilityIncreases(progression);

  errors.push(
    ...totalLevelsResult.errors,
    ...featPrereqsResult.errors,
    ...prestigeResult.errors,
    ...skillPointsResult.errors,
    ...babResult.errors,
    ...savesResult.errors,
    ...abilityIncreasesResult.errors
  );

  return {
    valid: errors.length === 0,
    errors,
  };
}
