import { ClassSelection, LevelProgression, CharacterClass, isPrestigeClass } from '../types/classes';
import { AbilityScores, FocusType } from '../types/character';
import {
  calculateSkillPointsForLevel,
} from './skillCalculator';
import {
  canTakeFeat,
  getMinimumPrestigeEntryLevel,
} from './prerequisiteValidator';
import {
  optimizeForDamage,
  optimizeForSpellcasting,
  optimizeForSkills,
  optimizeForSurvivability,
  selectOptimalFeat,
} from './advancedOptimizer';

import classesData from '@data/classes.json';
import prestigeClassesData from '@data/prestige-classes.json';
import featsData from '@data/feats.json';
import epicFeatsData from '@data/epic-feats.json';

/**
 * Main optimization function
 * Generates optimal level-by-level character progression
 */
export function optimizeClassProgression(
  totalLevel: number,
  targetClasses: ClassSelection[],
  desiredFeats: string[],
  keySkills: string[],
  abilityScores: AbilityScores,
  focus: FocusType
): LevelProgression[] {
  // Step 1: Load class data
  const classMap = loadClassData(targetClasses);

  // Step 2: Distribute levels among selected classes based on priorities
  const classesWithLevels = distributeClassLevels(totalLevel, targetClasses, classMap, abilityScores);

  // Step 3: Build feat dependency graph
  const featGraph = buildFeatDependencyGraph(desiredFeats);

  // Step 4: Determine prestige class entry levels
  const prestigeEntryLevels = calculatePrestigeEntryLevels(classesWithLevels, classMap, abilityScores);

  // Step 5: Order base class levels for skill optimization
  const orderedClasses = orderClassesForSkills(classesWithLevels, classMap, prestigeEntryLevels, abilityScores, focus);

  // Step 6: Generate level progression
  const progression = generateProgression(
    totalLevel,
    orderedClasses,
    classMap,
    abilityScores,
    desiredFeats,
    featGraph,
    keySkills,
    focus
  );

  return progression;
}

/**
 * Load class data from JSON files
 * Filters out incomplete classes (missing id, saves, etc.)
 */
function loadClassData(targetClasses: ClassSelection[]): Map<string, CharacterClass> {
  const classMap = new Map<string, CharacterClass>();

  for (const selection of targetClasses) {
    // Check base classes
    let classData: any = classesData.find(c => c.id === selection.classId);

    // Check prestige classes
    if (!classData) {
      classData = prestigeClassesData.find(c => c.id === selection.classId);
    }

    // Validate class has required data
    if (classData && classData.id && classData.saves && classData.saves.fortitude !== undefined) {
      classMap.set(selection.classId, classData as CharacterClass);
    } else if (classData) {
      console.warn(`Skipping incomplete class: ${classData.name || selection.classId}`);
    }
  }

  return classMap;
}

/**
 * Distribute total levels among selected classes based on priorities
 * Returns class selections with calculated level counts
 */
function distributeClassLevels(
  totalLevel: number,
  targetClasses: ClassSelection[],
  classMap: Map<string, CharacterClass>,
  abilityScores: AbilityScores
): Array<ClassSelection & { levels: number }> {
  if (targetClasses.length === 0) {
    return [];
  }

  // Check if levels are already specified in the input
  const hasExplicitLevels = targetClasses.some(tc => 'levels' in tc && tc.levels !== undefined);

  if (hasExplicitLevels) {
    // Use explicitly specified levels from input
    return targetClasses.map(tc => ({
      ...tc,
      levels: (tc as any).levels || 0
    }));
  }

  // If only one class, give it all levels
  if (targetClasses.length === 1) {
    return [{
      ...targetClasses[0],
      levels: totalLevel
    }];
  }

  // Calculate prestige class minimum levels (to meet prerequisites)
  const prestigeMinimums = new Map<string, number>();
  for (const selection of targetClasses) {
    const classData = classMap.get(selection.classId);
    if (classData && isPrestigeClass(classData)) {
      const minLevel = getMinimumPrestigeEntryLevel(
        classData,
        [], // Parameter not used by function
        {
          strength: abilityScores.strength,
          dexterity: abilityScores.dexterity,
          constitution: abilityScores.constitution,
          intelligence: abilityScores.intelligence,
          wisdom: abilityScores.wisdom,
          charisma: abilityScores.charisma,
        }
      );
      // Prestige class needs at least some levels to be worth taking
      // Reserve minimum 5 levels for prestige class progression
      prestigeMinimums.set(selection.classId, Math.min(5, totalLevel - minLevel + 1));
    }
  }

  // Calculate priority weights (default to medium if not specified)
  const priorityWeights: Record<string, number> = {
    high: 3,
    medium: 2,
    low: 1
  };

  // Build distribution
  const distribution: Array<ClassSelection & { levels: number; weight: number }> = targetClasses.map(tc => ({
    ...tc,
    levels: 0,
    weight: priorityWeights[tc.priority || 'medium']
  }));

  // First, allocate minimum levels for prestige classes
  let remainingLevels = totalLevel;
  for (const item of distribution) {
    const minLevels = prestigeMinimums.get(item.classId);
    if (minLevels) {
      item.levels = minLevels;
      remainingLevels -= minLevels;
    }
  }

  // Calculate total weight for remaining classes
  const totalWeight = distribution
    .filter(d => !prestigeMinimums.has(d.classId))
    .reduce((sum, d) => sum + d.weight, 0);

  // Distribute remaining levels proportionally by weight
  if (totalWeight > 0) {
    for (const item of distribution) {
      if (!prestigeMinimums.has(item.classId)) {
        const proportion = item.weight / totalWeight;
        item.levels = Math.floor(remainingLevels * proportion);
      }
    }

    // Handle rounding - distribute remaining levels to highest priority classes
    let allocated = distribution.reduce((sum, d) => sum + d.levels, 0);
    const sortedByPriority = [...distribution].sort((a, b) => b.weight - a.weight);
    let index = 0;
    while (allocated < totalLevel && index < sortedByPriority.length) {
      sortedByPriority[index].levels += 1;
      allocated += 1;
      index = (index + 1) % sortedByPriority.length;
    }
  }

  // Ensure every class has at least 1 level
  for (const item of distribution) {
    if (item.levels === 0) {
      item.levels = 1;
      // Take from highest level class
      const highest = distribution.reduce((max, d) => d.levels > max.levels ? d : max);
      if (highest.levels > 1) {
        highest.levels -= 1;
      }
    }
  }

  return distribution;
}


/**
 * Build feat dependency graph
 * Returns Map of feat -> prerequisites
 */
export function buildFeatDependencyGraph(desiredFeats: string[]): Map<string, string[]> {
  const graph = new Map<string, string[]>();

  function addFeatDependencies(featId: string, visited = new Set<string>()) {
    if (visited.has(featId)) return; // Prevent infinite loops
    visited.add(featId);

    // Check both regular feats and epic feats
    let feat = featsData.find(f => f.id === featId);
    if (!feat) {
      feat = epicFeatsData.find(f => f.id === featId) as any;
    }
    if (!feat) return;

    const prereqFeats: string[] = [];

    // Handle both string and object prerequisites
    if (Array.isArray(feat.prerequisites)) {
      for (const prereq of feat.prerequisites) {
        if (typeof prereq === 'object' && prereq !== null && 'type' in prereq && prereq.type === 'feat') {
          const prereqFeatId = (prereq as any).featId;
          prereqFeats.push(prereqFeatId);
          // Recursively add prerequisites
          addFeatDependencies(prereqFeatId, visited);
        }
      }
    }

    graph.set(featId, prereqFeats);
  }

  for (const featId of desiredFeats) {
    addFeatDependencies(featId);
  }

  return graph;
}

/**
 * Calculate minimum entry level for each prestige class
 */
function calculatePrestigeEntryLevels(
  targetClasses: Array<ClassSelection & { levels?: number }>,
  classMap: Map<string, CharacterClass>,
  abilityScores: AbilityScores
): Map<string, number> {
  const entryLevels = new Map<string, number>();

  for (const selection of targetClasses) {
    const classData = classMap.get(selection.classId);
    if (!classData || !isPrestigeClass(classData)) continue;

    const minLevel = getMinimumPrestigeEntryLevel(
      classData,
      [], // Parameter not used by function
      {
        strength: abilityScores.strength,
        dexterity: abilityScores.dexterity,
        constitution: abilityScores.constitution,
        intelligence: abilityScores.intelligence,
        wisdom: abilityScores.wisdom,
        charisma: abilityScores.charisma,
      }
    );

    entryLevels.set(selection.classId, minLevel);
  }

  return entryLevels;
}

/**
 * Order classes to maximize skill points
 * Prestige classes are placed at their minimum entry level
 * Supports epic levels (up to 30)
 *
 * IMPORTANT: When prestige classes are present, respect the input order
 * to ensure prerequisites are met at the correct levels.
 */
function orderClassesForSkills(
  targetClasses: Array<ClassSelection & { levels: number }>,
  classMap: Map<string, CharacterClass>,
  prestigeEntryLevels: Map<string, number>,
  abilityScores: AbilityScores,
  focus: FocusType
): { classId: string; startLevel: number; count: number }[] {
  const baseClasses: { classId: string; count: number; classData: CharacterClass }[] = [];
  const prestigeClasses: { classId: string; count: number; entryLevel: number }[] = [];

  // Separate base and prestige classes
  for (const selection of targetClasses) {
    const classData = classMap.get(selection.classId);
    if (!classData) continue;

    if (isPrestigeClass(classData)) {
      prestigeClasses.push({
        classId: selection.classId,
        count: selection.levels,
        entryLevel: prestigeEntryLevels.get(selection.classId) || 1,
      });
    } else {
      baseClasses.push({
        classId: selection.classId,
        count: selection.levels,
        classData,
      });
    }
  }

  // If prestige classes are present, preserve input order for prerequisite timing
  // Re-sorting base classes can delay prestige class entry
  if (prestigeClasses.length > 0) {
    const ordered: { classId: string; startLevel: number; count: number }[] = [];
    let currentLevel = 1;

    for (const selection of targetClasses) {
      ordered.push({
        classId: selection.classId,
        startLevel: currentLevel,
        count: selection.levels,
      });
      currentLevel += selection.levels;
    }

    return ordered;
  }

  // USE ADVANCED OPTIMIZATION STRATEGIES based on focus
  if (focus === 'melee' || focus === 'ranged') {
    return optimizeForDamage(targetClasses, classMap);
  } else if (focus === 'spells' || focus === 'healing') {
    return optimizeForSpellcasting(targetClasses, classMap);
  } else if (focus === 'skills') {
    return optimizeForSkills(targetClasses, classMap, abilityScores);
  } else if (focus === 'hp') {
    return optimizeForSurvivability(targetClasses, classMap);
  }

  // Sort base classes by skill points (descending) with focus-aware optimization
  // OPTIMIZATION: Prioritize classes with most skill points to maximize level 1 ×4 multiplier
  const sortedBaseClasses = baseClasses.sort((a, b) => {
    // Focus-specific optimization
    if (focus === 'spells' || focus === 'healing') {
      // For caster builds, prioritize full casters (Wizard, Cleric, Druid, Sorcerer)
      const fullCasters = ['wizard', 'cleric', 'druid', 'sorcerer', 'psion'];
      const aIsCaster = fullCasters.includes(a.classId);
      const bIsCaster = fullCasters.includes(b.classId);
      if (aIsCaster && !bIsCaster) return -1;
      if (!aIsCaster && bIsCaster) return 1;
    }

    if (focus === 'melee' || focus === 'hp') {
      // For melee builds, prioritize full BAB classes
      const aIsMartial = a.classData.baseAttackBonus === 'good';
      const bIsMartial = b.classData.baseAttackBonus === 'good';
      if (aIsMartial && !bIsMartial) return -1;
      if (!aIsMartial && bIsMartial) return 1;
    }

    // Default: sort by skill points (always valuable)
    const aPoints = calculateSkillPointsForLevel(1, a.classData, abilityScores.intelligence);
    const bPoints = calculateSkillPointsForLevel(1, b.classData, abilityScores.intelligence);

    // If skill points are equal, prefer classes with better BAB for versatility
    if (aPoints === bPoints) {
      const aBab = a.classData.baseAttackBonus === 'good' ? 3 : a.classData.baseAttackBonus === 'average' ? 2 : 1;
      const bBab = b.classData.baseAttackBonus === 'good' ? 3 : b.classData.baseAttackBonus === 'average' ? 2 : 1;
      return bBab - aBab;
    }

    return bPoints - aPoints;
  });

  // Build ordered list
  const ordered: { classId: string; startLevel: number; count: number }[] = [];
  let currentLevel = 1;

  // Take highest skill-point base class first
  if (sortedBaseClasses.length > 0) {
    const firstClass = sortedBaseClasses[0];
    ordered.push({
      classId: firstClass.classId,
      startLevel: currentLevel,
      count: 1,
    });
    currentLevel += 1;
    firstClass.count -= 1;
  }

  // Place remaining levels
  // Simple greedy: fill prestige requirements first, then alternate base classes
  // Support up to level 30 for epic characters
  const maxLevel = targetClasses.reduce((sum, tc) => sum + tc.levels, 0);
  while (currentLevel <= maxLevel && currentLevel <= 30) {
    let placed = false;

    // Check if we need to enter a prestige class at this level
    for (const prestige of prestigeClasses) {
      if (prestige.entryLevel === currentLevel && prestige.count > 0) {
        ordered.push({
          classId: prestige.classId,
          startLevel: currentLevel,
          count: prestige.count,
        });
        currentLevel += prestige.count;
        prestige.count = 0;
        placed = true;
        break;
      }
    }

    if (placed) continue;

    // Place base class levels
    for (const baseClass of sortedBaseClasses) {
      if (baseClass.count > 0) {
        const existing = ordered.find(o => o.classId === baseClass.classId);
        if (existing) {
          existing.count += 1;
        } else {
          ordered.push({
            classId: baseClass.classId,
            startLevel: currentLevel,
            count: 1,
          });
        }
        baseClass.count -= 1;
        currentLevel += 1;
        placed = true;
        break;
      }
    }

    if (!placed) break;
  }

  return ordered;
}

/**
 * Generate complete level-by-level progression
 */
function generateProgression(
  totalLevel: number,
  orderedClasses: { classId: string; startLevel: number; count: number }[],
  classMap: Map<string, CharacterClass>,
  abilityScores: AbilityScores,
  desiredFeats: string[],
  featGraph: Map<string, string[]>,
  _keySkills: string[],
  focus: FocusType
): LevelProgression[] {
  const progression: LevelProgression[] = [];

  // Expand ordered classes into level-by-level
  const levelToClass: CharacterClass[] = [];
  for (const entry of orderedClasses) {
    const classData = classMap.get(entry.classId);
    if (!classData) continue;

    for (let i = 0; i < entry.count; i++) {
      levelToClass.push(classData);
    }
  }

  // Generate progression for each level
  let cumulativeBAB = 0;
  let cumulativeFort = 0;
  let cumulativeRef = 0;
  let cumulativeWill = 0;
  const classLevelCounts: Record<string, number> = {};
  let currentAbilityScores = { ...abilityScores };

  for (let level = 1; level <= totalLevel && level <= Math.min(levelToClass.length, 30); level++) {
    const classData = levelToClass[level - 1];

    // Skip classes with incomplete data
    if (!classData || !classData.id || !classData.saves) {
      console.warn(`Skipping invalid class at level ${level}:`, classData?.name || 'unknown');
      continue;
    }

    const classLevel = (classLevelCounts[classData.id] || 0) + 1;
    classLevelCounts[classData.id] = classLevel;

    // Calculate BAB
    cumulativeBAB += getBABForLevel(classData.baseAttackBonus, classLevel);

    // Calculate saves
    cumulativeFort += getSaveForLevel(classData.saves.fortitude, classLevel);
    cumulativeRef += getSaveForLevel(classData.saves.reflex, classLevel);
    cumulativeWill += getSaveForLevel(classData.saves.will, classLevel);

    // Calculate skill points
    const skillPoints = calculateSkillPointsForLevel(level, classData, currentAbilityScores.intelligence);

    // Ability score increase every 4 levels (continues through epic levels)
    let abilityIncrease: 'str' | 'dex' | 'con' | 'int' | 'wis' | 'cha' | undefined;
    if (level % 4 === 0) {
      abilityIncrease = chooseAbilityIncrease(focus, currentAbilityScores);
      if (abilityIncrease) {
        // Map short form to full ability name
        const abilityMap: Record<'str' | 'dex' | 'con' | 'int' | 'wis' | 'cha', keyof AbilityScores> = {
          str: 'strength',
          dex: 'dexterity',
          con: 'constitution',
          int: 'intelligence',
          wis: 'wisdom',
          cha: 'charisma',
        };
        currentAbilityScores[abilityMap[abilityIncrease]] += 1;
      }
    }

    // Determine if feat is gained this level
    let featGained: string | undefined;
    if (shouldGainFeat(level, classData, classLevel)) {
      featGained = selectNextFeat(progression, desiredFeats, featGraph, abilityScores, focus);
    }

    progression.push({
      levelNumber: level,
      class: classData,
      hitPoints: 0, // Will be calculated later based on rolls/average
      baseAttackBonus: cumulativeBAB,
      saves: {
        fortitude: cumulativeFort,
        reflex: cumulativeRef,
        will: cumulativeWill,
      },
      skillPoints,
      skillsAssigned: {},
      featGained,
      abilityIncrease,
    });
  }

  return progression;
}

/**
 * Calculate BAB increase for a class level
 * This returns the increase for THIS level, not cumulative
 */
function getBABForLevel(progression: 'good' | 'average' | 'poor', classLevel: number): number {
  if (progression === 'good') {
    return 1; // +1 per level
  } else if (progression === 'average') {
    // +3/4 per level: rounds down each level
    // Level 1 = +0, 2 = +1, 3 = +2, 4 = +3, etc.
    // Increase: 0, 1, 1, 1, 0, 1, 1, 1, ...
    const previousTotal = Math.floor((classLevel - 1) * 3 / 4);
    const currentTotal = Math.floor(classLevel * 3 / 4);
    return currentTotal - previousTotal;
  } else {
    // poor: +1/2 per level
    // Level 1 = +0, 2 = +1, 3 = +1, 4 = +2, etc.
    // Increase: 0, 1, 0, 1, ...
    const previousTotal = Math.floor((classLevel - 1) / 2);
    const currentTotal = Math.floor(classLevel / 2);
    return currentTotal - previousTotal;
  }
}

/**
 * Calculate save increase for a class level
 * This returns the increase for THIS level, not cumulative
 */
function getSaveForLevel(progression: 'good' | 'poor', classLevel: number): number {
  if (progression === 'good') {
    // Good save: +2, +3, +3, +4, +4, +5, ...
    // Increase: +2, +1, +0, +1, +0, +1, ...
    const previousTotal = classLevel === 1 ? 0 : 2 + Math.floor((classLevel - 2) / 2);
    const currentTotal = 2 + Math.floor((classLevel - 1) / 2);
    return currentTotal - previousTotal;
  } else {
    // Poor save: +0, +0, +1, +1, +1, +2, ...
    // Increase: +0, +0, +1, +0, +0, +1, ...
    const previousTotal = classLevel === 1 ? 0 : Math.floor((classLevel - 1) / 3);
    const currentTotal = Math.floor(classLevel / 3);
    return currentTotal - previousTotal;
  }
}

/**
 * Determine if character gains a feat this level
 */
function shouldGainFeat(characterLevel: number, classData: CharacterClass, classLevel: number): boolean {
  // D&D 3.5 feat progression:
  // Base: 1, 3, 6, 9, 12, 15, 18
  // Epic (21+): Every 3 levels (21, 24, 27, 30...)

  if (characterLevel <= 20) {
    // Standard progression
    if ([1, 3, 6, 9, 12, 15, 18].includes(characterLevel)) {
      return true;
    }
  } else {
    // Epic progression: every 2 levels starting at 21 (21, 23, 25, 27, 29, 31, 33, 35, 37, 39)
    if (characterLevel >= 21 && (characterLevel - 21) % 2 === 0) {
      return true;
    }
  }

  // Fighters get bonus feats at even class levels
  if (classData.id === 'fighter' && classLevel % 2 === 0) {
    return true;
  }

  return false;
}

/**
 * Select the next feat to assign based on prerequisites and dependency graph
 */
function selectNextFeat(
  currentProgression: LevelProgression[],
  desiredFeats: string[],
  featGraph: Map<string, string[]>,
  abilityScores: AbilityScores,
  focus?: FocusType
): string | undefined {
  const takenFeats = currentProgression
    .filter(l => l.featGained)
    .map(l => l.featGained!);

  // Find all available feats (prerequisites satisfied)
  const availableFeats: string[] = [];

  for (const featId of desiredFeats) {
    if (takenFeats.includes(featId)) continue;

    const prerequisites = featGraph.get(featId) || [];
    const allPrereqsMet = prerequisites.every(prereq => takenFeats.includes(prereq));

    if (allPrereqsMet) {
      // Check actual prerequisites
      const abilityScoresRecord = {
        str: abilityScores.strength,
        dex: abilityScores.dexterity,
        con: abilityScores.constitution,
        int: abilityScores.intelligence,
        wis: abilityScores.wisdom,
        cha: abilityScores.charisma,
      };

      const canTake = canTakeFeat(featId, currentProgression, abilityScoresRecord);
      if (canTake.valid) {
        availableFeats.push(featId);
      }
    }
  }

  // Use advanced feat selection if we have a focus and multiple options
  if (availableFeats.length > 1 && focus) {
    const optimalFeat = selectOptimalFeat(
      currentProgression.length,
      takenFeats,
      availableFeats,
      desiredFeats,
      featsData as Array<{ id: string; prerequisites: any[] }>,
      focus
    );
    if (optimalFeat) return optimalFeat;
  }

  // Fall back to first available feat
  return availableFeats[0];
}

/**
 * Choose which ability score to increase based on focus
 */
function chooseAbilityIncrease(
  focus: FocusType,
  currentScores: AbilityScores
): 'str' | 'dex' | 'con' | 'int' | 'wis' | 'cha' {
  switch (focus) {
    case 'melee':
      return 'str';
    case 'ranged':
      return 'dex';
    case 'spells':
      return currentScores.intelligence >= currentScores.charisma ? 'int' : 'cha';
    case 'healing':
      return 'wis';
    case 'hp':
      return 'con';
    case 'skills':
      return 'int';  // Maximize INT for skill points
    default:
      return 'str';
  }
}
