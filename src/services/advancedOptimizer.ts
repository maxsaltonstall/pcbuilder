/**
 * Advanced Optimization Strategies
 * Provides archetype-specific optimization logic beyond the greedy approach
 */

import { ClassSelection, CharacterClass } from '../types/classes';
import { FocusType, AbilityScores } from '../types/character';

export interface OptimizationGoal {
  type: 'feat-chain' | 'skill-monkey' | 'damage' | 'survivability' | 'spellcasting';
  priority: number; // 1-10
  description: string;
}

/**
 * Detect optimization goals based on focus and desired feats/classes
 */
export function detectOptimizationGoals(
  focus: FocusType,
  targetClasses: ClassSelection[],
  desiredFeats: string[]
): OptimizationGoal[] {
  const goals: OptimizationGoal[] = [];

  // Focus-based goals
  if (focus === 'skills') {
    goals.push({
      type: 'skill-monkey',
      priority: 10,
      description: 'Maximize skill points and skill versatility',
    });
  } else if (focus === 'melee' || focus === 'ranged') {
    goals.push({
      type: 'damage',
      priority: 8,
      description: 'Maximize attack damage output',
    });
  } else if (focus === 'hp') {
    goals.push({
      type: 'survivability',
      priority: 10,
      description: 'Maximize hit points and defensive abilities',
    });
  } else if (focus === 'spells') {
    goals.push({
      type: 'spellcasting',
      priority: 10,
      description: 'Maximize caster level and spell access',
    });
  }

  // Feat chain goals
  const hasFeatChains = desiredFeats.some(feat =>
    feat.toLowerCase().includes('greater') ||
    feat.toLowerCase().includes('improved') ||
    feat.toLowerCase().includes('epic')
  );

  if (hasFeatChains || desiredFeats.length > 5) {
    goals.push({
      type: 'feat-chain',
      priority: 7,
      description: 'Unlock feat chains efficiently',
    });
  }

  return goals;
}

/**
 * Calculate BAB breakpoints that are important for feat prerequisites
 */
export function getBABBreakpoints(): number[] {
  return [1, 4, 6, 8, 11, 13, 16, 18]; // Common feat prerequisite BABs
}

/**
 * Calculate caster level breakpoints for important spell levels
 */
export function getCasterLevelBreakpoints(): number[] {
  return [1, 3, 5, 7, 9, 11, 13, 15, 17]; // Spell levels unlock at odd caster levels
}

/**
 * Optimize class order for damage-focused builds
 * Prioritizes: full BAB classes early, power attack at level 1, martial feats
 */
export function optimizeForDamage(
  classesWithLevels: Array<ClassSelection & { levels: number }>,
  classMap: Map<string, CharacterClass>
): Array<{ classId: string; startLevel: number; count: number }> {
  const result: Array<{ classId: string; startLevel: number; count: number }> = [];
  let currentLevel = 1;

  // Sort classes: full BAB first, then average, then poor
  const sorted = [...classesWithLevels].sort((a, b) => {
    const classA = classMap.get(a.classId);
    const classB = classMap.get(b.classId);
    if (!classA || !classB) return 0;

    const babOrder = { good: 3, average: 2, poor: 1 };
    return babOrder[classB.baseAttackBonus] - babOrder[classA.baseAttackBonus];
  });

  sorted.forEach(selection => {
    result.push({
      classId: selection.classId,
      startLevel: currentLevel,
      count: selection.levels,
    });
    currentLevel += selection.levels;
  });

  return result;
}

/**
 * Optimize class order for spellcasting builds
 * Prioritizes: getting to key spell levels quickly, avoiding multiclass penalties
 */
export function optimizeForSpellcasting(
  classesWithLevels: Array<ClassSelection & { levels: number }>,
  classMap: Map<string, CharacterClass>
): Array<{ classId: string; startLevel: number; count: number }> {
  const result: Array<{ classId: string; startLevel: number; count: number }> = [];
  let currentLevel = 1;

  // Identify primary caster class (most levels)
  const primaryCaster = classesWithLevels.reduce((max, curr) =>
    curr.levels > max.levels ? curr : max
  );

  // Put primary caster first to get to high spell levels quickly
  result.push({
    classId: primaryCaster.classId,
    startLevel: currentLevel,
    count: primaryCaster.levels,
  });
  currentLevel += primaryCaster.levels;

  // Add other classes after
  classesWithLevels
    .filter(c => c.classId !== primaryCaster.classId)
    .forEach(selection => {
      result.push({
        classId: selection.classId,
        startLevel: currentLevel,
        count: selection.levels,
      });
      currentLevel += selection.levels;
    });

  return result;
}

/**
 * Optimize class order for skill-focused builds
 * Prioritizes: high skill point classes first, INT-based classes, Rogue/Bard
 */
export function optimizeForSkills(
  classesWithLevels: Array<ClassSelection & { levels: number }>,
  classMap: Map<string, CharacterClass>,
  abilityScores: AbilityScores
): Array<{ classId: string; startLevel: number; count: number }> {
  const result: Array<{ classId: string; startLevel: number; count: number }> = [];
  let currentLevel = 1;

  // Calculate effective skill points per level for each class
  const intMod = Math.floor((abilityScores.intelligence - 10) / 2);
  const withSkillPriority = classesWithLevels.map(selection => {
    const classData = classMap.get(selection.classId);
    const baseSkillPoints = classData?.skillPointsPerLevel || 2;
    const effectivePoints = baseSkillPoints + intMod;

    return {
      ...selection,
      skillPriority: effectivePoints * selection.levels,
    };
  });

  // Sort by total skill points (higher first)
  const sorted = withSkillPriority.sort((a, b) => b.skillPriority - a.skillPriority);

  sorted.forEach(selection => {
    result.push({
      classId: selection.classId,
      startLevel: currentLevel,
      count: selection.levels,
    });
    currentLevel += selection.levels;
  });

  return result;
}

/**
 * Optimize class order for survivability
 * Prioritizes: high HP classes (d12, d10), good Fort saves, defensive abilities
 */
export function optimizeForSurvivability(
  classesWithLevels: Array<ClassSelection & { levels: number }>,
  classMap: Map<string, CharacterClass>
): Array<{ classId: string; startLevel: number; count: number }> {
  const result: Array<{ classId: string; startLevel: number; count: number }> = [];
  let currentLevel = 1;

  // Sort by hit die size (larger first)
  const sorted = [...classesWithLevels].sort((a, b) => {
    const classA = classMap.get(a.classId);
    const classB = classMap.get(b.classId);
    if (!classA || !classB) return 0;

    return classB.hitDie - classA.hitDie;
  });

  sorted.forEach(selection => {
    result.push({
      classId: selection.classId,
      startLevel: currentLevel,
      count: selection.levels,
    });
    currentLevel += selection.levels;
  });

  return result;
}

/**
 * Score a feat based on how many other feats it unlocks
 * Used for prioritizing feat selection
 */
export function calculateFeatChainScore(
  featId: string,
  allFeats: Array<{ id: string; prerequisites: any[] }>,
  targetFeats: string[]
): number {
  let score = 0;

  // Check how many target feats require this feat
  for (const targetFeat of targetFeats) {
    const feat = allFeats.find(f => f.id === targetFeat);
    if (!feat) continue;

    // Check if this feat is in the prerequisites
    const requiresFeat = feat.prerequisites.some(
      prereq => prereq.type === 'feat' && prereq.featId === featId
    );

    if (requiresFeat) {
      score += 10; // High value for directly unlocking target feats
    }
  }

  // Bonus for well-known gateway feats
  const gatewayFeats = [
    'power-attack',
    'combat-expertise',
    'weapon-focus',
    'dodge',
    'point-blank-shot',
  ];

  if (gatewayFeats.includes(featId)) {
    score += 5;
  }

  return score;
}

/**
 * Advanced feat selection strategy that considers feat chains
 */
export function selectOptimalFeat(
  characterLevel: number,
  currentFeats: string[],
  availableFeats: string[],
  targetFeats: string[],
  allFeatsData: Array<{ id: string; prerequisites: any[] }>,
  focus: FocusType
): string | null {
  if (availableFeats.length === 0) return null;

  // Score each available feat
  const scoredFeats = availableFeats.map(featId => ({
    featId,
    score: calculateFeatChainScore(featId, allFeatsData, targetFeats),
  }));

  // Sort by score (highest first)
  scoredFeats.sort((a, b) => b.score - a.score);

  // Return the highest-scoring feat
  return scoredFeats[0]?.featId || null;
}
