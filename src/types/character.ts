import { ClassSelection, LevelProgression } from './classes';
import { CompleteCharacter } from './complete';

export type FocusType = 'melee' | 'ranged' | 'spells' | 'healing' | 'hp';

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

  // Step 2: Ability Scores
  abilityScores?: AbilityScores;
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
