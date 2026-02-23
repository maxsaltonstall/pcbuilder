import {
  Requirement,
  RequirementContext,
  AbilityRequirement,
  SkillRequirement,
  FeatRequirement,
  BaseAttackRequirement,
  CasterLevelRequirement,
  ClassLevelRequirement,
} from '../types/requirements';
import { PrestigeClass, LevelProgression } from '../types/classes';
import featsData from '@data/feats.json';
import epicFeatsData from '@data/epic-feats.json';
import prestigeClassesData from '@data/prestige-classes.json';

export interface ValidationResult {
  valid: boolean;
  errors: string[];
  warnings: string[];
}

/**
 * Validates a single requirement against a character context
 */
export function validateRequirement(
  requirement: Requirement,
  context: RequirementContext
): ValidationResult {
  const result: ValidationResult = { valid: true, errors: [], warnings: [] };

  switch (requirement.type) {
    case 'ability':
      return validateAbilityRequirement(requirement as AbilityRequirement, context);

    case 'skill':
      return validateSkillRequirement(requirement as SkillRequirement, context);

    case 'feat':
      return validateFeatRequirement(requirement as FeatRequirement, context);

    case 'baseAttackBonus':
      return validateBaseAttackRequirement(requirement as BaseAttackRequirement, context);

    case 'casterLevel':
      return validateCasterLevelRequirement(requirement as CasterLevelRequirement, context);

    case 'classLevel':
      return validateClassLevelRequirement(requirement as ClassLevelRequirement, context);

    default:
      result.warnings.push(`Unknown requirement type: ${requirement.type}`);
      return result;
  }
}

/**
 * Validates ability score requirement (e.g., Str 13)
 */
function validateAbilityRequirement(
  req: AbilityRequirement,
  context: RequirementContext
): ValidationResult {
  const result: ValidationResult = { valid: true, errors: [], warnings: [] };
  const score = context.abilityScores[req.ability];

  if (score < req.minimumScore) {
    result.valid = false;
    result.errors.push(
      `Requires ${req.ability.toUpperCase()} ${req.minimumScore}, but character has ${score}`
    );
  }

  return result;
}

/**
 * Validates skill rank requirement (e.g., 8 ranks in Disable Device)
 */
function validateSkillRequirement(
  req: SkillRequirement,
  context: RequirementContext
): ValidationResult {
  const result: ValidationResult = { valid: true, errors: [], warnings: [] };
  const ranks = context.skillRanks[req.skillId] || 0;

  if (ranks < req.minimumRanks) {
    result.valid = false;
    result.errors.push(
      `Requires ${req.minimumRanks} ranks in ${req.skillId}, but character has ${ranks}`
    );
  }

  return result;
}

/**
 * Validates feat prerequisite (e.g., must have Power Attack)
 */
function validateFeatRequirement(
  req: FeatRequirement,
  context: RequirementContext
): ValidationResult {
  const result: ValidationResult = { valid: true, errors: [], warnings: [] };
  const hasFeat = context.feats.includes(req.featId);

  if (!hasFeat) {
    result.valid = false;
    const feat = featsData.find(f => f.id === req.featId);
    result.errors.push(`Requires feat: ${feat?.name || req.featId}`);
  }

  return result;
}

/**
 * Validates base attack bonus requirement (e.g., BAB +6)
 */
function validateBaseAttackRequirement(
  req: BaseAttackRequirement,
  context: RequirementContext
): ValidationResult {
  const result: ValidationResult = { valid: true, errors: [], warnings: [] };

  if (context.baseAttackBonus < req.minimumBonus) {
    result.valid = false;
    result.errors.push(
      `Requires base attack bonus +${req.minimumBonus}, but character has +${context.baseAttackBonus}`
    );
  }

  return result;
}

/**
 * Validates caster level requirement (e.g., can cast 3rd level spells)
 */
function validateCasterLevelRequirement(
  req: CasterLevelRequirement,
  context: RequirementContext
): ValidationResult {
  const result: ValidationResult = { valid: true, errors: [], warnings: [] };

  let casterLevel = context.casterLevel;
  if (req.spellType === 'arcane') {
    casterLevel = context.arcaneCasterLevel;
  } else if (req.spellType === 'divine') {
    casterLevel = context.divineCasterLevel;
  }

  if (casterLevel < req.minimumLevel) {
    result.valid = false;
    const spellType = req.spellType ? `${req.spellType} ` : '';
    result.errors.push(
      `Requires ${spellType}caster level ${req.minimumLevel}, but character has ${casterLevel}`
    );
  }

  return result;
}

/**
 * Validates class level requirement (e.g., Fighter 4)
 */
function validateClassLevelRequirement(
  req: ClassLevelRequirement,
  context: RequirementContext
): ValidationResult {
  const result: ValidationResult = { valid: true, errors: [], warnings: [] };
  const classLevel = context.classLevels[req.classId] || 0;

  if (classLevel < req.minimumLevel) {
    result.valid = false;
    result.errors.push(
      `Requires ${req.minimumLevel} levels in ${req.classId}, but character has ${classLevel}`
    );
  }

  return result;
}

/**
 * Validates all requirements in a list
 */
export function validateAllRequirements(
  requirements: Requirement[],
  context: RequirementContext
): ValidationResult {
  const result: ValidationResult = { valid: true, errors: [], warnings: [] };

  for (const requirement of requirements) {
    const reqResult = validateRequirement(requirement, context);

    if (!reqResult.valid) {
      result.valid = false;
    }

    result.errors.push(...reqResult.errors);
    result.warnings.push(...reqResult.warnings);
  }

  return result;
}

/**
 * Build requirement context from character progression
 */
export function buildRequirementContext(
  progression: LevelProgression[],
  abilityScores: Record<string, number>
): RequirementContext {
  const context: RequirementContext = {
    abilityScores,
    skillRanks: {},
    feats: [],
    baseAttackBonus: 0,
    casterLevel: 0,
    arcaneCasterLevel: 0,
    divineCasterLevel: 0,
    classLevels: {},
  };

  // Calculate cumulative stats from progression
  for (const level of progression) {
    // Track class levels
    const classId = level.class.id;
    context.classLevels[classId] = (context.classLevels[classId] || 0) + 1;

    // Accumulate skill ranks
    for (const [skillId, ranks] of Object.entries(level.skillsAssigned || {})) {
      context.skillRanks[skillId] = (context.skillRanks[skillId] || 0) + ranks;
    }

    // Track feats
    if (level.featGained) {
      context.feats.push(level.featGained);
    }

    // Track BAB (use max from progression)
    if (level.baseAttackBonus > context.baseAttackBonus) {
      context.baseAttackBonus = level.baseAttackBonus;
    }
  }

  // Calculate caster levels (simplified - would need spell progression tables)
  const wizardLevels = context.classLevels['wizard'] || 0;
  const sorcererLevels = context.classLevels['sorcerer'] || 0;
  const clericLevels = context.classLevels['cleric'] || 0;
  const druidLevels = context.classLevels['druid'] || 0;

  context.arcaneCasterLevel = Math.max(wizardLevels, sorcererLevels);
  context.divineCasterLevel = Math.max(clericLevels, druidLevels);
  context.casterLevel = Math.max(context.arcaneCasterLevel, context.divineCasterLevel);

  return context;
}

/**
 * Check if character can take a specific feat at a given level
 */
export function canTakeFeat(
  featId: string,
  progression: LevelProgression[],
  abilityScores: Record<string, number>
): ValidationResult {
  // Check regular feats first
  let feat = featsData.find(f => f.id === featId);
  let isEpic = false;

  // If not found, check epic feats
  if (!feat) {
    feat = epicFeatsData.find(f => f.id === featId) as any;
    isEpic = true;
  }

  if (!feat) {
    return {
      valid: false,
      errors: [`Feat not found: ${featId}`],
      warnings: [],
    };
  }

  const context = buildRequirementContext(progression, abilityScores);

  // Epic feats require character level 21+
  if (isEpic && progression.length < 21) {
    return {
      valid: false,
      errors: [`Epic feats require character level 21 or higher (current level: ${progression.length})`],
      warnings: [],
    };
  }

  return validateAllRequirements(feat.prerequisites as unknown as Requirement[], context);
}

/**
 * Check if character can enter a prestige class at a given level
 */
export function canEnterPrestigeClass(
  classId: string,
  progression: LevelProgression[],
  abilityScores: Record<string, number>
): ValidationResult {
  const prestigeClass = prestigeClassesData.find(pc => pc.id === classId);

  if (!prestigeClass) {
    return {
      valid: false,
      errors: [`Prestige class not found: ${classId}`],
      warnings: [],
    };
  }

  const context = buildRequirementContext(progression, abilityScores);
  return validateAllRequirements(prestigeClass.requirements as unknown as Requirement[], context);
}

/**
 * Get minimum level at which prestige class can be entered
 * Returns -1 if prerequisites cannot be met with given classes
 */
export function getMinimumPrestigeEntryLevel(
  prestigeClass: PrestigeClass,
  _targetClasses: { classId: string; levels: number }[],
  _abilityScores: Record<string, number>
): number {
  let minLevel = 1;

  for (const req of prestigeClass.requirements) {
    if (req.type === 'baseAttackBonus') {
      const babReq = req as BaseAttackRequirement;
      // Good BAB = level, Average = 3/4 level, Poor = 1/2 level
      // Calculate minimum levels needed from base classes
      minLevel = Math.max(minLevel, babReq.minimumBonus);
    }

    if (req.type === 'skill') {
      const skillReq = req as SkillRequirement;
      // Skill ranks ≤ character level
      minLevel = Math.max(minLevel, skillReq.minimumRanks);
    }

    if (req.type === 'casterLevel') {
      const casterReq = req as CasterLevelRequirement;
      // Need at least this many caster levels
      minLevel = Math.max(minLevel, casterReq.minimumLevel);
    }
  }

  return minLevel;
}

/**
 * Check if a feat is an epic feat
 */
export function isEpicFeat(featId: string): boolean {
  return epicFeatsData.some(f => f.id === featId);
}

/**
 * Get list of all available epic feats
 */
export function getAvailableEpicFeats(
  progression: LevelProgression[],
  abilityScores: Record<string, number>
): Array<{ id: string; name: string; canTake: boolean; errors: string[] }> {
  const characterLevel = progression.length;

  // Epic feats only available at level 21+
  if (characterLevel < 21) {
    return [];
  }

  const context = buildRequirementContext(progression, abilityScores);

  return epicFeatsData.map(feat => {
    const validation = validateAllRequirements(
      feat.prerequisites as unknown as Requirement[],
      context
    );

    return {
      id: feat.id,
      name: feat.name,
      canTake: validation.valid,
      errors: validation.errors,
    };
  });
}

/**
 * Check if character can enter an epic prestige class
 */
export function canEnterEpicPrestigeClass(
  classId: string,
  progression: LevelProgression[],
  abilityScores: Record<string, number>
): ValidationResult {
  const characterLevel = progression.length;

  // Epic prestige classes require level 21+
  if (characterLevel < 21) {
    return {
      valid: false,
      errors: [`Epic prestige classes require character level 21 or higher (current level: ${characterLevel})`],
      warnings: [],
    };
  }

  // Use the same validation as regular prestige classes
  return canEnterPrestigeClass(classId, progression, abilityScores);
}
