export type AbilityType = 'str' | 'dex' | 'con' | 'int' | 'wis' | 'cha';

export interface Skill {
  id: string;
  name: string;
  description: string;
  keyAbility: AbilityType;
  trainedOnly: boolean;
  armorCheckPenalty: boolean;
  source: string;
}

export interface SkillRanks {
  skillId: string;
  skillName: string;
  totalRanks: number;
  isClassSkill: boolean;
  abilityModifier: number;
  miscModifier: number;
  totalBonus: number;
}
