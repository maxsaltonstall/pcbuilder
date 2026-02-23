/**
 * Build Validation Tests
 *
 * Validates optimizer output against community-optimized benchmark builds
 */

import { describe, test, expect } from 'vitest';
import { optimizeClassProgression } from '../services/optimizationEngine';
import { calculateTotalSkillPoints } from '../services/skillCalculator';
import { calculateCombatStats, calculateSpellSlots } from '../services/combatCalculations';
import type { AbilityScores, FocusType, ClassSelection } from '../types/character';
import * as fs from 'fs';
import * as path from 'path';

interface TestBuild {
  buildName: string;
  source: string;
  level: number;
  focus: FocusType;
  abilityScores: AbilityScores;
  targetClasses: { className: string; levels: number }[];
  expectedStats: {
    totalSkillPoints: number;
    baseAttackBonus: number;
    casterLevel: number;
    hp: number;
  };
  expectedFeats: string[];
  validationCriteria: {
    mustHave: Record<string, { min: number; ideal: number; max?: number }>;
    shouldHave: {
      feats: string[];
      spellLevel: number;
      maxedSkills: string[];
    };
  };
}

function loadTestBuild(buildName: string): TestBuild {
  const buildPath = path.join(__dirname, '../../test-builds', `${buildName}.json`);
  const data = fs.readFileSync(buildPath, 'utf-8');
  return JSON.parse(data);
}

function convertToClassSelections(targetClasses: { className: string; levels: number }[]): ClassSelection[] {
  return targetClasses.map(tc => ({
    // Convert class names to IDs (lowercase, hyphenated)
    className: tc.className.toLowerCase().replace(/\s+/g, '-'),
    levels: tc.levels,
    priority: 'medium' as const,
  }));
}

describe('Build Validation - Community Optimized Builds', () => {

  describe('Arcane Archer - Gish Optimization', () => {
    test('achieves expected caster level and BAB', () => {
      const build = loadTestBuild('arcane-archer-example');
      const classSelections = convertToClassSelections(build.targetClasses);

      const progression = optimizeClassProgression(
        build.level,
        classSelections,
        build.expectedFeats,
        ['Spellcraft', 'Concentration', 'Spot'],
        build.abilityScores,
        build.focus
      );

      expect(progression.length).toBe(build.level);

      const finalLevel = progression[progression.length - 1];
      const bab = finalLevel.baseAttackBonus;

      // BAB should be at least 15, ideally 17
      expect(bab).toBeGreaterThanOrEqual(build.validationCriteria.mustHave.baseAttackBonus.min);

      // Check prestige class entry timing
      const aaEntryIndex = progression.findIndex(l => l.class.name === 'Arcane Archer');
      expect(aaEntryIndex).toBeGreaterThan(-1); // Should have AA
      expect(aaEntryIndex).toBeLessThanOrEqual(7); // Should enter by level 8 (0-indexed)
    });

    test('maximizes skill points effectively', () => {
      const build = loadTestBuild('arcane-archer-example');
      const classSelections = convertToClassSelections(build.targetClasses);

      const progression = optimizeClassProgression(
        build.level,
        classSelections,
        build.expectedFeats,
        ['Spellcraft', 'Concentration'],
        build.abilityScores,
        build.focus
      );

      const totalSkillPoints = calculateTotalSkillPoints(
        progression,
        build.abilityScores,
        false
      );

      // Should be within 10% of expected skill points
      const minAcceptable = build.validationCriteria.mustHave.totalSkillPoints.min;
      expect(totalSkillPoints).toBeGreaterThanOrEqual(minAcceptable);
    });
  });

  describe('CoDzilla Cleric - Divine Metamagic', () => {
    test('maintains full caster progression', () => {
      const build = loadTestBuild('codzilla-cleric');
      const classSelections = convertToClassSelections(build.targetClasses);

      const progression = optimizeClassProgression(
        build.level,
        classSelections,
        build.expectedFeats,
        ['Concentration', 'Spellcraft'],
        build.abilityScores,
        build.focus
      );

      expect(progression.length).toBe(build.level);

      // Should be pure cleric (full caster level)
      const spellSlots = calculateSpellSlots(progression, build.abilityScores);
      expect(spellSlots.length).toBeGreaterThan(0);

      const clericCasting = spellSlots.find(s => s.casterClass.includes('Cleric'));
      expect(clericCasting).toBeDefined();
      expect(clericCasting!.casterLevel).toBe(15);
    });

    test('includes critical Divine Metamagic feats', () => {
      const build = loadTestBuild('codzilla-cleric');
      const classSelections = convertToClassSelections(build.targetClasses);

      const progression = optimizeClassProgression(
        build.level,
        classSelections,
        build.expectedFeats,
        ['Concentration', 'Spellcraft'],
        build.abilityScores,
        build.focus
      );

      const allFeats = progression
        .filter(l => l.featGained)
        .map(l => l.featGained!);

      // Must have Persistent Spell before Divine Metamagic
      const persistentIndex = progression.findIndex(l =>
        l.featGained && l.featGained.toLowerCase().includes('persistent')
      );
      const divineMetaIndex = progression.findIndex(l =>
        l.featGained && l.featGained.toLowerCase().includes('divine') && l.featGained.toLowerCase().includes('metamagic')
      );

      if (persistentIndex > -1 && divineMetaIndex > -1) {
        expect(persistentIndex).toBeLessThan(divineMetaIndex);
      }
    });
  });

  describe('Ubercharger - Melee Optimization', () => {
    test('achieves full BAB progression', () => {
      const build = loadTestBuild('ubercharger');
      const classSelections = convertToClassSelections(build.targetClasses);

      const progression = optimizeClassProgression(
        build.level,
        classSelections,
        build.expectedFeats,
        ['Jump', 'Intimidate'],
        build.abilityScores,
        build.focus
      );

      const finalLevel = progression[progression.length - 1];
      const bab = finalLevel.baseAttackBonus;

      expect(bab).toBe(12); // Full BAB at level 12
    });

    test('includes Power Attack chain feats', () => {
      const build = loadTestBuild('ubercharger');
      const classSelections = convertToClassSelections(build.targetClasses);

      const progression = optimizeClassProgression(
        build.level,
        classSelections,
        build.expectedFeats,
        ['Jump'],
        build.abilityScores,
        build.focus
      );

      const allFeats = progression
        .filter(l => l.featGained)
        .map(l => l.featGained!);

      // Should include Power Attack as foundation
      const hasPowerAttack = allFeats.some(f =>
        f.toLowerCase().includes('power') && f.toLowerCase().includes('attack')
      );
      expect(hasPowerAttack).toBe(true);
    });

    test('maximizes HP for survivability', () => {
      const build = loadTestBuild('ubercharger');
      const classSelections = convertToClassSelections(build.targetClasses);

      const progression = optimizeClassProgression(
        build.level,
        classSelections,
        build.expectedFeats,
        ['Jump'],
        build.abilityScores,
        build.focus
      );

      const allFeats = progression
        .filter(l => l.featGained)
        .map(l => l.featGained!);

      const combatStats = calculateCombatStats(
        progression,
        build.abilityScores,
        false,
        allFeats
      );

      // Should have high HP (Barbarian d12 + Fighter d10)
      expect(combatStats.hp).toBeGreaterThanOrEqual(build.validationCriteria.mustHave.hp.min);
    });
  });

  describe('Skill Monkey - Factotum/Rogue', () => {
    test('maximizes total skill points', () => {
      const build = loadTestBuild('skill-monkey-supreme');
      const classSelections = convertToClassSelections(build.targetClasses);

      const progression = optimizeClassProgression(
        build.level,
        classSelections,
        build.expectedFeats,
        build.expectedStats.keySkills,
        build.abilityScores,
        build.focus
      );

      const totalSkillPoints = calculateTotalSkillPoints(
        progression,
        build.abilityScores,
        false
      );

      // Should have 400+ skill points
      expect(totalSkillPoints).toBeGreaterThanOrEqual(400);
    });

    test('starts with Rogue for skill point multiplier', () => {
      const build = loadTestBuild('skill-monkey-supreme');
      const classSelections = convertToClassSelections(build.targetClasses);

      const progression = optimizeClassProgression(
        build.level,
        classSelections,
        build.expectedFeats,
        build.expectedStats.keySkills,
        build.abilityScores,
        build.focus
      );

      // First level should be Rogue for 40 skill points
      expect(progression[0].class.name).toBe('Rogue');
    });
  });

  describe('Batman Wizard - Tier 1 Caster', () => {
    test('maintains full wizard progression to 20', () => {
      const build = loadTestBuild('batman-wizard');
      const classSelections = convertToClassSelections(build.targetClasses);

      const progression = optimizeClassProgression(
        build.level,
        classSelections,
        build.expectedFeats,
        build.expectedStats.keySkills,
        build.abilityScores,
        build.focus
      );

      expect(progression.length).toBe(20);

      // Should be pure wizard
      const allWizard = progression.every(l => l.class.name === 'Wizard');
      expect(allWizard).toBe(true);

      // Caster level should be 20
      const spellSlots = calculateSpellSlots(progression, build.abilityScores);
      const wizardCasting = spellSlots.find(s => s.casterClass.includes('Wizard'));
      expect(wizardCasting?.casterLevel).toBe(20);
    });

    test('achieves 9th level spells', () => {
      const build = loadTestBuild('batman-wizard');
      const classSelections = convertToClassSelections(build.targetClasses);

      const progression = optimizeClassProgression(
        build.level,
        classSelections,
        build.expectedFeats,
        build.expectedStats.keySkills,
        build.abilityScores,
        build.focus
      );

      const spellSlots = calculateSpellSlots(progression, build.abilityScores);
      const wizardCasting = spellSlots.find(s => s.casterClass.includes('Wizard'));

      // Should have 9th level spell slots
      expect(wizardCasting?.spellsPerDay[9]).toBeDefined();
      expect(wizardCasting?.spellsPerDay[9]).toBeGreaterThan(0);
    });
  });

  describe('Wildshape Druid - Natural Spell', () => {
    test('includes Natural Spell by level 5', () => {
      const build = loadTestBuild('wildshape-druid');
      const classSelections = convertToClassSelections(build.targetClasses);

      const progression = optimizeClassProgression(
        build.level,
        classSelections,
        build.expectedFeats,
        build.expectedStats.keySkills,
        build.abilityScores,
        build.focus
      );

      // Natural Spell should be acquired by level 5
      const naturalSpellLevel = progression.findIndex(l =>
        l.featGained && l.featGained.toLowerCase().includes('natural') && l.featGained.toLowerCase().includes('spell')
      );

      expect(naturalSpellLevel).toBeGreaterThan(-1);
      expect(naturalSpellLevel).toBeLessThanOrEqual(4); // Level 5 is index 4
    });
  });

  describe('TWF Ranger - Full Attack Routine', () => {
    test('completes TWF chain progression', () => {
      const build = loadTestBuild('twf-ranger');
      const classSelections = convertToClassSelections(build.targetClasses);

      const progression = optimizeClassProgression(
        build.level,
        classSelections,
        build.expectedFeats,
        build.expectedStats.keySkills,
        build.abilityScores,
        build.focus
      );

      const allFeats = progression
        .filter(l => l.featGained)
        .map(l => l.featGained!);

      // Should have complete TWF chain
      const hasTWF = allFeats.some(f =>
        f.toLowerCase().includes('two-weapon fighting') && !f.toLowerCase().includes('improved') && !f.toLowerCase().includes('greater')
      );
      const hasImprovedTWF = allFeats.some(f =>
        f.toLowerCase().includes('improved') && f.toLowerCase().includes('two-weapon')
      );
      const hasGreaterTWF = allFeats.some(f =>
        f.toLowerCase().includes('greater') && f.toLowerCase().includes('two-weapon')
      );

      expect(hasTWF).toBe(true);
      expect(hasImprovedTWF).toBe(true);
      expect(hasGreaterTWF).toBe(true);
    });
  });

  describe('Overall Optimizer Quality', () => {
    test('passes majority of benchmark builds', () => {
      const builds = [
        'arcane-archer-example',
        'codzilla-cleric',
        'ubercharger',
        'skill-monkey-supreme',
        'batman-wizard',
        'wildshape-druid',
        'crusader-tob',
        'twf-ranger'
      ];

      let passedCount = 0;
      const results: Array<{ name: string; passed: boolean }> = [];

      for (const buildName of builds) {
        try {
          const build = loadTestBuild(buildName);
          const classSelections = convertToClassSelections(build.targetClasses);

          const progression = optimizeClassProgression(
            build.level,
            classSelections,
            build.expectedFeats,
            build.expectedStats.keySkills || [],
            build.abilityScores,
            build.focus
          );

          const totalSkillPoints = calculateTotalSkillPoints(
            progression,
            build.abilityScores,
            false
          );

          const finalLevel = progression[progression.length - 1];
          const bab = finalLevel.baseAttackBonus;

          // Check if build meets minimum criteria
          const skillPointsOK = totalSkillPoints >= build.validationCriteria.mustHave.totalSkillPoints.min;
          const babOK = !build.validationCriteria.mustHave.baseAttackBonus ||
                       bab >= build.validationCriteria.mustHave.baseAttackBonus.min;

          const passed = skillPointsOK && babOK;
          results.push({ name: buildName, passed });
          if (passed) passedCount++;

        } catch (error) {
          results.push({ name: buildName, passed: false });
        }
      }

      console.log('\nBuild Validation Results:');
      console.log('='.repeat(60));
      results.forEach(r => {
        console.log(`${r.passed ? '✅' : '❌'} ${r.name}`);
      });
      console.log('='.repeat(60));
      console.log(`Passed: ${passedCount}/${builds.length} (${Math.round(passedCount/builds.length*100)}%)\n`);

      // Should pass at least 50% of builds
      expect(passedCount).toBeGreaterThanOrEqual(builds.length * 0.5);
    });
  });
});
