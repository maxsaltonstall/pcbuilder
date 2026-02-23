import { LevelProgression } from '../types/classes';
import { FocusType } from '../types/character';

export interface FeatRecommendation {
  featId: string;
  featName: string;
  level: number;
  reason: string;
  isUserRequested: boolean;
}

/**
 * Generate feat recommendations for all feat slots
 */
export function recommendFeats(
  progression: LevelProgression[],
  desiredFeats: string[],
  focus: FocusType
): FeatRecommendation[] {
  const recommendations: FeatRecommendation[] = [];
  const assignedFeats = new Set<string>();

  // Process each level that grants a feat
  progression.forEach((level) => {
    if (level.featGained) {
      // If user already requested a feat for this level, use it
      if (level.featGained && level.featGained !== 'TBD') {
        recommendations.push({
          featId: level.featGained,
          featName: level.featGained,
          level: level.levelNumber,
          reason: 'Your requested feat',
          isUserRequested: true,
        });
        assignedFeats.add(level.featGained);
      } else {
        // Recommend a feat based on build
        const recommended = getNextRecommendedFeat(
          assignedFeats,
          desiredFeats,
          focus,
          level.levelNumber
        );
        if (recommended) {
          recommendations.push({
            ...recommended,
            level: level.levelNumber,
          });
          assignedFeats.add(recommended.featId);
        }
      }
    }
  });

  return recommendations;
}

/**
 * Get the next recommended feat based on what's already taken
 */
function getNextRecommendedFeat(
  assignedFeats: Set<string>,
  desiredFeats: string[],
  focus: FocusType,
  level: number
): Omit<FeatRecommendation, 'level'> | null {
  // First, try to fulfill user's desired feats
  for (const featId of desiredFeats) {
    if (!assignedFeats.has(featId)) {
      return {
        featId,
        featName: featId,
        reason: 'Your requested feat',
        isUserRequested: true,
      };
    }
  }

  // Then suggest build-appropriate feats
  const buildFeats = getBuildFeatProgression(focus);

  for (const feat of buildFeats) {
    if (!assignedFeats.has(feat.featId)) {
      return feat;
    }
  }

  // Fallback generic feats
  const genericFeats = [
    { featId: 'toughness', featName: 'Toughness', reason: 'Extra hit points' },
    { featId: 'iron-will', featName: 'Iron Will', reason: '+2 to Will saves' },
    { featId: 'lightning-reflexes', featName: 'Lightning Reflexes', reason: '+2 to Reflex saves' },
    { featId: 'great-fortitude', featName: 'Great Fortitude', reason: '+2 to Fortitude saves' },
    { featId: 'improved-initiative', featName: 'Improved Initiative', reason: '+4 to initiative' },
    { featId: 'weapon-focus', featName: 'Weapon Focus', reason: '+1 to attack rolls' },
  ];

  for (const feat of genericFeats) {
    if (!assignedFeats.has(feat.featId)) {
      return feat;
    }
  }

  return null;
}

/**
 * Get optimal feat progression for a build focus
 */
function getBuildFeatProgression(focus: FocusType): Omit<FeatRecommendation, 'level'>[] {
  switch (focus) {
    case 'melee':
      return [
        { featId: 'power-attack', featName: 'Power Attack', reason: 'Trade accuracy for damage - melee essential', isUserRequested: false },
        { featId: 'cleave', featName: 'Cleave', reason: 'Extra attack when you drop an enemy', isUserRequested: false },
        { featId: 'improved-initiative', featName: 'Improved Initiative', reason: 'Act first in combat', isUserRequested: false },
        { featId: 'weapon-focus', featName: 'Weapon Focus', reason: '+1 to attack with chosen weapon', isUserRequested: false },
        { featId: 'weapon-specialization', featName: 'Weapon Specialization', reason: '+2 damage with chosen weapon', isUserRequested: false },
        { featId: 'toughness', featName: 'Toughness', reason: 'Survive longer in melee', isUserRequested: false },
        { featId: 'improved-critical', featName: 'Improved Critical', reason: 'Double threat range', isUserRequested: false },
      ];

    case 'ranged':
      return [
        { featId: 'point-blank-shot', featName: 'Point Blank Shot', reason: 'Essential ranged feat - +1 attack/damage within 30ft', isUserRequested: false },
        { featId: 'precise-shot', featName: 'Precise Shot', reason: 'No penalty for shooting into melee', isUserRequested: false },
        { featId: 'rapid-shot', featName: 'Rapid Shot', reason: 'Extra attack with ranged weapons', isUserRequested: false },
        { featId: 'weapon-focus', featName: 'Weapon Focus (Bow)', reason: '+1 to attack rolls', isUserRequested: false },
        { featId: 'manyshot', featName: 'Manyshot', reason: 'Fire multiple arrows at once', isUserRequested: false },
        { featId: 'improved-initiative', featName: 'Improved Initiative', reason: 'Strike before enemies close distance', isUserRequested: false },
      ];

    case 'spells':
      return [
        { featId: 'spell-focus', featName: 'Spell Focus (Evocation)', reason: '+1 DC for chosen school', isUserRequested: false },
        { featId: 'combat-casting', featName: 'Combat Casting', reason: '+4 to Concentration checks in combat', isUserRequested: false },
        { featId: 'empower-spell', featName: 'Empower Spell', reason: '+50% damage on spells', isUserRequested: false },
        { featId: 'maximize-spell', featName: 'Maximize Spell', reason: 'Maximum effect on variable spells', isUserRequested: false },
        { featId: 'quicken-spell', featName: 'Quicken Spell', reason: 'Cast as swift action', isUserRequested: false },
        { featId: 'spell-penetration', featName: 'Spell Penetration', reason: '+2 to overcome spell resistance', isUserRequested: false },
      ];

    case 'healing':
      return [
        { featId: 'combat-casting', featName: 'Combat Casting', reason: 'Cast healing spells in combat', isUserRequested: false },
        { featId: 'empower-spell', featName: 'Empower Spell', reason: '+50% healing', isUserRequested: false },
        { featId: 'extend-spell', featName: 'Extend Spell', reason: 'Double duration on buffs', isUserRequested: false },
        { featId: 'spell-focus', featName: 'Spell Focus (Conjuration)', reason: 'Better healing/summoning', isUserRequested: false },
        { featId: 'improved-initiative', featName: 'Improved Initiative', reason: 'Heal allies before they drop', isUserRequested: false },
      ];

    case 'hp':
      return [
        { featId: 'toughness', featName: 'Toughness', reason: '+3 HP - essential for tank', isUserRequested: false },
        { featId: 'improved-toughness', featName: 'Improved Toughness', reason: 'Even more HP', isUserRequested: false },
        { featId: 'great-fortitude', featName: 'Great Fortitude', reason: 'Resist poison/disease', isUserRequested: false },
        { featId: 'endurance', featName: 'Endurance', reason: '+4 to various endurance checks', isUserRequested: false },
        { featId: 'diehard', featName: 'Diehard', reason: 'Remain conscious below 0 HP', isUserRequested: false },
        { featId: 'iron-will', featName: 'Iron Will', reason: 'Resist mind control', isUserRequested: false },
      ];

    default:
      return [];
  }
}
