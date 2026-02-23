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
import { CharacterRace } from '../types/races';
import { CharacterDeitySelection } from '../types/deities';

type CharacterAction =
  | { type: 'UPDATE_INITIAL_SETUP'; payload: { level: number; concept: string; sources: string[] } }
  | { type: 'UPDATE_RACE'; payload: CharacterRace }
  | { type: 'UPDATE_DEITY'; payload: CharacterDeitySelection | undefined }
  | { type: 'UPDATE_ABILITY_SCORES'; payload: { scores: AbilityScores; assumeMagicItems?: boolean } }
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
  | { type: 'RESET_CHARACTER' }
  | { type: 'LOAD_CHARACTER'; payload: CharacterState };

function characterReducer(state: CharacterState, action: CharacterAction): CharacterState {
  switch (action.type) {
    case 'UPDATE_INITIAL_SETUP':
      return {
        ...state,
        totalLevel: action.payload.level,
        concept: action.payload.concept,
        rulesSources: action.payload.sources,
      };
    case 'UPDATE_RACE':
      return {
        ...state,
        race: action.payload,
      };
    case 'UPDATE_DEITY':
      return {
        ...state,
        deity: action.payload,
      };
    case 'UPDATE_ABILITY_SCORES':
      // Apply racial modifiers to base scores
      const baseScores = action.payload.scores;
      const finalScores = state.race ? {
        strength: baseScores.strength + (state.race.abilityModifiers.strength || 0),
        dexterity: baseScores.dexterity + (state.race.abilityModifiers.dexterity || 0),
        constitution: baseScores.constitution + (state.race.abilityModifiers.constitution || 0),
        intelligence: baseScores.intelligence + (state.race.abilityModifiers.intelligence || 0),
        wisdom: baseScores.wisdom + (state.race.abilityModifiers.wisdom || 0),
        charisma: baseScores.charisma + (state.race.abilityModifiers.charisma || 0),
      } : baseScores;

      return {
        ...state,
        baseAbilityScores: baseScores,
        abilityScores: finalScores,
        assumeMagicItems: action.payload.assumeMagicItems,
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
    case 'LOAD_CHARACTER':
      return {
        ...initialCharacterState,
        ...action.payload,
      };
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
    updateRace: (race) =>
      dispatch({ type: 'UPDATE_RACE', payload: race }),
    updateDeity: (deity) =>
      dispatch({ type: 'UPDATE_DEITY', payload: deity }),
    updateAbilityScores: (scores, assumeMagicItems) =>
      dispatch({ type: 'UPDATE_ABILITY_SCORES', payload: { scores, assumeMagicItems } }),
    updateGoals: (classes, feats, skills, focus) =>
      dispatch({ type: 'UPDATE_GOALS', payload: { classes, feats, skills, focus } }),
    setOptimizedProgression: (progression) =>
      dispatch({ type: 'SET_OPTIMIZED_PROGRESSION', payload: progression }),
    setFinalCharacter: (character) =>
      dispatch({ type: 'SET_FINAL_CHARACTER', payload: character }),
    resetCharacter: () => dispatch({ type: 'RESET_CHARACTER' }),
    loadCharacter: (character) => dispatch({ type: 'LOAD_CHARACTER', payload: character }),
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
