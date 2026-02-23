import { CharacterClass, LevelProgression } from '../types/classes';
import { AbilityScores } from '../types/character';
import { Skill, SkillSynergy } from '../types/skills';
import skillsData from '@data/skills.json';

/**
 * Get ability modifier from ability score
 */
export function getAbilityModifier(abilityScore: number): number {
  return Math.floor((abilityScore - 10) / 2);
}

/**
 * Get expected INT bonus from magic items based on character level and wealth
 * Based on DMG Table 5-1: Character Wealth by Level
 *
 * Typical progression:
 * - Level 5-7: +2 INT (Headband of Intellect +2, 4,000 gp)
 * - Level 8-11: +4 INT (Headband of Intellect +4, 16,000 gp)
 * - Level 12+: +6 INT (Headband of Intellect +6, 36,000 gp)
 */
export function getMagicItemIntBonus(characterLevel: number): number {
  if (characterLevel < 5) return 0;
  if (characterLevel < 8) return 2;
  if (characterLevel < 12) return 4;
  return 6;
}

/**
 * Calculate skill points gained at a specific level
 *
 * D&D 3.5 Rules:
 * - 1st level: (class base + INT modifier) × 4
 * - 2nd+ level: class base + INT modifier
 * - Minimum 1 skill point per level (even with negative INT)
 */
export function calculateSkillPointsForLevel(
  level: number,
  classData: CharacterClass,
  intelligenceScore: number
): number {
  const intModifier = getAbilityModifier(intelligenceScore);
  const basePoints = classData.skillPointsPerLevel;

  let skillPoints: number;

  if (level === 1) {
    // First level gets ×4 multiplier
    skillPoints = (basePoints + intModifier) * 4;
  } else {
    // Subsequent levels
    skillPoints = basePoints + intModifier;
  }

  // Minimum 1 skill point per level
  return Math.max(1, skillPoints);
}

/**
 * Calculate total skill points available across entire progression
 * Accounts for ability score increases at levels 4, 8, 12, 16, 20
 * Optionally accounts for magic item INT bonuses
 */
export function calculateTotalSkillPoints(
  progression: LevelProgression[],
  baseAbilityScores: AbilityScores,
  assumeMagicItems: boolean = false
): number {
  let totalPoints = 0;
  let currentIntelligence = baseAbilityScores.intelligence;

  for (let i = 0; i < progression.length; i++) {
    const level = progression[i];
    const characterLevel = i + 1;

    // Check for ability score increase at levels 4, 8, 12, 16, 20
    if (characterLevel % 4 === 0 && level.abilityIncrease === 'int') {
      currentIntelligence += 1;
    }

    // Add magic item bonus (enhancement bonus, not retroactive)
    const magicItemBonus = assumeMagicItems ? getMagicItemIntBonus(characterLevel) : 0;
    const effectiveInt = currentIntelligence + magicItemBonus;

    const points = calculateSkillPointsForLevel(
      characterLevel,
      level.class,
      effectiveInt
    );

    totalPoints += points;
  }

  return totalPoints;
}

/**
 * Get maximum ranks allowed in a skill at a given character level
 *
 * D&D 3.5 Rules:
 * - Class skill: max ranks = character level + 3
 * - Cross-class skill: max ranks = (character level + 3) / 2
 * - Applies through epic levels (1-30+)
 */
export function getMaxRanks(
  characterLevel: number,
  isClassSkill: boolean
): number {
  if (isClassSkill) {
    return characterLevel + 3;
  } else {
    return Math.floor((characterLevel + 3) / 2);
  }
}

/**
 * Check if a skill is a class skill for any of the character's classes
 */
export function isClassSkill(
  skillId: string,
  progression: LevelProgression[]
): boolean {
  for (const level of progression) {
    if (level.class.classSkills.includes(skillId)) {
      return true;
    }
  }
  return false;
}

/**
 * Validate skill rank assignment
 */
export function canAssignSkillRanks(
  _skillId: string,
  proposedRanks: number,
  characterLevel: number,
  isClassSkill: boolean
): { valid: boolean; error?: string } {
  const maxRanks = getMaxRanks(characterLevel, isClassSkill);

  if (proposedRanks > maxRanks) {
    return {
      valid: false,
      error: `Cannot assign ${proposedRanks} ranks. Maximum for ${
        isClassSkill ? 'class' : 'cross-class'
      } skill at level ${characterLevel} is ${maxRanks}`,
    };
  }

  if (proposedRanks < 0) {
    return {
      valid: false,
      error: 'Cannot assign negative skill ranks',
    };
  }

  return { valid: true };
}

/**
 * Calculate skill points gained at each level in progression
 * Returns array of skill points per level
 * Optionally accounts for magic item INT bonuses
 */
export function getSkillPointsPerLevel(
  progression: LevelProgression[],
  baseAbilityScores: AbilityScores,
  assumeMagicItems: boolean = false
): number[] {
  const pointsPerLevel: number[] = [];
  let currentIntelligence = baseAbilityScores.intelligence;

  for (let i = 0; i < progression.length; i++) {
    const level = progression[i];
    const characterLevel = i + 1;

    // Check for ability score increase
    if (characterLevel % 4 === 0 && level.abilityIncrease === 'int') {
      currentIntelligence += 1;
    }

    // Add magic item bonus
    const magicItemBonus = assumeMagicItems ? getMagicItemIntBonus(characterLevel) : 0;
    const effectiveInt = currentIntelligence + magicItemBonus;

    const points = calculateSkillPointsForLevel(
      characterLevel,
      level.class,
      effectiveInt
    );

    pointsPerLevel.push(points);
  }

  return pointsPerLevel;
}

/**
 * Calculate class skill bonus
 * First rank in a class skill grants +3 bonus
 */
export function getClassSkillBonus(
  totalRanks: number,
  isClassSkill: boolean
): number {
  if (isClassSkill && totalRanks > 0) {
    return 3;
  }
  return 0;
}

/**
 * Calculate total skill bonus
 * Total = ranks + ability modifier + class skill bonus + misc modifiers
 */
export function calculateSkillBonus(
  ranks: number,
  abilityModifier: number,
  isClassSkill: boolean,
  miscModifier: number = 0
): number {
  const classBonus = getClassSkillBonus(ranks, isClassSkill);
  return ranks + abilityModifier + classBonus + miscModifier;
}

/**
 * Optimize skill point distribution to maximize key skills
 * This is a helper for the optimization engine
 */
export function distributeSkillPoints(
  availablePoints: number,
  keySkills: string[],
  characterLevel: number,
  classSkillIds: string[]
): Record<string, number> {
  const distribution: Record<string, number> = {};
  let remainingPoints = availablePoints;

  // Prioritize key skills
  for (const skillId of keySkills) {
    const isClass = classSkillIds.includes(skillId);
    const maxRanks = getMaxRanks(characterLevel, isClass);
    const ranksToAssign = Math.min(maxRanks, remainingPoints);

    distribution[skillId] = ranksToAssign;
    remainingPoints -= ranksToAssign;

    if (remainingPoints <= 0) break;
  }

  return distribution;
}

/**
 * Calculate the skill point advantage of taking one class before another
 * This helps optimize class order
 */
export function calculateSkillPointAdvantage(
  class1: CharacterClass,
  class2: CharacterClass,
  intelligenceScore: number
): number {
  // Calculate difference if taking class1 at level 1 vs class2 at level 1
  const class1First = calculateSkillPointsForLevel(1, class1, intelligenceScore);
  const class2First = calculateSkillPointsForLevel(1, class2, intelligenceScore);

  // The advantage is the difference (class1 first gives this many more points)
  return class1First - class2First;
}

/**
 * Get recommended class order to maximize skill points
 * Higher skill point classes should be taken first
 */
export function getOptimalClassOrder(
  classes: CharacterClass[],
  intelligenceScore: number
): CharacterClass[] {
  return [...classes].sort((a, b) => {
    const aPoints = calculateSkillPointsForLevel(1, a, intelligenceScore);
    const bPoints = calculateSkillPointsForLevel(1, b, intelligenceScore);
    return bPoints - aPoints; // Descending order
  });
}

/**
 * Calculate synergy bonuses for a skill based on ranks in related skills
 * 
 * D&D 3.5 Rules:
 * - Having 5+ ranks in certain skills grants a +2 synergy bonus to related skills
 * - Example: 5 ranks in Bluff grants +2 to Diplomacy, Disguise, Intimidate, Sleight of Hand
 */
export function calculateSynergyBonus(
  skillId: string,
  skillRanks: Record<string, number>
): number {
  const skills = skillsData as Skill[];
  const skill = skills.find(s => s.id === skillId);
  
  if (!skill || !skill.synergiesFrom) {
    return 0;
  }
  
  let totalBonus = 0;
  
  for (const synergy of skill.synergiesFrom) {
    const sourceRanks = skillRanks[synergy.sourceSkillId] || 0;
    if (sourceRanks >= synergy.minimumRanks) {
      totalBonus += synergy.bonus;
    }
  }
  
  return totalBonus;
}

/**
 * Get all synergies that apply to a skill, with their status
 */
export function getSkillSynergies(
  skillId: string,
  skillRanks: Record<string, number>
): Array<SkillSynergy & { sourceSkillName: string; active: boolean }> {
  const skills = skillsData as Skill[];
  const skill = skills.find(s => s.id === skillId);
  
  if (!skill || !skill.synergiesFrom) {
    return [];
  }
  
  return skill.synergiesFrom.map(synergy => {
    const sourceSkill = skills.find(s => s.id === synergy.sourceSkillId);
    const sourceRanks = skillRanks[synergy.sourceSkillId] || 0;
    
    return {
      ...synergy,
      sourceSkillName: sourceSkill?.name || synergy.sourceSkillId,
      active: sourceRanks >= synergy.minimumRanks
    };
  });
}
