import { ClassSelection, LevelProgression } from './classes';
import { CompleteCharacter } from './complete';
import { CharacterRace } from './races';

export type FocusType = 'melee' | 'ranged' | 'spells' | 'healing' | 'hp' | 'skills';

export interface AbilityScores {
  strength: number;
  dexterity: number;
  constitution: number;
  intelligence: number;
  wisdom: number;
  charisma: number;
}

export interface CharacterState {
  // Step 1: Initial Setup
  totalLevel: number;
  concept: string;
  rulesSources: string[];
  race?: CharacterRace;

  // Step 2: Ability Scores (base scores before racial modifiers)
  baseAbilityScores?: AbilityScores;
  abilityScores?: AbilityScores; // Final scores with racial modifiers
  assumeMagicItems?: boolean; // Assume standard wealth-appropriate INT-boosting items

  // Step 3: Goal Setting
  targetClasses: ClassSelection[];
  desiredFeats: string[];
  keySkills: string[];
  focus: FocusType;

  // Step 4: Optimization Results
  optimizedProgression: LevelProgression[];

  // Step 5: Final Character
  finalCharacter?: CompleteCharacter;
}

export interface CharacterContextType {
  state: CharacterState;
  updateInitialSetup: (level: number, concept: string, sources: string[]) => void;
  updateRace: (race: CharacterRace) => void;
  updateAbilityScores: (scores: AbilityScores, assumeMagicItems?: boolean) => void;
  updateGoals: (
    classes: ClassSelection[],
    feats: string[],
    skills: string[],
    focus: FocusType
  ) => void;
  setOptimizedProgression: (progression: LevelProgression[]) => void;
  setFinalCharacter: (character: CompleteCharacter) => void;
  resetCharacter: () => void;
  loadCharacter: (character: CharacterState) => void;
}

export const initialCharacterState: CharacterState = {
  totalLevel: 1,
  concept: '',
  rulesSources: ['Player\'s Handbook'],
  targetClasses: [],
  desiredFeats: [],
  keySkills: [],
  focus: 'melee',
  optimizedProgression: []
};
