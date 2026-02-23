export type AbilityType = 'str' | 'dex' | 'con' | 'int' | 'wis' | 'cha';

export interface SkillSynergy {
  /** Skill that provides the bonus */
  sourceSkillId: string;
  /** Minimum ranks required in source skill */
  minimumRanks: number;
  /** Bonus granted (usually +2) */
  bonus: number;
  /** Condition or situation when bonus applies */
  condition?: string;
}

export interface Skill {
  id: string;
  name: string;
  description: string;
  keyAbility: AbilityType;
  trainedOnly: boolean;
  armorCheckPenalty: boolean;
  source: string;
  /** Synergy bonuses this skill receives from other skills */
  synergiesFrom?: SkillSynergy[];
  /** Example DCs and uses (optional) */
  examples?: string;
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
