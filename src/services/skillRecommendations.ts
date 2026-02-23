import { LevelProgression } from '../types/classes';
import { AbilityScores } from '../types/character';
import { getAbilityModifier, isClassSkill, getMaxRanks, getClassSkillBonus } from './skillCalculator';

export interface SkillAllocation {
  skillId: string;
  skillName: string;
  ranks: number;
  abilityMod: number;
  classSkillBonus: number;
  totalModifier: number;
  isClassSkill: boolean;
  explanation: string;
}

// Common D&D 3.5 skills
const allSkills = [
  { id: 'spot', name: 'Spot', ability: 'wisdom' },
  { id: 'listen', name: 'Listen', ability: 'wisdom' },
  { id: 'search', name: 'Search', ability: 'intelligence' },
  { id: 'hide', name: 'Hide', ability: 'dexterity' },
  { id: 'move-silently', name: 'Move Silently', ability: 'dexterity' },
  { id: 'concentration', name: 'Concentration', ability: 'constitution' },
  { id: 'spellcraft', name: 'Spellcraft', ability: 'intelligence' },
  { id: 'tumble', name: 'Tumble', ability: 'dexterity' },
  { id: 'balance', name: 'Balance', ability: 'dexterity' },
  { id: 'climb', name: 'Climb', ability: 'strength' },
  { id: 'jump', name: 'Jump', ability: 'strength' },
  { id: 'swim', name: 'Swim', ability: 'strength' },
  { id: 'diplomacy', name: 'Diplomacy', ability: 'charisma' },
  { id: 'bluff', name: 'Bluff', ability: 'charisma' },
  { id: 'intimidate', name: 'Intimidate', ability: 'charisma' },
  { id: 'sense-motive', name: 'Sense Motive', ability: 'wisdom' },
  { id: 'heal', name: 'Heal', ability: 'wisdom' },
  { id: 'survival', name: 'Survival', ability: 'wisdom' },
  { id: 'knowledge-arcana', name: 'Knowledge (Arcana)', ability: 'intelligence' },
  { id: 'knowledge-religion', name: 'Knowledge (Religion)', ability: 'intelligence' },
  { id: 'knowledge-nature', name: 'Knowledge (Nature)', ability: 'intelligence' },
  { id: 'knowledge-planes', name: 'Knowledge (The Planes)', ability: 'intelligence' },
  { id: 'use-magic-device', name: 'Use Magic Device', ability: 'charisma' },
  { id: 'disable-device', name: 'Disable Device', ability: 'intelligence' },
  { id: 'open-lock', name: 'Open Lock', ability: 'dexterity' },
  { id: 'sleight-of-hand', name: 'Sleight of Hand', ability: 'dexterity' },
] as const;

type AbilityKey = keyof AbilityScores;

/**
 * Allocate skill points optimally based on user priorities and character build
 */
export function allocateSkillPoints(
  totalPoints: number,
  keySkills: string[],
  progression: LevelProgression[],
  abilityScores: AbilityScores,
  focus: string
): SkillAllocation[] {
  const characterLevel = progression.length;
  const allocations: SkillAllocation[] = [];
  let remainingPoints = totalPoints;

  // Expand key skills with focus-appropriate suggestions
  const expandedPriorities = expandSkillPriorities(keySkills, focus);

  // Sort skills by priority
  const prioritizedSkills = expandedPriorities.map(skillId => {
    const skillData = allSkills.find(s => s.id === skillId);
    if (!skillData) return null;

    const isClass = isClassSkill(skillId, progression);
    const maxRanks = getMaxRanks(characterLevel, isClass);
    const abilityKey = skillData.ability as AbilityKey;
    const abilityMod = getAbilityModifier(abilityScores[abilityKey]);

    return {
      skillId,
      skillData,
      isClass,
      maxRanks,
      abilityMod,
      priority: keySkills.includes(skillId) ? 'high' : 'medium',
    };
  }).filter(Boolean);

  // Allocate to priority skills first (max ranks)
  for (const skill of prioritizedSkills) {
    if (!skill || remainingPoints <= 0) continue;

    const ranksToAssign = Math.min(skill.maxRanks, remainingPoints);
    const classBonus = getClassSkillBonus(ranksToAssign, skill.isClass);
    const totalMod = ranksToAssign + skill.abilityMod + classBonus;

    allocations.push({
      skillId: skill.skillId,
      skillName: skill.skillData.name,
      ranks: ranksToAssign,
      abilityMod: skill.abilityMod,
      classSkillBonus: classBonus,
      totalModifier: totalMod,
      isClassSkill: skill.isClass,
      explanation: getSkillExplanation(skill.skillId, skill.priority, focus),
    });

    remainingPoints -= ranksToAssign;
  }

  // Sort by total modifier (best skills first)
  return allocations.sort((a, b) => b.totalModifier - a.totalModifier);
}

/**
 * Expand key skills with focus-appropriate suggestions
 */
function expandSkillPriorities(keySkills: string[], focus: string): string[] {
  const expanded = new Set(keySkills);

  // Universal important skills
  expanded.add('spot');
  expanded.add('listen');
  expanded.add('search');

  // Focus-specific skills
  switch (focus) {
    case 'melee':
      expanded.add('tumble');
      expanded.add('jump');
      expanded.add('intimidate');
      break;
    case 'ranged':
      expanded.add('hide');
      expanded.add('move-silently');
      expanded.add('tumble');
      break;
    case 'spells':
      expanded.add('concentration');
      expanded.add('spellcraft');
      expanded.add('knowledge-arcana');
      break;
    case 'healing':
      expanded.add('heal');
      expanded.add('concentration');
      expanded.add('diplomacy');
      break;
  }

  return Array.from(expanded);
}

/**
 * Get explanation for why a skill was prioritized
 */
function getSkillExplanation(skillId: string, priority: string, focus: string): string {
  if (priority === 'high') {
    return 'Your priority skill - maxed out';
  }

  const explanations: Record<string, string> = {
    'spot': 'Essential perception - spot hidden enemies',
    'listen': 'Essential perception - hear approaching danger',
    'search': 'Find traps and hidden objects',
    'tumble': `${focus === 'melee' ? 'Avoid AoOs in melee' : 'Mobility in combat'}`,
    'concentration': 'Maintain spells in combat',
    'spellcraft': 'Identify spells and magic items',
    'hide': 'Stealth for surprise attacks',
    'move-silently': 'Silent movement for ambushes',
    'intimidate': 'Demoralize enemies in combat',
    'heal': 'Stabilize and treat wounds',
    'diplomacy': 'Social encounters and party face',
    'knowledge-arcana': 'Identify magical threats',
    'jump': 'Mobility and tactical positioning',
  };

  return explanations[skillId] || 'Recommended for your build';
}
