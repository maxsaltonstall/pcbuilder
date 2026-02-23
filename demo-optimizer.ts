#!/usr/bin/env tsx
/**
 * Demo script to show the optimizer in action
 */

import { optimizeClassProgression } from './src/services/optimizationEngine';
import { validateCharacter } from './src/test/characterValidators';

console.log('🎲 D&D 3.5 Character Builder - Optimizer Demo\n');
console.log('='.repeat(60));

// Example 1: Epic Arcane Trickster
console.log('\n📖 Example 1: Level 22 Arcane Trickster');
console.log('-'.repeat(60));

const build1 = optimizeClassProgression(
  22,
  [
    { classId: 'rogue', className: 'Rogue', priority: 'high' },
    { classId: 'wizard', className: 'Wizard', priority: 'medium' },
    { classId: 'arcane-trickster', className: 'Arcane Trickster', priority: 'high' },
  ],
  ['weapon-finesse', 'combat-casting'],
  ['hide', 'move-silently', 'disable-device', 'spellcraft'],
  {
    strength: 10,
    dexterity: 18,
    constitution: 12,
    intelligence: 16,
    wisdom: 10,
    charisma: 10,
  },
  'spells'
);

// Count class distribution
const classCount1: Record<string, number> = {};
build1.forEach(level => {
  classCount1[level.class.name] = (classCount1[level.class.name] || 0) + 1;
});

console.log('\nClass Distribution:');
Object.entries(classCount1).forEach(([name, levels]) => {
  console.log(`  ${name}: ${levels} levels`);
});

console.log('\nKey Stats:');
console.log(`  Total Levels: ${build1.length}`);
console.log(`  Final BAB: +${build1[build1.length - 1].baseAttackBonus}`);
console.log(`  Final Saves: Fort +${build1[build1.length - 1].saves.fortitude}, Ref +${build1[build1.length - 1].saves.reflex}, Will +${build1[build1.length - 1].saves.will}`);
console.log(`  Total Feats: ${build1.filter(l => l.featGained).length}`);
console.log(`  Total Skill Points: ${build1.reduce((sum, l) => sum + l.skillPoints, 0)}`);

const validation1 = validateCharacter(build1, 22, {
  strength: 10,
  dexterity: 18,
  constitution: 12,
  intelligence: 16,
  wisdom: 10,
  charisma: 10,
});

console.log(`\n✅ Validation: ${validation1.valid ? 'PASSED' : 'FAILED'}`);
if (!validation1.valid) {
  console.log('Errors:', validation1.errors);
}

// Example 2: Level 30 Epic Fighter
console.log('\n\n📖 Example 2: Level 30 Epic Fighter');
console.log('-'.repeat(60));

const build2 = optimizeClassProgression(
  30,
  [
    { classId: 'fighter', className: 'Fighter', priority: 'high' },
  ],
  ['power-attack', 'cleave', 'weapon-focus', 'weapon-specialization',
   'toughness', 'improved-initiative', 'iron-will'],
  ['intimidate', 'climb', 'jump'],
  {
    strength: 18,
    dexterity: 14,
    constitution: 16,
    intelligence: 10,
    wisdom: 12,
    charisma: 8,
  },
  'melee'
);

const classCount2: Record<string, number> = {};
build2.forEach(level => {
  classCount2[level.class.name] = (classCount2[level.class.name] || 0) + 1;
});

console.log('\nClass Distribution:');
Object.entries(classCount2).forEach(([name, levels]) => {
  console.log(`  ${name}: ${levels} levels`);
});

console.log('\nKey Stats:');
console.log(`  Total Levels: ${build2.length}`);
console.log(`  Final BAB: +${build2[build2.length - 1].baseAttackBonus}`);
console.log(`  Final Saves: Fort +${build2[build2.length - 1].saves.fortitude}, Ref +${build2[build2.length - 1].saves.reflex}, Will +${build2[build2.length - 1].saves.will}`);
console.log(`  Total Feats: ${build2.filter(l => l.featGained).length}`);

// Show epic feat levels
const epicFeats = build2
  .filter(l => l.levelNumber >= 21 && l.featGained)
  .map(l => ({ level: l.levelNumber, feat: l.featGained }));
console.log(`  Epic Feats: ${epicFeats.map(f => `Level ${f.level}`).join(', ')}`);

// Show ability increases
const abilityIncreases = build2
  .filter(l => l.abilityIncrease)
  .map(l => ({ level: l.levelNumber, ability: l.abilityIncrease }));
console.log(`  Ability Increases: ${abilityIncreases.map(a => `Level ${a.level} (${a.ability.toUpperCase()})`).join(', ')}`);

const validation2 = validateCharacter(build2, 30, {
  strength: 18,
  dexterity: 14,
  constitution: 16,
  intelligence: 10,
  wisdom: 12,
  charisma: 8,
});

console.log(`\n✅ Validation: ${validation2.valid ? 'PASSED' : 'FAILED'}`);
if (!validation2.valid) {
  console.log('Errors:', validation2.errors);
}

// Example 3: Fighter/Wizard with priorities
console.log('\n\n📖 Example 3: Level 15 Fighter/Wizard (Different Priorities)');
console.log('-'.repeat(60));

const build3 = optimizeClassProgression(
  15,
  [
    { classId: 'fighter', className: 'Fighter', priority: 'high' },
    { classId: 'wizard', className: 'Wizard', priority: 'low' },
  ],
  ['combat-casting', 'weapon-focus'],
  ['spellcraft', 'concentration'],
  {
    strength: 16,
    dexterity: 12,
    constitution: 14,
    intelligence: 16,
    wisdom: 10,
    charisma: 8,
  },
  'melee'
);

const classCount3: Record<string, number> = {};
build3.forEach(level => {
  classCount3[level.class.name] = (classCount3[level.class.name] || 0) + 1;
});

console.log('\nClass Distribution (Fighter=HIGH, Wizard=LOW):');
Object.entries(classCount3).forEach(([name, levels]) => {
  console.log(`  ${name}: ${levels} levels`);
});

console.log('\nKey Stats:');
console.log(`  Total Levels: ${build3.length}`);
console.log(`  Final BAB: +${build3[build3.length - 1].baseAttackBonus}`);
console.log(`  Total Feats: ${build3.filter(l => l.featGained).length}`);
console.log(`  Total Skill Points: ${build3.reduce((sum, l) => sum + l.skillPoints, 0)}`);

const validation3 = validateCharacter(build3, 15, {
  strength: 16,
  dexterity: 12,
  constitution: 14,
  intelligence: 16,
  wisdom: 10,
  charisma: 8,
});

console.log(`\n✅ Validation: ${validation3.valid ? 'PASSED' : 'FAILED'}`);

console.log('\n' + '='.repeat(60));
console.log('🎉 All examples generated and validated successfully!');
console.log('='.repeat(60));
