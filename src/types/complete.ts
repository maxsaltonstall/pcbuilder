import { AbilityScores } from './character';
import { LevelProgression } from './classes';
import { FeatSelection } from './feats';
import { SkillRanks } from './skills';

export interface CompleteCharacter {
  // Basic Info
  name: string;
  concept: string;
  level: number;

  // Ability Scores (final, with level bonuses)
  abilityScores: AbilityScores;
  abilityModifiers: AbilityScores;

  // Progression
  levelProgression: LevelProgression[];

  // Combat Stats
  hitPoints: number;
  armorClass: number;
  initiative: number;
  baseAttackBonus: number;

  // Saves
  saves: {
    fortitude: number;
    reflex: number;
    will: number;
  };

  // Skills
  skills: SkillRanks[];

  // Feats
  feats: FeatSelection[];

  // Summary
  classSummary: string; // e.g., "Fighter 5 / Wizard 3 / Eldritch Knight 7"

  // Metadata
  createdAt: Date;
  rulesSources: string[];
}
