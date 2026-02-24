/**
 * Equipment Calculator
 * Recommends equipment based on character level, wealth, and build focus
 */

import { WEALTH_BY_LEVEL, EquipmentRecommendation, MagicItem } from '../types/equipment';
import { FocusType } from '../types/character';
import magicItemsData from '@data/magic-items.json';

/**
 * Get wealth available for a character of given level
 */
export function getWealthByLevel(level: number): number {
  // Clamp to valid range
  const clampedLevel = Math.max(1, Math.min(40, level));
  return WEALTH_BY_LEVEL[clampedLevel] || 0;
}

/**
 * Recommend budget allocation based on character focus
 */
export function recommendBudgetAllocation(
  totalBudget: number,
  focus: FocusType
): {
  weapons: number;
  armor: number;
  abilityItems: number;
  protectionItems: number;
  utilityItems: number;
  consumables: number;
} {
  // Base allocations (percentages)
  const allocations = {
    melee: {
      weapons: 0.30,
      armor: 0.25,
      abilityItems: 0.25,  // STR/CON items
      protectionItems: 0.15, // Rings of protection, cloaks of resistance
      utilityItems: 0.03,
      consumables: 0.02,
    },
    ranged: {
      weapons: 0.30,
      armor: 0.15,
      abilityItems: 0.30,  // DEX items
      protectionItems: 0.20,
      utilityItems: 0.03,
      consumables: 0.02,
    },
    spells: {
      weapons: 0.05,
      armor: 0.10,
      abilityItems: 0.40,  // INT/WIS/CHA items
      protectionItems: 0.30, // Very important for casters
      utilityItems: 0.10,  // Metamagic rods, etc.
      consumables: 0.05,
    },
    healing: {
      weapons: 0.10,
      armor: 0.20,
      abilityItems: 0.30,  // WIS items
      protectionItems: 0.25,
      utilityItems: 0.10,
      consumables: 0.05,
    },
    hp: {
      weapons: 0.25,
      armor: 0.30,
      abilityItems: 0.20,  // CON items
      protectionItems: 0.20,
      utilityItems: 0.03,
      consumables: 0.02,
    },
    skills: {
      weapons: 0.15,
      armor: 0.15,
      abilityItems: 0.30,  // INT/DEX items
      protectionItems: 0.20,
      utilityItems: 0.15,  // Skill-boosting items
      consumables: 0.05,
    },
  };

  const allocation = allocations[focus];

  return {
    weapons: Math.floor(totalBudget * allocation.weapons),
    armor: Math.floor(totalBudget * allocation.armor),
    abilityItems: Math.floor(totalBudget * allocation.abilityItems),
    protectionItems: Math.floor(totalBudget * allocation.protectionItems),
    utilityItems: Math.floor(totalBudget * allocation.utilityItems),
    consumables: Math.floor(totalBudget * allocation.consumables),
  };
}

/**
 * Get recommended ability score item based on focus and budget
 */
export function getRecommendedAbilityItem(
  focus: FocusType,
  budget: number
): MagicItem | null {
  const items = magicItemsData as MagicItem[];

  // Determine which ability to boost based on focus
  const abilityPriority: Record<FocusType, string[]> = {
    melee: ['strength', 'constitution', 'dexterity'],
    ranged: ['dexterity', 'strength', 'constitution'],
    spells: ['intelligence', 'wisdom', 'charisma'],
    healing: ['wisdom', 'charisma', 'constitution'],
    hp: ['constitution', 'strength', 'dexterity'],
    skills: ['intelligence', 'dexterity', 'wisdom'],
  };

  const priorities = abilityPriority[focus];

  // Find the best item we can afford for the priority ability
  for (const ability of priorities) {
    // Get all items that boost this ability, sorted by bonus (descending)
    const abilityItems = items
      .filter(item =>
        item.abilityBonuses?.some(ab => ab.ability === ability)
      )
      .sort((a, b) => {
        const bonusA = a.abilityBonuses?.find(ab => ab.ability === ability)?.bonus || 0;
        const bonusB = b.abilityBonuses?.find(ab => ab.ability === ability)?.bonus || 0;
        return bonusB - bonusA;
      });

    // Find the best one we can afford
    for (const item of abilityItems) {
      if (item.cost <= budget) {
        return item;
      }
    }
  }

  return null;
}

/**
 * Get recommended protection item (ring of protection or cloak of resistance)
 */
export function getRecommendedProtectionItem(
  budget: number,
  preferSaves: boolean = false
): MagicItem | null {
  const items = magicItemsData as MagicItem[];

  // Prioritize saves for casters, AC for frontliners
  const itemType = preferSaves ? 'cloak-resistance' : 'ring-protection';

  // Get items of this type, sorted by bonus (descending)
  const protectionItems = items
    .filter(item => item.id.startsWith(itemType))
    .sort((a, b) => {
      const valueA = a.savingThrowBonus || a.acBonus || 0;
      const valueB = b.savingThrowBonus || b.acBonus || 0;
      return valueB - valueA;
    });

  // Find the best one we can afford
  for (const item of protectionItems) {
    if (item.cost <= budget) {
      return item;
    }
  }

  return null;
}

/**
 * Generate full equipment recommendations
 */
export function generateEquipmentRecommendations(
  characterLevel: number,
  focus: FocusType
): EquipmentRecommendation {
  const totalBudget = getWealthByLevel(characterLevel);
  const allocations = recommendBudgetAllocation(totalBudget, focus);
  const recommendedItems: MagicItem[] = [];

  // Recommend ability item
  const abilityItem = getRecommendedAbilityItem(focus, allocations.abilityItems);
  if (abilityItem) {
    recommendedItems.push(abilityItem);
  }

  // Recommend protection items
  const preferSaves = focus === 'spells' || focus === 'healing';
  const protectionItem = getRecommendedProtectionItem(allocations.protectionItems, preferSaves);
  if (protectionItem) {
    recommendedItems.push(protectionItem);
  }

  // Generate reasoning
  let reasoning = `For a level ${characterLevel} ${focus}-focused character with ${totalBudget.toLocaleString()} gp:\n\n`;
  reasoning += `Budget allocation:\n`;
  reasoning += `- Weapons: ${allocations.weapons.toLocaleString()} gp\n`;
  reasoning += `- Armor: ${allocations.armor.toLocaleString()} gp\n`;
  reasoning += `- Ability items: ${allocations.abilityItems.toLocaleString()} gp\n`;
  reasoning += `- Protection items: ${allocations.protectionItems.toLocaleString()} gp\n`;
  reasoning += `- Utility items: ${allocations.utilityItems.toLocaleString()} gp\n`;
  reasoning += `- Consumables: ${allocations.consumables.toLocaleString()} gp\n\n`;
  reasoning += `Key recommendations:\n`;
  if (abilityItem) {
    reasoning += `- ${abilityItem.name} to boost your primary ability\n`;
  }
  if (protectionItem) {
    reasoning += `- ${protectionItem.name} for defense\n`;
  }
  reasoning += `\nRemaining budget should be spent on weapons, armor, and utility items based on your build.`;

  return {
    totalBudget,
    allocations,
    recommendedItems,
    reasoning,
  };
}
