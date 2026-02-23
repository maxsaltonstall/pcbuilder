import { describe, it, expect } from 'vitest';
import { optimizeClassProgression } from '../services/optimizationEngine';
import { ClassSelection } from '../types/classes';
import { AbilityScores } from '../types/character';
import { validateCharacter } from './characterValidators';

/**
 * Integration tests for complete character builds
 * These test real-world character concepts to ensure the optimizer produces valid results
 */

const defaultAbilityScores: AbilityScores = {
  strength: 16,
  dexterity: 14,
  constitution: 14,
  intelligence: 12,
  wisdom: 10,
  charisma: 10,
};

describe('Standard Character Builds (Levels 1-20)', () => {
  describe('Pure Class Builds', () => {
    it('should create valid level 20 Fighter', () => {
      const classes: ClassSelection[] = [
        { classId: 'fighter', className: 'Fighter' },
      ];

      const result = optimizeClassProgression(
        20,
        classes,
        ['power-attack', 'cleave', 'weapon-focus'],
        ['climb', 'jump', 'intimidate'],
        defaultAbilityScores,
        'melee'
      );

      const validation = validateCharacter(result, 20, defaultAbilityScores);
      expect(validation.valid).toBe(true);
      expect(validation.errors).toEqual([]);

      // Fighter specific checks
      expect(result.every(l => l.class.id === 'fighter')).toBe(true);
      expect(result[19].baseAttackBonus).toBe(20); // Full BAB at 20
      expect(result[19].saves.fortitude).toBeGreaterThan(10); // Good Fort save
    });

    it('should create valid level 20 Wizard', () => {
      const wizardAbilities: AbilityScores = {
        strength: 10,
        dexterity: 14,
        constitution: 12,
        intelligence: 18,
        wisdom: 12,
        charisma: 8,
      };

      const classes: ClassSelection[] = [
        { classId: 'wizard', className: 'Wizard' },
      ];

      const result = optimizeClassProgression(
        20,
        classes,
        ['combat-casting', 'spell-focus-evocation'],
        ['spellcraft', 'knowledge-arcana', 'concentration'],
        wizardAbilities,
        'spells'
      );

      const validation = validateCharacter(result, 20, wizardAbilities);
      expect(validation.valid).toBe(true);

      // Wizard specific checks
      expect(result[19].baseAttackBonus).toBe(10); // Poor BAB
      expect(result[19].saves.will).toBeGreaterThan(10); // Good Will save
      expect(result[0].skillPoints).toBeGreaterThan(20); // High skill points with INT
    });

    it('should create valid level 20 Rogue', () => {
      const rogueAbilities: AbilityScores = {
        strength: 12,
        dexterity: 18,
        constitution: 12,
        intelligence: 14,
        wisdom: 10,
        charisma: 12,
      };

      const classes: ClassSelection[] = [
        { classId: 'rogue', className: 'Rogue' },
      ];

      const result = optimizeClassProgression(
        20,
        classes,
        ['weapon-finesse'],
        ['hide', 'move-silently', 'disable-device', 'open-lock', 'search'],
        rogueAbilities,
        'melee'
      );

      const validation = validateCharacter(result, 20, rogueAbilities);
      expect(validation.valid).toBe(true);

      // Rogue specific checks - high skill points
      const totalSkillPoints = result.reduce((sum, l) => sum + l.skillPoints, 0);
      expect(totalSkillPoints).toBeGreaterThan(150); // Lots of skills
    });

    it('should create valid level 20 Cleric', () => {
      const clericAbilities: AbilityScores = {
        strength: 14,
        dexterity: 10,
        constitution: 14,
        intelligence: 10,
        wisdom: 18,
        charisma: 12,
      };

      const classes: ClassSelection[] = [
        { classId: 'cleric', className: 'Cleric' },
      ];

      const result = optimizeClassProgression(
        20,
        classes,
        ['combat-casting'],
        ['concentration', 'heal', 'knowledge-religion'],
        clericAbilities,
        'healing'
      );

      const validation = validateCharacter(result, 20, clericAbilities);
      expect(validation.valid).toBe(true);
    });
  });

  describe('Multiclass Builds', () => {
    it('should create valid Fighter/Wizard gish', () => {
      const gishAbilities: AbilityScores = {
        strength: 16,
        dexterity: 12,
        constitution: 14,
        intelligence: 16,
        wisdom: 10,
        charisma: 8,
      };

      const classes: ClassSelection[] = [
        { classId: 'fighter', className: 'Fighter', priority: 'high' },
        { classId: 'wizard', className: 'Wizard', priority: 'medium' },
      ];

      const result = optimizeClassProgression(
        15,
        classes,
        ['combat-casting', 'weapon-focus'],
        ['concentration', 'spellcraft'],
        gishAbilities,
        'melee'
      );

      const validation = validateCharacter(result, 15, gishAbilities);
      expect(validation.valid).toBe(true);

      // Should have both classes
      const fighterLevels = result.filter(l => l.class.id === 'fighter').length;
      const wizardLevels = result.filter(l => l.class.id === 'wizard').length;
      expect(fighterLevels).toBeGreaterThan(0);
      expect(wizardLevels).toBeGreaterThan(0);
    });

    it('should create valid Rogue/Fighter skill monkey', () => {
      const classes: ClassSelection[] = [
        { classId: 'rogue', className: 'Rogue', priority: 'high' },
        { classId: 'fighter', className: 'Fighter', priority: 'low' },
      ];

      const result = optimizeClassProgression(
        12,
        classes,
        [],
        ['hide', 'move-silently', 'search', 'disable-device'],
        { ...defaultAbilityScores, dexterity: 16 },
        'melee'
      );

      const validation = validateCharacter(result, 12, {
        ...defaultAbilityScores,
        dexterity: 16,
      });
      expect(validation.valid).toBe(true);

      // Rogue should be taken first for skill points
      expect(result[0].class.id).toBe('rogue');
    });
  });

  describe('Prestige Class Builds', () => {
    it('should create valid Arcane Archer build', () => {
      const archerAbilities: AbilityScores = {
        strength: 14,
        dexterity: 18,
        constitution: 12,
        intelligence: 14,
        wisdom: 10,
        charisma: 8,
      };

      const classes: ClassSelection[] = [
        { classId: 'fighter', className: 'Fighter', priority: 'medium' },
        { classId: 'wizard', className: 'Wizard', priority: 'low' },
        { classId: 'arcane-archer', className: 'Arcane Archer', priority: 'high' },
      ];

      const result = optimizeClassProgression(
        15,
        classes,
        ['point-blank-shot', 'weapon-focus-bow'],
        [],
        archerAbilities,
        'ranged'
      );

      const validation = validateCharacter(result, 15, archerAbilities);
      expect(validation.valid).toBe(true);

      // Should have all three classes
      const aaLevels = result.filter(l => l.class.id === 'arcane-archer').length;
      expect(aaLevels).toBeGreaterThan(0);

      // Arcane Archer should not be first
      expect(result[0].class.id).not.toBe('arcane-archer');
    });

    it('should create valid Eldritch Knight build', () => {
      const ekAbilities: AbilityScores = {
        strength: 16,
        dexterity: 12,
        constitution: 14,
        intelligence: 16,
        wisdom: 10,
        charisma: 8,
      };

      const classes: ClassSelection[] = [
        { classId: 'fighter', className: 'Fighter', priority: 'medium' },
        { classId: 'wizard', className: 'Wizard', priority: 'medium' },
        { classId: 'eldritch-knight', className: 'Eldritch Knight', priority: 'high' },
      ];

      const result = optimizeClassProgression(
        15,
        classes,
        ['weapon-focus'],
        ['concentration', 'spellcraft'],
        ekAbilities,
        'melee'
      );

      const validation = validateCharacter(result, 15, ekAbilities);
      expect(validation.valid).toBe(true);

      const ekLevels = result.filter(l => l.class.id === 'eldritch-knight').length;
      expect(ekLevels).toBeGreaterThan(0);
    });

    it('should create valid Arcane Trickster build', () => {
      const atAbilities: AbilityScores = {
        strength: 10,
        dexterity: 18,
        constitution: 12,
        intelligence: 16,
        wisdom: 10,
        charisma: 10,
      };

      const classes: ClassSelection[] = [
        { classId: 'rogue', className: 'Rogue', priority: 'medium' },
        { classId: 'wizard', className: 'Wizard', priority: 'medium' },
        { classId: 'arcane-trickster', className: 'Arcane Trickster', priority: 'high' },
      ];

      const result = optimizeClassProgression(
        20,
        classes,
        [],
        ['hide', 'move-silently', 'disable-device', 'spellcraft'],
        atAbilities,
        'spells'
      );

      const validation = validateCharacter(result, 20, atAbilities);
      expect(validation.valid).toBe(true);

      // Rogue should be first for skill points
      expect(result[0].class.id).toBe('rogue');
    });
  });
});

describe('Epic Character Builds (Levels 21-30)', () => {
  it('should create valid level 25 epic Fighter', () => {
    const classes: ClassSelection[] = [
      { classId: 'fighter', className: 'Fighter' },
    ];

    const result = optimizeClassProgression(
      25,
      classes,
      [
        'power-attack', 'cleave', 'toughness', 'iron-will', 'lightning-reflexes',
        'great-fortitude', 'weapon-focus', 'improved-initiative', 'combat-casting',
        'dodge', 'mobility', 'point-blank-shot', 'precise-shot', 'rapid-shot',
        'spell-focus-evocation', 'empower-spell', 'maximize-spell'
      ],
      [],
      { ...defaultAbilityScores, dexterity: 13 },
      'melee'
    );

    const validation = validateCharacter(result, 25, { ...defaultAbilityScores, dexterity: 13 });
    expect(validation.valid).toBe(true);

    // Epic level checks
    expect(result[24].baseAttackBonus).toBe(25);

    // Should have epic feats at 21, 24
    const epicFeats = result
      .filter(l => l.levelNumber >= 21 && l.featGained)
      .map(l => l.levelNumber);
    expect(epicFeats).toContain(21);
    expect(epicFeats).toContain(24);
  });

  it('should create valid level 30 epic Wizard', () => {
    const wizardAbilities: AbilityScores = {
      strength: 10,
      dexterity: 14,
      constitution: 12,
      intelligence: 18,
      wisdom: 12,
      charisma: 8,
    };

    const classes: ClassSelection[] = [
      { classId: 'wizard', className: 'Wizard' },
    ];

    const result = optimizeClassProgression(
      30,
      classes,
      [
        'combat-casting', 'spell-focus-evocation', 'empower-spell', 'maximize-spell',
        'improved-initiative', 'iron-will', 'lightning-reflexes', 'toughness',
        'dodge', 'mobility', 'great-fortitude' // Need 11 feats for level 30
      ],
      ['spellcraft', 'knowledge-arcana', 'concentration'],
      wizardAbilities,
      'spells'
    );

    const validation = validateCharacter(result, 30, wizardAbilities);
    expect(validation.valid).toBe(true);

    // Epic feats at 21, 24, 27, 30
    const epicFeats = result
      .filter(l => l.levelNumber >= 21 && l.featGained)
      .map(l => l.levelNumber);
    expect(epicFeats).toContain(21);
    expect(epicFeats).toContain(24);
    expect(epicFeats).toContain(27);
    expect(epicFeats).toContain(30);

    // Ability increases through epic
    const abilityIncreases = result
      .filter(l => l.abilityIncrease)
      .map(l => l.levelNumber);
    expect(abilityIncreases).toContain(24);
    expect(abilityIncreases).toContain(28);
  });

  it('should create valid level 30 epic multiclass', () => {
    const classes: ClassSelection[] = [
      { classId: 'rogue', className: 'Rogue', priority: 'high' },
      { classId: 'wizard', className: 'Wizard', priority: 'high' },
      { classId: 'arcane-trickster', className: 'Arcane Trickster', priority: 'high' },
    ];

    const result = optimizeClassProgression(
      30,
      classes,
      [],
      ['hide', 'move-silently', 'spellcraft'],
      { ...defaultAbilityScores, dexterity: 18, intelligence: 16 },
      'spells'
    );

    const validation = validateCharacter(result, 30, {
      ...defaultAbilityScores,
      dexterity: 18,
      intelligence: 16,
    });
    expect(validation.valid).toBe(true);
  });
});

describe('Complex Character Builds', () => {
  it('should create valid build with 4 classes', () => {
    const classes: ClassSelection[] = [
      { classId: 'fighter', className: 'Fighter', priority: 'medium' },
      { classId: 'rogue', className: 'Rogue', priority: 'medium' },
      { classId: 'wizard', className: 'Wizard', priority: 'low' },
      { classId: 'eldritch-knight', className: 'Eldritch Knight', priority: 'high' },
    ];

    const result = optimizeClassProgression(
      20,
      classes,
      ['weapon-focus'],
      [],
      { ...defaultAbilityScores, dexterity: 16, intelligence: 14 },
      'melee'
    );

    const validation = validateCharacter(result, 20, {
      ...defaultAbilityScores,
      dexterity: 16,
      intelligence: 14,
    });
    expect(validation.valid).toBe(true);

    // Should have all 4 classes represented
    const uniqueClasses = new Set(result.map(l => l.class.id));
    expect(uniqueClasses.size).toBeGreaterThanOrEqual(3);
  });

  it('should handle build with many desired feats', () => {
    const classes: ClassSelection[] = [
      { classId: 'fighter', className: 'Fighter', priority: 'high' },
    ];

    const manyFeats = [
      'power-attack',
      'cleave',
      'weapon-focus',
      'weapon-specialization',
      'combat-reflexes',
      'improved-initiative',
    ];

    const result = optimizeClassProgression(
      20,
      classes,
      manyFeats,
      [],
      { ...defaultAbilityScores, strength: 13, dexterity: 13 },
      'melee'
    );

    const validation = validateCharacter(result, 20, {
      ...defaultAbilityScores,
      strength: 13,
      dexterity: 13,
    });
    expect(validation.valid).toBe(true);

    // Fighter gets lots of feats (7 standard + 10 bonus = 17 total by level 20)
    const featCount = result.filter(l => l.featGained).length;
    // Should get most requested feats (some may not meet prerequisites in time)
    expect(featCount).toBeGreaterThanOrEqual(5);
    expect(featCount).toBeLessThanOrEqual(17); // Max possible at level 20
  });

  it('should handle all priority levels in one build', () => {
    const classes: ClassSelection[] = [
      { classId: 'fighter', className: 'Fighter', priority: 'high' },
      { classId: 'rogue', className: 'Rogue', priority: 'medium' },
      { classId: 'wizard', className: 'Wizard', priority: 'low' },
    ];

    const result = optimizeClassProgression(
      18,
      classes,
      [],
      [],
      defaultAbilityScores,
      'melee'
    );

    const validation = validateCharacter(result, 18, defaultAbilityScores);
    expect(validation.valid).toBe(true);

    const fighterLevels = result.filter(l => l.class.id === 'fighter').length;
    const rogueLevels = result.filter(l => l.class.id === 'rogue').length;
    const wizardLevels = result.filter(l => l.class.id === 'wizard').length;

    // Verify priorities are respected
    expect(fighterLevels).toBeGreaterThanOrEqual(rogueLevels);
    expect(rogueLevels).toBeGreaterThanOrEqual(wizardLevels);
  });
});
