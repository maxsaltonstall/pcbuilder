import { Requirement } from './requirements';

export type AttackBonus = 'good' | 'average' | 'poor';
export type SaveProgression = 'good' | 'poor';

export interface SaveBonuses {
  fortitude: SaveProgression;
  reflex: SaveProgression;
  will: SaveProgression;
}

export interface BaseClass {
  id: string;
  name: string;
  description: string;
  hitDie: number;
  skillPointsPerLevel: number;
  classSkills: string[];
  baseAttackBonus: AttackBonus;
  saves: SaveBonuses;
  source: string;
}

export interface PrestigeClass extends BaseClass {
  requirements: Requirement[];
  isPrestige: true;
}

export type CharacterClass = BaseClass | PrestigeClass;

export function isPrestigeClass(cls: CharacterClass): cls is PrestigeClass {
  return 'isPrestige' in cls && cls.isPrestige === true;
}

export type ClassPriority = 'high' | 'medium' | 'low';

export interface ClassSelection {
  classId: string;
  className: string;
  priority?: ClassPriority; // Optional: hints to optimizer about desired emphasis
}

export interface LevelProgression {
  levelNumber: number;
  class: CharacterClass;
  hitPoints: number;
  baseAttackBonus: number;
  saves: {
    fortitude: number;
    reflex: number;
    will: number;
  };
  skillPoints: number;
  skillsAssigned: Record<string, number>; // skillId -> ranks assigned this level
  featGained?: string; // featId if feat is gained this level
  abilityIncrease?: 'str' | 'dex' | 'con' | 'int' | 'wis' | 'cha'; // at levels 4, 8, 12, 16, 20
}
