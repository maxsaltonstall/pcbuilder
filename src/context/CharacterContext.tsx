import { createContext, useContext, useReducer, ReactNode } from 'react';
import {
  CharacterState,
  CharacterContextType,
  initialCharacterState,
  AbilityScores,
  FocusType,
} from '../types/character';
import { ClassSelection, LevelProgression } from '../types/classes';
import { CompleteCharacter } from '../types/complete';

type CharacterAction =
  | { type: 'UPDATE_INITIAL_SETUP'; payload: { level: number; concept: string; sources: string[] } }
  | { type: 'UPDATE_ABILITY_SCORES'; payload: AbilityScores }
  | {
      type: 'UPDATE_GOALS';
      payload: {
        classes: ClassSelection[];
        feats: string[];
        skills: string[];
        focus: FocusType;
      };
    }
  | { type: 'SET_OPTIMIZED_PROGRESSION'; payload: LevelProgression[] }
  | { type: 'SET_FINAL_CHARACTER'; payload: CompleteCharacter }
  | { type: 'RESET_CHARACTER' };

function characterReducer(state: CharacterState, action: CharacterAction): CharacterState {
  switch (action.type) {
    case 'UPDATE_INITIAL_SETUP':
      return {
        ...state,
        totalLevel: action.payload.level,
        concept: action.payload.concept,
        rulesSources: action.payload.sources,
      };
    case 'UPDATE_ABILITY_SCORES':
      return {
        ...state,
        abilityScores: action.payload,
      };
    case 'UPDATE_GOALS':
      return {
        ...state,
        targetClasses: action.payload.classes,
        desiredFeats: action.payload.feats,
        keySkills: action.payload.skills,
        focus: action.payload.focus,
      };
    case 'SET_OPTIMIZED_PROGRESSION':
      return {
        ...state,
        optimizedProgression: action.payload,
      };
    case 'SET_FINAL_CHARACTER':
      return {
        ...state,
        finalCharacter: action.payload,
      };
    case 'RESET_CHARACTER':
      return initialCharacterState;
    default:
      return state;
  }
}

const CharacterContext = createContext<CharacterContextType | undefined>(undefined);

export function CharacterProvider({ children }: { children: ReactNode }) {
  const [state, dispatch] = useReducer(characterReducer, initialCharacterState);

  const value: CharacterContextType = {
    state,
    updateInitialSetup: (level, concept, sources) =>
      dispatch({ type: 'UPDATE_INITIAL_SETUP', payload: { level, concept, sources } }),
    updateAbilityScores: (scores) =>
      dispatch({ type: 'UPDATE_ABILITY_SCORES', payload: scores }),
    updateGoals: (classes, feats, skills, focus) =>
      dispatch({ type: 'UPDATE_GOALS', payload: { classes, feats, skills, focus } }),
    setOptimizedProgression: (progression) =>
      dispatch({ type: 'SET_OPTIMIZED_PROGRESSION', payload: progression }),
    setFinalCharacter: (character) =>
      dispatch({ type: 'SET_FINAL_CHARACTER', payload: character }),
    resetCharacter: () => dispatch({ type: 'RESET_CHARACTER' }),
  };

  return <CharacterContext.Provider value={value}>{children}</CharacterContext.Provider>;
}

export function useCharacter(): CharacterContextType {
  const context = useContext(CharacterContext);
  if (context === undefined) {
    throw new Error('useCharacter must be used within a CharacterProvider');
  }
  return context;
}
