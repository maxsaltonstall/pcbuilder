/**
 * Race type definitions for D&D 3.5
 */

import { AbilityScores } from './character';

export type Size = 'Fine' | 'Diminutive' | 'Tiny' | 'Small' | 'Medium' | 'Large' | 'Huge' | 'Gargantuan' | 'Colossal';

export interface RacialTrait {
  name: string;
  description: string;
}

export interface RacialSkillBonus {
  skillId: string;
  bonus: number;
  condition?: string; // e.g., "in forests" for elves
}

export interface Race {
  id: string;
  name: string;
  description: string;

  // Ability score modifiers
  abilityModifiers: Partial<AbilityScores>;

  // Physical characteristics
  size: Size;
  speed: number; // in feet

  // Special abilities
  traits: RacialTrait[];

  // Skill bonuses
  skillBonuses?: RacialSkillBonus[];

  // Favored class (class that doesn't count for multiclass XP penalty)
  favoredClass: string; // class ID or "any" for humans

  // Automatic languages
  automaticLanguages: string[];
  bonusLanguages: string[];

  // Source book
  source: string;
}

export interface CharacterRace {
  raceId: string;
  raceName: string;
  abilityModifiers: Partial<AbilityScores>;
  traits: RacialTrait[];
  skillBonuses: RacialSkillBonus[];
}
