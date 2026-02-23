export interface FeatChain {
  chainName: string;
  description: string;
  feats: FeatInChain[];
  focus: string[]; // Which build focuses benefit (melee, ranged, spells, etc.)
}

export interface FeatInChain {
  featId: string;
  featName: string;
  level: number; // Suggested level to take
  acquired: boolean;
  prerequisitesMet: boolean;
  reason: string;
}

export interface ChainProgress {
  chain: FeatChain;
  completed: number; // Number of feats acquired in chain
  total: number;
  nextFeat?: FeatInChain;
  percentComplete: number;
}

/**
 * Common feat chains in D&D 3.5
 */
const FEAT_CHAINS: FeatChain[] = [
  {
    chainName: 'Power Attack Chain',
    description: 'Melee damage optimization through trading accuracy for power',
    focus: ['melee', 'hp'],
    feats: [
      {
        featId: 'power-attack',
        featName: 'Power Attack',
        level: 1,
        acquired: false,
        prerequisitesMet: true,
        reason: 'Foundation: Trade attack for damage (STR 13+)',
      },
      {
        featId: 'cleave',
        featName: 'Cleave',
        level: 3,
        acquired: false,
        prerequisitesMet: false,
        reason: 'Extra attack when you drop an enemy',
      },
      {
        featId: 'great-cleave',
        featName: 'Great Cleave',
        level: 6,
        acquired: false,
        prerequisitesMet: false,
        reason: 'Multiple bonus attacks in one round (BAB +4)',
      },
    ],
  },
  {
    chainName: 'Point Blank Shot Chain',
    description: 'Ranged combat optimization for bow and crossbow users',
    focus: ['ranged'],
    feats: [
      {
        featId: 'point-blank-shot',
        featName: 'Point Blank Shot',
        level: 1,
        acquired: false,
        prerequisitesMet: true,
        reason: 'Foundation: +1 attack/damage within 30ft',
      },
      {
        featId: 'precise-shot',
        featName: 'Precise Shot',
        level: 3,
        acquired: false,
        prerequisitesMet: false,
        reason: 'Ignore soft cover penalties',
      },
      {
        featId: 'rapid-shot',
        featName: 'Rapid Shot',
        level: 6,
        acquired: false,
        prerequisitesMet: false,
        reason: 'Extra attack at -2 (DEX 13+)',
      },
      {
        featId: 'manyshot',
        featName: 'Manyshot',
        level: 9,
        acquired: false,
        prerequisitesMet: false,
        reason: 'Fire two arrows as one attack (DEX 17+, BAB +6)',
      },
    ],
  },
  {
    chainName: 'Weapon Focus Chain',
    description: 'Specialized weapon mastery for consistent attack bonuses',
    focus: ['melee', 'ranged'],
    feats: [
      {
        featId: 'weapon-focus',
        featName: 'Weapon Focus',
        level: 1,
        acquired: false,
        prerequisitesMet: true,
        reason: '+1 attack with chosen weapon (BAB +1)',
      },
      {
        featId: 'weapon-specialization',
        featName: 'Weapon Specialization',
        level: 6,
        acquired: false,
        prerequisitesMet: false,
        reason: '+2 damage with chosen weapon (BAB +4, Fighter only)',
      },
      {
        featId: 'greater-weapon-focus',
        featName: 'Greater Weapon Focus',
        level: 12,
        acquired: false,
        prerequisitesMet: false,
        reason: 'Additional +1 attack (BAB +8, Fighter 8+)',
      },
      {
        featId: 'greater-weapon-specialization',
        featName: 'Greater Weapon Specialization',
        level: 15,
        acquired: false,
        prerequisitesMet: false,
        reason: 'Additional +2 damage (BAB +12, Fighter 12+)',
      },
    ],
  },
  {
    chainName: 'Metamagic Feats',
    description: 'Enhance spell power through metamagic adjustments',
    focus: ['spells', 'healing'],
    feats: [
      {
        featId: 'empower-spell',
        featName: 'Empower Spell',
        level: 3,
        acquired: false,
        prerequisitesMet: true,
        reason: 'Increase spell variables by 50% (+2 slot)',
      },
      {
        featId: 'maximize-spell',
        featName: 'Maximize Spell',
        level: 6,
        acquired: false,
        prerequisitesMet: true,
        reason: 'Maximum effect on spell variables (+3 slot)',
      },
      {
        featId: 'quicken-spell',
        featName: 'Quicken Spell',
        level: 9,
        acquired: false,
        prerequisitesMet: true,
        reason: 'Cast as swift action (+4 slot)',
      },
    ],
  },
  {
    chainName: 'Spell Focus Chain',
    description: 'Increase spell save DCs for specific schools',
    focus: ['spells'],
    feats: [
      {
        featId: 'spell-focus',
        featName: 'Spell Focus',
        level: 1,
        acquired: false,
        prerequisitesMet: true,
        reason: '+1 DC for chosen school',
      },
      {
        featId: 'greater-spell-focus',
        featName: 'Greater Spell Focus',
        level: 6,
        acquired: false,
        prerequisitesMet: false,
        reason: 'Additional +1 DC for chosen school',
      },
    ],
  },
  {
    chainName: 'Two-Weapon Fighting Chain',
    description: 'Dual-wielding mastery for multiple attacks per round',
    focus: ['melee', 'ranged'],
    feats: [
      {
        featId: 'two-weapon-fighting',
        featName: 'Two-Weapon Fighting',
        level: 1,
        acquired: false,
        prerequisitesMet: true,
        reason: 'Reduce TWF penalties (DEX 15+)',
      },
      {
        featId: 'improved-two-weapon-fighting',
        featName: 'Improved Two-Weapon Fighting',
        level: 6,
        acquired: false,
        prerequisitesMet: false,
        reason: 'Second off-hand attack (DEX 17+, BAB +6)',
      },
      {
        featId: 'greater-two-weapon-fighting',
        featName: 'Greater Two-Weapon Fighting',
        level: 12,
        acquired: false,
        prerequisitesMet: false,
        reason: 'Third off-hand attack (DEX 19+, BAB +11)',
      },
    ],
  },
  {
    chainName: 'Combat Reflexes Chain',
    description: 'Opportunity attack optimization for battlefield control',
    focus: ['melee'],
    feats: [
      {
        featId: 'combat-reflexes',
        featName: 'Combat Reflexes',
        level: 1,
        acquired: false,
        prerequisitesMet: true,
        reason: 'Additional attacks of opportunity = DEX mod',
      },
      {
        featId: 'combat-expertise',
        featName: 'Combat Expertise',
        level: 3,
        acquired: false,
        prerequisitesMet: true,
        reason: 'Trade attack for AC (INT 13+)',
      },
      {
        featId: 'improved-trip',
        featName: 'Improved Trip',
        level: 6,
        acquired: false,
        prerequisitesMet: false,
        reason: '+4 on trip attempts, no AoO against you',
      },
    ],
  },
];

/**
 * Detect which feat chains are active in the build
 */
export function detectActiveFeatChains(
  acquiredFeats: string[],
  focus: string
): ChainProgress[] {
  const progress: ChainProgress[] = [];

  for (const chain of FEAT_CHAINS) {
    // Skip chains not relevant to build focus
    if (!chain.focus.includes(focus)) {
      continue;
    }

    const completed = chain.feats.filter(f => acquiredFeats.includes(f.featId)).length;
    const total = chain.feats.length;

    // Mark which feats are acquired
    const updatedChain: FeatChain = {
      ...chain,
      feats: chain.feats.map(f => ({
        ...f,
        acquired: acquiredFeats.includes(f.featId),
      })),
    };

    // Find next feat to acquire
    const nextFeat = updatedChain.feats.find(f => !f.acquired);

    // Only include chains that are started or highly relevant
    if (completed > 0 || chain.feats[0].acquired) {
      progress.push({
        chain: updatedChain,
        completed,
        total,
        nextFeat,
        percentComplete: Math.round((completed / total) * 100),
      });
    }
  }

  // Sort by completion percentage (descending)
  return progress.sort((a, b) => b.percentComplete - a.percentComplete);
}

/**
 * Suggest next feat for each active chain
 */
export function suggestNextFeats(
  acquiredFeats: string[],
  focus: string
): FeatInChain[] {
  const activeChains = detectActiveFeatChains(acquiredFeats, focus);
  const suggestions: FeatInChain[] = [];

  for (const chainProgress of activeChains) {
    if (chainProgress.nextFeat) {
      suggestions.push(chainProgress.nextFeat);
    }
  }

  return suggestions;
}

/**
 * Get all possible feat chains for a build focus
 */
export function getRelevantFeatChains(focus: string): FeatChain[] {
  return FEAT_CHAINS.filter(chain => chain.focus.includes(focus));
}

/**
 * Check if a feat is part of any chain
 */
export function getFeatChainInfo(featId: string): {
  chains: string[];
  position: string;
} | null {
  const chains: string[] = [];
  let position = '';

  for (const chain of FEAT_CHAINS) {
    const index = chain.feats.findIndex(f => f.featId === featId);
    if (index !== -1) {
      chains.push(chain.chainName);
      const total = chain.feats.length;
      if (index === 0) position = 'Foundation';
      else if (index === total - 1) position = 'Capstone';
      else position = `Step ${index + 1} of ${total}`;
    }
  }

  return chains.length > 0 ? { chains, position } : null;
}

/**
 * Analyze feat synergies - which feats work well together
 */
export function analyzeFeatSynergies(
  acquiredFeats: string[]
): { synergies: string[]; recommendations: string[] } {
  const synergies: string[] = [];
  const recommendations: string[] = [];

  // Power Attack + Leap Attack synergy
  if (acquiredFeats.includes('power-attack') && acquiredFeats.includes('leap-attack')) {
    synergies.push('Power Attack + Leap Attack = double Power Attack bonus on charge');
  }

  // Point Blank Shot + Precise Shot synergy
  if (acquiredFeats.includes('point-blank-shot') && acquiredFeats.includes('precise-shot')) {
    synergies.push('Point Blank Shot + Precise Shot = reliable close-range archery');
  }

  // Rapid Shot + Manyshot synergy
  if (acquiredFeats.includes('rapid-shot') && acquiredFeats.includes('manyshot')) {
    synergies.push('Rapid Shot + Manyshot = maximum arrows per round');
  }

  // Combat Expertise + Improved Disarm/Trip synergy
  if (acquiredFeats.includes('combat-expertise')) {
    if (acquiredFeats.includes('improved-disarm') || acquiredFeats.includes('improved-trip')) {
      synergies.push('Combat Expertise enables tactical combat maneuvers');
    }
  }

  // Recommendations based on partial chains
  if (acquiredFeats.includes('power-attack') && !acquiredFeats.includes('cleave')) {
    recommendations.push('Consider Cleave to complete Power Attack chain');
  }

  if (acquiredFeats.includes('point-blank-shot') && !acquiredFeats.includes('precise-shot')) {
    recommendations.push('Precise Shot is essential for ranged builds (eliminates soft cover penalty)');
  }

  if (acquiredFeats.includes('weapon-focus') && !acquiredFeats.includes('weapon-specialization')) {
    recommendations.push('Weapon Specialization adds +2 damage (requires Fighter levels)');
  }

  return { synergies, recommendations };
}

/**
 * Validate feat chain progression - ensure feats are taken in correct order
 */
export function validateFeatChainOrder(
  featProgression: { level: number; featId: string }[]
): { valid: boolean; errors: string[] } {
  const errors: string[] = [];

  // Check each chain
  for (const chain of FEAT_CHAINS) {
    const chainFeats = featProgression
      .filter(fp => chain.feats.some(cf => cf.featId === fp.featId))
      .sort((a, b) => a.level - b.level);

    if (chainFeats.length > 1) {
      // Verify they're in the correct order
      for (let i = 1; i < chainFeats.length; i++) {
        const previousFeatInChain = chain.feats.find(f => f.featId === chainFeats[i - 1].featId);
        const currentFeatInChain = chain.feats.find(f => f.featId === chainFeats[i].featId);

        if (previousFeatInChain && currentFeatInChain) {
          const prevIndex = chain.feats.indexOf(previousFeatInChain);
          const currIndex = chain.feats.indexOf(currentFeatInChain);

          if (currIndex <= prevIndex) {
            errors.push(
              `${chain.chainName}: ${currentFeatInChain.featName} taken before prerequisites met`
            );
          }
        }
      }
    }
  }

  return {
    valid: errors.length === 0,
    errors,
  };
}
