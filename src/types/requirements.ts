export type RequirementType =
  | 'ability'
  | 'skill'
  | 'feat'
  | 'baseAttackBonus'
  | 'casterLevel'
  | 'classLevel'
  | 'race'
  | 'alignment';

export interface Requirement {
  type: RequirementType;
  description: string; // Human-readable description
  validate: (context: RequirementContext) => boolean;
}

export interface AbilityRequirement extends Requirement {
  type: 'ability';
  ability: 'str' | 'dex' | 'con' | 'int' | 'wis' | 'cha';
  minimumScore: number;
}

export interface SkillRequirement extends Requirement {
  type: 'skill';
  skillId: string;
  minimumRanks: number;
}

export interface FeatRequirement extends Requirement {
  type: 'feat';
  featId: string;
}

export interface BaseAttackRequirement extends Requirement {
  type: 'baseAttackBonus';
  minimumBonus: number;
}

export interface CasterLevelRequirement extends Requirement {
  type: 'casterLevel';
  minimumLevel: number;
  spellType?: 'arcane' | 'divine';
}

export interface ClassLevelRequirement extends Requirement {
  type: 'classLevel';
  classId: string;
  minimumLevel: number;
}

export interface RequirementContext {
  abilityScores: Record<string, number>;
  skillRanks: Record<string, number>; // skillId -> total ranks
  feats: string[]; // featIds
  baseAttackBonus: number;
  casterLevel: number;
  arcaneCasterLevel: number;
  divineCasterLevel: number;
  classLevels: Record<string, number>; // classId -> levels
  race?: string;
  alignment?: string;
}
