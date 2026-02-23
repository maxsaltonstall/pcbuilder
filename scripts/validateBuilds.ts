/**
 * Build Validation Script
 *
 * Compares optimizer output against known-good benchmark builds
 * from the D&D 3.5 optimization community.
 *
 * Usage: npx tsx scripts/validateBuilds.ts [build-name]
 */

import * as fs from 'fs';
import * as path from 'path';

interface TestBuild {
  buildName: string;
  source: string;
  level: number;
  focus: string;
  abilityScores: Record<string, number>;
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

interface ValidationResult {
  buildName: string;
  passed: boolean;
  score: number;
  details: {
    skillPoints: { expected: number; actual: number; diff: number; passed: boolean };
    bab: { expected: number; actual: number; diff: number; passed: boolean };
    casterLevel: { expected: number; actual: number; diff: number; passed: boolean };
    feats: { expected: string[]; actual: string[]; missing: string[]; extra: string[]; passed: boolean };
    prestigeEntry: { expected: number; actual: number; passed: boolean };
  };
  warnings: string[];
  errors: string[];
}

/**
 * Load a test build from JSON
 */
function loadTestBuild(buildName: string): TestBuild {
  const buildPath = path.join(__dirname, '../test-builds', `${buildName}.json`);
  const data = fs.readFileSync(buildPath, 'utf-8');
  return JSON.parse(data);
}

/**
 * Run optimizer on test build
 * (This would call the actual optimization engine)
 */
function runOptimizer(testBuild: TestBuild): any {
  // TODO: Import and call actual optimization engine
  // For now, return mock data
  console.log(`Running optimizer for: ${testBuild.buildName}`);

  // This would be replaced with:
  // import { optimizeClassProgression } from '../src/services/optimizationEngine';
  // const result = optimizeClassProgression(
  //   testBuild.level,
  //   testBuild.targetClasses,
  //   testBuild.expectedFeats,
  //   []
  // );

  return {
    progression: [],
    totalSkillPoints: 0,
    baseAttackBonus: 0,
    casterLevel: 0,
    feats: [],
  };
}

/**
 * Compare optimizer output against expected results
 */
function validateBuild(testBuild: TestBuild, optimizerOutput: any): ValidationResult {
  const result: ValidationResult = {
    buildName: testBuild.buildName,
    passed: true,
    score: 0,
    details: {
      skillPoints: {
        expected: testBuild.expectedStats.totalSkillPoints,
        actual: optimizerOutput.totalSkillPoints,
        diff: 0,
        passed: false,
      },
      bab: {
        expected: testBuild.expectedStats.baseAttackBonus,
        actual: optimizerOutput.baseAttackBonus,
        diff: 0,
        passed: false,
      },
      casterLevel: {
        expected: testBuild.expectedStats.casterLevel,
        actual: optimizerOutput.casterLevel,
        diff: 0,
        passed: false,
      },
      feats: {
        expected: testBuild.expectedFeats,
        actual: optimizerOutput.feats || [],
        missing: [],
        extra: [],
        passed: false,
      },
      prestigeEntry: {
        expected: testBuild.validationCriteria.mustHave.aaEntryLevel?.ideal || 0,
        actual: 0,
        passed: false,
      },
    },
    warnings: [],
    errors: [],
  };

  // Validate skill points
  const skillPointDiff = optimizerOutput.totalSkillPoints - testBuild.expectedStats.totalSkillPoints;
  result.details.skillPoints.diff = skillPointDiff;
  result.details.skillPoints.passed = Math.abs(skillPointDiff) <= 10; // Within 10 points

  if (!result.details.skillPoints.passed) {
    result.errors.push(`Skill points off by ${skillPointDiff} (expected ${testBuild.expectedStats.totalSkillPoints}, got ${optimizerOutput.totalSkillPoints})`);
  }

  // Validate BAB
  const babDiff = optimizerOutput.baseAttackBonus - testBuild.expectedStats.baseAttackBonus;
  result.details.bab.diff = babDiff;
  result.details.bab.passed = Math.abs(babDiff) <= 1;

  if (!result.details.bab.passed) {
    result.errors.push(`BAB off by ${babDiff} (expected ${testBuild.expectedStats.baseAttackBonus}, got ${optimizerOutput.baseAttackBonus})`);
  }

  // Validate caster level
  const clDiff = optimizerOutput.casterLevel - testBuild.expectedStats.casterLevel;
  result.details.casterLevel.diff = clDiff;
  result.details.casterLevel.passed = Math.abs(clDiff) <= 1;

  if (!result.details.casterLevel.passed) {
    result.errors.push(`Caster level off by ${clDiff} (expected ${testBuild.expectedStats.casterLevel}, got ${optimizerOutput.casterLevel})`);
  }

  // Validate feats
  const actualFeats = new Set(optimizerOutput.feats || []);
  const expectedFeats = new Set(testBuild.expectedFeats);

  result.details.feats.missing = testBuild.expectedFeats.filter(f => !actualFeats.has(f));
  result.details.feats.extra = (optimizerOutput.feats || []).filter((f: string) => !expectedFeats.has(f));
  result.details.feats.passed = result.details.feats.missing.length === 0;

  if (result.details.feats.missing.length > 0) {
    result.errors.push(`Missing critical feats: ${result.details.feats.missing.join(', ')}`);
  }

  // Calculate overall score (0-100)
  let scorePoints = 0;
  if (result.details.skillPoints.passed) scorePoints += 25;
  if (result.details.bab.passed) scorePoints += 25;
  if (result.details.casterLevel.passed) scorePoints += 25;
  if (result.details.feats.passed) scorePoints += 25;

  result.score = scorePoints;
  result.passed = result.score >= 75; // Must pass at least 3 out of 4 criteria

  return result;
}

/**
 * Print validation results
 */
function printResults(result: ValidationResult): void {
  console.log('\n' + '='.repeat(60));
  console.log(`Build: ${result.buildName}`);
  console.log('='.repeat(60));

  const statusEmoji = result.passed ? '✅' : '❌';
  console.log(`\nOverall: ${statusEmoji} ${result.passed ? 'PASSED' : 'FAILED'} (Score: ${result.score}/100)`);

  console.log('\nDetailed Results:');
  console.log(`  Skill Points: ${result.details.skillPoints.passed ? '✅' : '❌'} ${result.details.skillPoints.actual} (expected ${result.details.skillPoints.expected}, diff: ${result.details.skillPoints.diff})`);
  console.log(`  Base Attack:  ${result.details.bab.passed ? '✅' : '❌'} +${result.details.bab.actual} (expected +${result.details.bab.expected}, diff: ${result.details.bab.diff})`);
  console.log(`  Caster Level: ${result.details.casterLevel.passed ? '✅' : '❌'} ${result.details.casterLevel.actual} (expected ${result.details.casterLevel.expected}, diff: ${result.details.casterLevel.diff})`);
  console.log(`  Feats:        ${result.details.feats.passed ? '✅' : '❌'} ${result.details.feats.actual.length}/${result.details.feats.expected.length} critical feats`);

  if (result.details.feats.missing.length > 0) {
    console.log(`    Missing: ${result.details.feats.missing.join(', ')}`);
  }

  if (result.warnings.length > 0) {
    console.log('\n⚠️  Warnings:');
    result.warnings.forEach(w => console.log(`    - ${w}`));
  }

  if (result.errors.length > 0) {
    console.log('\n❌ Errors:');
    result.errors.forEach(e => console.log(`    - ${e}`));
  }

  console.log('\n');
}

/**
 * Run validation on all test builds
 */
function validateAllBuilds(): void {
  const testBuildsDir = path.join(__dirname, '../test-builds');
  const buildFiles = fs.readdirSync(testBuildsDir).filter(f => f.endsWith('.json'));

  console.log(`Found ${buildFiles.length} test build(s)\n`);

  const results: ValidationResult[] = [];

  for (const buildFile of buildFiles) {
    const buildName = buildFile.replace('.json', '');
    const testBuild = loadTestBuild(buildName);
    const optimizerOutput = runOptimizer(testBuild);
    const result = validateBuild(testBuild, optimizerOutput);

    printResults(result);
    results.push(result);
  }

  // Summary
  const passed = results.filter(r => r.passed).length;
  const total = results.length;
  const avgScore = results.reduce((sum, r) => sum + r.score, 0) / total;

  console.log('='.repeat(60));
  console.log('SUMMARY');
  console.log('='.repeat(60));
  console.log(`Passed: ${passed}/${total} (${Math.round(passed/total*100)}%)`);
  console.log(`Average Score: ${avgScore.toFixed(1)}/100`);
  console.log('');
}

// CLI execution
const args = process.argv.slice(2);

if (args.length === 0) {
  console.log('Running validation on all test builds...');
  validateAllBuilds();
} else {
  const buildName = args[0];
  console.log(`Running validation on: ${buildName}`);
  const testBuild = loadTestBuild(buildName);
  const optimizerOutput = runOptimizer(testBuild);
  const result = validateBuild(testBuild, optimizerOutput);
  printResults(result);
}
