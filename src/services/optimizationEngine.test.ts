import { describe, it, expect } from 'vitest';
import { optimizeClassProgression, buildFeatDependencyGraph } from './optimizationEngine';
import { ClassSelection } from '../types/classes';
import { AbilityScores } from '../types/character';
import {
  validateCharacter,
  validateTotalLevels,
  validateFeatPrerequisites,
  validateAbilityIncreases,
} from '../test/characterValidators';

const defaultAbilityScores: AbilityScores = {
  strength: 16,
  dexterity: 14,
  constitution: 14,
  intelligence: 12,
  wisdom: 10,
  charisma: 10,
};

describe('optimizeClassProgression', () => {
  describe('Level Distribution', () => {
    it('should give all levels to a single class', () => {
      const classes: ClassSelection[] = [
        { classId: 'fighter', className: 'Fighter', priority: 'high' },
      ];

      const result = optimizeClassProgression(
        10,
        classes,
        [],
        [],
        defaultAbilityScores,
        'melee'
      );

      expect(result).toHaveLength(10);
      expect(result.every(l => l.class.id === 'fighter')).toBe(true);
    });

    it('should distribute levels among multiple classes', () => {
      const classes: ClassSelection[] = [
        { classId: 'fighter', className: 'Fighter', priority: 'high' },
        { classId: 'wizard', className: 'Wizard', priority: 'medium' },
      ];

      const result = optimizeClassProgression(
        10,
        classes,
        [],
        [],
        defaultAbilityScores,
        'melee'
      );

      expect(result).toHaveLength(10);

      // Count class distribution
      const fighterLevels = result.filter(l => l.class.id === 'fighter').length;
      const wizardLevels = result.filter(l => l.class.id === 'wizard').length;

      expect(fighterLevels + wizardLevels).toBe(10);
      expect(fighterLevels).toBeGreaterThan(0);
      expect(wizardLevels).toBeGreaterThan(0);

      // High priority should get more levels
      expect(fighterLevels).toBeGreaterThanOrEqual(wizardLevels);
    });

    it('should respect priority weighting', () => {
      const classes: ClassSelection[] = [
        { classId: 'fighter', className: 'Fighter', priority: 'high' },
        { classId: 'rogue', className: 'Rogue', priority: 'low' },
      ];

      const result = optimizeClassProgression(
        15,
        classes,
        [],
        [],
        defaultAbilityScores,
        'melee'
      );

      const fighterLevels = result.filter(l => l.class.id === 'fighter').length;
      const rogueLevels = result.filter(l => l.class.id === 'rogue').length;

      // High priority (3x) should get significantly more than low (1x)
      expect(fighterLevels).toBeGreaterThan(rogueLevels * 2);
    });

    it('should handle three classes with different priorities', () => {
      const classes: ClassSelection[] = [
        { classId: 'fighter', className: 'Fighter', priority: 'high' },
        { classId: 'wizard', className: 'Wizard', priority: 'medium' },
        { classId: 'rogue', className: 'Rogue', priority: 'low' },
      ];

      const result = optimizeClassProgression(
        20,
        classes,
        [],
        [],
        defaultAbilityScores,
        'melee'
      );

      expect(result).toHaveLength(20);

      const fighterLevels = result.filter(l => l.class.id === 'fighter').length;
      const wizardLevels = result.filter(l => l.class.id === 'wizard').length;
      const rogueLevels = result.filter(l => l.class.id === 'rogue').length;

      expect(fighterLevels + wizardLevels + rogueLevels).toBe(20);
      // Verify priority ordering
      expect(fighterLevels).toBeGreaterThanOrEqual(wizardLevels);
      expect(wizardLevels).toBeGreaterThanOrEqual(rogueLevels);
    });
  });

  describe('Prestige Classes', () => {
    it('should handle prestige class with prerequisites', () => {
      const classes: ClassSelection[] = [
        { classId: 'fighter', className: 'Fighter', priority: 'medium' },
        { classId: 'arcane-archer', className: 'Arcane Archer', priority: 'high' },
      ];

      const result = optimizeClassProgression(
        15,
        classes,
        ['point-blank-shot', 'weapon-focus-longbow'],
        [],
        { ...defaultAbilityScores, dexterity: 13 },
        'ranged'
      );

      expect(result).toHaveLength(15);

      // Arcane Archer should not appear at level 1
      expect(result[0].class.id).not.toBe('arcane-archer');

      // Should have some levels of prestige class
      const aaLevels = result.filter(l => l.class.id === 'arcane-archer').length;
      expect(aaLevels).toBeGreaterThan(0);
    });

    it('should handle Eldritch Knight progression', () => {
      const classes: ClassSelection[] = [
        { classId: 'fighter', className: 'Fighter', priority: 'medium' },
        { classId: 'wizard', className: 'Wizard', priority: 'medium' },
        { classId: 'eldritch-knight', className: 'Eldritch Knight', priority: 'high' },
      ];

      const result = optimizeClassProgression(
        15,
        classes,
        ['weapon-focus-longsword'],
        [],
        defaultAbilityScores,
        'melee'
      );

      expect(result).toHaveLength(15);

      // Should have all three classes
      const fighterLevels = result.filter(l => l.class.id === 'fighter').length;
      const wizardLevels = result.filter(l => l.class.id === 'wizard').length;
      const ekLevels = result.filter(l => l.class.id === 'eldritch-knight').length;

      expect(fighterLevels).toBeGreaterThan(0);
      expect(wizardLevels).toBeGreaterThan(0);
      expect(ekLevels).toBeGreaterThan(0);
    });
  });

  describe('Epic Levels', () => {
    it('should support level 30 character', () => {
      const classes: ClassSelection[] = [
        { classId: 'fighter', className: 'Fighter', priority: 'high' },
      ];

      const result = optimizeClassProgression(
        30,
        classes,
        [],
        [],
        defaultAbilityScores,
        'melee'
      );

      const validation = validateTotalLevels(result, 30);
      expect(validation.valid).toBe(true);
      expect(result).toHaveLength(30);
    });

    it('should assign epic feats correctly', () => {
      const classes: ClassSelection[] = [
        { classId: 'fighter', className: 'Fighter', priority: 'high' },
      ];

      // Request enough feats to fill all feat slots (Fighter gets LOTS of feats)
      const manyFeats = [
        'power-attack', 'cleave', 'toughness', 'iron-will', 'lightning-reflexes',
        'great-fortitude', 'weapon-focus', 'improved-initiative', 'combat-casting',
        'dodge', 'mobility', 'point-blank-shot', 'precise-shot', 'rapid-shot',
        'spell-focus-evocation', 'empower-spell', 'maximize-spell', 'martial-weapon-proficiency'
      ];

      const result = optimizeClassProgression(
        25,
        classes,
        manyFeats,
        [],
        { ...defaultAbilityScores, dexterity: 13 }, // For rapid-shot
        'melee'
      );

      // Epic feats at levels 21, 24 (plus standard feats and fighter bonus feats)
      const featsAtEpicLevels = result
        .filter(l => l.levelNumber >= 21 && l.featGained)
        .map(l => l.levelNumber);

      expect(featsAtEpicLevels).toContain(21);
      expect(featsAtEpicLevels).toContain(24);
    });

    it('should have ability increases through epic levels', () => {
      const classes: ClassSelection[] = [
        { classId: 'wizard', className: 'Wizard', priority: 'high' },
      ];

      const result = optimizeClassProgression(
        28,
        classes,
        [],
        [],
        defaultAbilityScores,
        'spells'
      );

      const validation = validateAbilityIncreases(result);
      expect(validation.valid).toBe(true);

      // Should have increases at 4, 8, 12, 16, 20, 24, 28
      const increases = result
        .filter(l => l.abilityIncrease)
        .map(l => l.levelNumber);

      expect(increases).toEqual([4, 8, 12, 16, 20, 24, 28]);
    });
  });

  describe('Feat Dependencies', () => {
    it('should build feat dependency graph', () => {
      const feats = ['power-attack', 'cleave'];
      const graph = buildFeatDependencyGraph(feats);

      expect(graph.has('power-attack')).toBe(true);
      expect(graph.has('cleave')).toBe(true);

      // Cleave should have power-attack as a prerequisite
      const cleavePrereqs = graph.get('cleave') || [];
      expect(cleavePrereqs).toContain('power-attack');
    });

    it('should assign feats in prerequisite order', () => {
      const classes: ClassSelection[] = [
        { classId: 'fighter', className: 'Fighter', priority: 'high' },
      ];

      // Cleave requires Power Attack
      const result = optimizeClassProgression(
        10,
        classes,
        ['cleave'], // This will trigger power-attack to be added as prerequisite
        [],
        { ...defaultAbilityScores, strength: 13 },
        'melee'
      );

      const validation = validateFeatPrerequisites(result, {
        ...defaultAbilityScores,
        strength: 13,
      });

      expect(validation.valid).toBe(true);

      // Check feat order
      const featsInOrder = result
        .filter(l => l.featGained)
        .map(l => l.featGained);

      const powerAttackIndex = featsInOrder.indexOf('power-attack');
      const cleaveIndex = featsInOrder.indexOf('cleave');

      if (powerAttackIndex !== -1 && cleaveIndex !== -1) {
        expect(powerAttackIndex).toBeLessThan(cleaveIndex);
      }
    });
  });

  describe('Skill Optimization', () => {
    it('should front-load high skill-point classes', () => {
      const classes: ClassSelection[] = [
        { classId: 'rogue', className: 'Rogue', priority: 'medium' }, // 8 skill points
        { classId: 'fighter', className: 'Fighter', priority: 'medium' }, // 2 skill points
      ];

      const result = optimizeClassProgression(
        10,
        classes,
        [],
        [],
        defaultAbilityScores,
        'melee'
      );

      // First level should be Rogue for 4x skill multiplier
      expect(result[0].class.id).toBe('rogue');
    });

    it('should maximize skill points for INT-based builds', () => {
      const highIntScores: AbilityScores = {
        ...defaultAbilityScores,
        intelligence: 18, // +4 modifier
      };

      const classes: ClassSelection[] = [
        { classId: 'wizard', className: 'Wizard', priority: 'high' },
      ];

      const result = optimizeClassProgression(
        5,
        classes,
        [],
        [],
        highIntScores,
        'spells'
      );

      // Level 1: (2 + 4) * 4 = 24 skill points
      expect(result[0].skillPoints).toBe(24);

      // Levels 2+: 2 + 4 = 6 skill points
      for (let i = 1; i < result.length; i++) {
        expect(result[i].skillPoints).toBe(6);
      }
    });
  });
});

describe('Character Validation', () => {
  it('should produce valid level 10 Fighter', () => {
    const classes: ClassSelection[] = [
      { classId: 'fighter', className: 'Fighter', priority: 'high' },
    ];

    const result = optimizeClassProgression(
      10,
      classes,
      [],
      [],
      defaultAbilityScores,
      'melee'
    );

    const validation = validateCharacter(result, 10, defaultAbilityScores);
    if (!validation.valid) {
      console.error('Validation errors:', validation.errors);
    }
    expect(validation.valid).toBe(true);
  });

  it('should produce valid level 20 Wizard', () => {
    const classes: ClassSelection[] = [
      { classId: 'wizard', className: 'Wizard', priority: 'high' },
    ];

    const result = optimizeClassProgression(
      20,
      classes,
      [],
      [],
      defaultAbilityScores,
      'spells'
    );

    const validation = validateCharacter(result, 20, defaultAbilityScores);
    if (!validation.valid) {
      console.error('Validation errors:', validation.errors);
    }
    expect(validation.valid).toBe(true);
  });

  it('should produce valid multiclass character', () => {
    const classes: ClassSelection[] = [
      { classId: 'fighter', className: 'Fighter', priority: 'high' },
      { classId: 'wizard', className: 'Wizard', priority: 'medium' },
    ];

    const result = optimizeClassProgression(
      12,
      classes,
      ['combat-casting'],
      [],
      defaultAbilityScores,
      'melee'
    );

    const validation = validateCharacter(result, 12, defaultAbilityScores);
    if (!validation.valid) {
      console.error('Validation errors:', validation.errors);
    }
    expect(validation.valid).toBe(true);
  });

  it('should produce valid epic level character', () => {
    const classes: ClassSelection[] = [
      { classId: 'fighter', className: 'Fighter', priority: 'high' },
    ];

    const result = optimizeClassProgression(
      25,
      classes,
      [],
      [],
      defaultAbilityScores,
      'melee'
    );

    const validation = validateCharacter(result, 25, defaultAbilityScores);
    if (!validation.valid) {
      console.error('Validation errors:', validation.errors);
    }
    expect(validation.valid).toBe(true);
  });
});
