import { FocusType } from '../types/character';

export interface EquipmentItem {
  name: string;
  slot: string;
  bonus: string;
  cost: number;
  reason: string;
}

/**
 * Recommend equipment based on character level, wealth-by-level, and build focus
 * Based on D&D 3.5 DMG Table 5-1: Character Wealth by Level
 */
export function recommendEquipment(
  characterLevel: number,
  focus: FocusType,
  assumeMagicItems: boolean
): EquipmentItem[] {
  if (!assumeMagicItems) {
    return [];
  }

  const equipment: EquipmentItem[] = [];

  // The "Big 6" magic items (priority order for spending)
  // 1. Weapon enhancement
  // 2. Armor enhancement
  // 3. Ability score booster (primary stat)
  // 4. Cloak of Resistance
  // 5. Ring of Protection
  // 6. Amulet of Natural Armor

  // Weapon (varies by focus)
  addWeapon(equipment, characterLevel, focus);

  // Armor and Shield
  addArmor(equipment, characterLevel, focus);

  // Ability Score Boosters
  addAbilityBoosters(equipment, characterLevel, focus);

  // Cloak of Resistance (universal)
  addCloakOfResistance(equipment, characterLevel);

  // Ring of Protection (universal)
  addRingOfProtection(equipment, characterLevel);

  // Amulet of Natural Armor (universal)
  addAmuletOfNaturalArmor(equipment, characterLevel);

  // Miscellaneous useful items
  addMiscItems(equipment, characterLevel, focus);

  return equipment;
}

export function getWealthByLevel(level: number): number {
  // Simplified wealth-by-level from DMG Table 5-1 (in gp)
  if (level <= 1) return 0;
  if (level === 2) return 900;
  if (level === 3) return 2700;
  if (level === 4) return 5400;
  if (level === 5) return 9000;
  if (level === 6) return 13000;
  if (level === 7) return 19000;
  if (level === 8) return 27000;
  if (level === 9) return 36000;
  if (level === 10) return 49000;
  if (level === 11) return 66000;
  if (level === 12) return 88000;
  if (level === 13) return 110000;
  if (level === 14) return 150000;
  if (level === 15) return 200000;
  if (level === 16) return 260000;
  if (level === 17) return 340000;
  if (level === 18) return 440000;
  if (level === 19) return 580000;
  if (level === 20) return 760000;
  // Epic levels - exponential growth
  return 760000 * Math.pow(1.5, level - 20);
}

function addWeapon(items: EquipmentItem[], level: number, focus: FocusType) {
  let weaponType = 'Longsword';
  let reason = 'Versatile melee weapon';

  if (focus === 'ranged') {
    weaponType = 'Composite Longbow';
    reason = 'Primary ranged weapon';
  } else if (focus === 'spells' || focus === 'healing') {
    weaponType = 'Quarterstaff';
    reason = 'Simple backup weapon for casters';
  }

  if (level >= 3) {
    items.push({
      name: `${weaponType} +1`,
      slot: 'Weapon',
      bonus: '+1 enhancement',
      cost: 2000,
      reason,
    });
  }

  if (level >= 6) {
    // Upgrade to +2
    items[items.length - 1] = {
      name: `${weaponType} +2`,
      slot: 'Weapon',
      bonus: '+2 enhancement',
      cost: 8000,
      reason,
    };
  }

  if (level >= 9) {
    // Upgrade to +3
    items[items.length - 1] = {
      name: `${weaponType} +3`,
      slot: 'Weapon',
      bonus: '+3 enhancement',
      cost: 18000,
      reason,
    };
  }

  if (level >= 12) {
    // Upgrade to +4
    items[items.length - 1] = {
      name: `${weaponType} +4`,
      slot: 'Weapon',
      bonus: '+4 enhancement',
      cost: 32000,
      reason,
    };
  }

  if (level >= 15) {
    // Upgrade to +5
    items[items.length - 1] = {
      name: `${weaponType} +5`,
      slot: 'Weapon',
      bonus: '+5 enhancement',
      cost: 50000,
      reason,
    };
  }
}

function addArmor(items: EquipmentItem[], level: number, focus: FocusType) {
  // Spellcasters avoid armor (arcane spell failure)
  if (focus === 'spells' || focus === 'healing') {
    if (level >= 4) {
      items.push({
        name: 'Bracers of Armor +1',
        slot: 'Wrists',
        bonus: '+1 armor',
        cost: 1000,
        reason: 'AC bonus without spell failure',
      });
    }
    if (level >= 8) {
      items[items.length - 1] = {
        name: 'Bracers of Armor +3',
        slot: 'Wrists',
        bonus: '+3 armor',
        cost: 9000,
        reason: 'AC bonus without spell failure',
      };
    }
    if (level >= 12) {
      items[items.length - 1] = {
        name: 'Bracers of Armor +5',
        slot: 'Wrists',
        bonus: '+5 armor',
        cost: 25000,
        reason: 'AC bonus without spell failure',
      };
    }
    return;
  }

  // Melee/HP builds: heavier armor
  if (focus === 'melee' || focus === 'hp') {
    if (level >= 3) {
      items.push({
        name: 'Chainmail +1',
        slot: 'Armor',
        bonus: '+1 enhancement',
        cost: 1300,
        reason: 'Medium armor with good protection',
      });
    }
    if (level >= 5) {
      items[items.length - 1] = {
        name: 'Breastplate +1',
        slot: 'Armor',
        bonus: '+1 enhancement',
        cost: 1350,
        reason: 'Better medium armor (lower ACP)',
      };
    }
    if (level >= 8) {
      items[items.length - 1] = {
        name: 'Breastplate +2',
        slot: 'Armor',
        bonus: '+2 enhancement',
        cost: 4350,
        reason: 'Enhanced protection',
      };
    }
    if (level >= 12) {
      items[items.length - 1] = {
        name: 'Full Plate +2',
        slot: 'Armor',
        bonus: '+2 enhancement',
        cost: 5650,
        reason: 'Maximum armor protection',
      };
    }
    if (level >= 15) {
      items[items.length - 1] = {
        name: 'Full Plate +3',
        slot: 'Armor',
        bonus: '+3 enhancement',
        cost: 10650,
        reason: 'Elite armor protection',
      };
    }
  }

  // Ranged builds: lighter armor for mobility
  if (focus === 'ranged') {
    if (level >= 3) {
      items.push({
        name: 'Chain Shirt +1',
        slot: 'Armor',
        bonus: '+1 enhancement',
        cost: 1250,
        reason: 'Light armor for mobility',
      });
    }
    if (level >= 5) {
      items[items.length - 1] = {
        name: 'Chain Shirt +2',
        slot: 'Armor',
        bonus: '+2 enhancement',
        cost: 4250,
        reason: 'Enhanced light armor',
      };
    }
    if (level >= 10) {
      items[items.length - 1] = {
        name: 'Mithral Breastplate +2',
        slot: 'Armor',
        bonus: '+2 enhancement',
        cost: 8350,
        reason: 'No ACP, counts as light armor',
      };
    }
    if (level >= 15) {
      items[items.length - 1] = {
        name: 'Mithral Breastplate +3',
        slot: 'Armor',
        bonus: '+3 enhancement',
        cost: 13350,
        reason: 'Elite light armor',
      };
    }
  }

  // Shield (for melee/hp builds)
  if (focus === 'melee' || focus === 'hp') {
    if (level >= 4) {
      items.push({
        name: 'Heavy Steel Shield',
        slot: 'Shield',
        bonus: '+2 shield',
        cost: 20,
        reason: 'Additional AC',
      });
    }
    if (level >= 10) {
      items[items.length - 1] = {
        name: 'Heavy Steel Shield +1',
        slot: 'Shield',
        bonus: '+3 shield',
        cost: 1170,
        reason: 'Enhanced shield',
      };
    }
    if (level >= 15) {
      items[items.length - 1] = {
        name: 'Heavy Steel Shield +2',
        slot: 'Shield',
        bonus: '+4 shield',
        cost: 4170,
        reason: 'Superior shield protection',
      };
    }
  }
}

function addAbilityBoosters(items: EquipmentItem[], level: number, focus: FocusType) {
  // Primary stat booster
  let primaryStat = 'Strength';
  let reason = 'Boost primary attack stat';

  if (focus === 'ranged') {
    primaryStat = 'Dexterity';
    reason = 'Boost ranged attack and AC';
  } else if (focus === 'spells') {
    primaryStat = 'Intelligence'; // or Charisma/Wisdom depending on class
    reason = 'Boost spell DC and slots';
  } else if (focus === 'healing') {
    primaryStat = 'Wisdom';
    reason = 'Boost healing and spell DC';
  }

  if (level >= 5) {
    items.push({
      name: `${primaryStat === 'Intelligence' ? 'Headband' : primaryStat === 'Wisdom' || primaryStat === 'Charisma' ? 'Periapt/Cloak' : 'Belt/Gauntlets'} of ${primaryStat} +2`,
      slot: 'Head/Waist',
      bonus: `+2 ${primaryStat}`,
      cost: 4000,
      reason,
    });
  }

  if (level >= 8) {
    items[items.length - 1] = {
      name: `${primaryStat === 'Intelligence' ? 'Headband' : primaryStat === 'Wisdom' || primaryStat === 'Charisma' ? 'Periapt/Cloak' : 'Belt/Gauntlets'} of ${primaryStat} +4`,
      slot: 'Head/Waist',
      bonus: `+4 ${primaryStat}`,
      cost: 16000,
      reason,
    };
  }

  if (level >= 12) {
    items[items.length - 1] = {
      name: `${primaryStat === 'Intelligence' ? 'Headband' : primaryStat === 'Wisdom' || primaryStat === 'Charisma' ? 'Periapt/Cloak' : 'Belt/Gauntlets'} of ${primaryStat} +6`,
      slot: 'Head/Waist',
      bonus: `+6 ${primaryStat}`,
      cost: 36000,
      reason,
    };
  }

  // Constitution booster (universal)
  if (level >= 6) {
    items.push({
      name: 'Amulet of Health +2',
      slot: 'Neck',
      bonus: '+2 Constitution',
      cost: 4000,
      reason: 'More HP and better Fort saves',
    });
  }

  if (level >= 10) {
    items[items.length - 1] = {
      name: 'Amulet of Health +4',
      slot: 'Neck',
      bonus: '+4 Constitution',
      cost: 16000,
      reason: 'Significantly more HP',
    };
  }

  if (level >= 14) {
    items[items.length - 1] = {
      name: 'Amulet of Health +6',
      slot: 'Neck',
      bonus: '+6 Constitution',
      cost: 36000,
      reason: 'Maximum HP boost',
    };
  }
}

function addCloakOfResistance(items: EquipmentItem[], level: number) {
  if (level >= 3) {
    items.push({
      name: 'Cloak of Resistance +1',
      slot: 'Shoulders',
      bonus: '+1 all saves',
      cost: 1000,
      reason: 'Essential save boost',
    });
  }

  if (level >= 7) {
    items[items.length - 1] = {
      name: 'Cloak of Resistance +2',
      slot: 'Shoulders',
      bonus: '+2 all saves',
      cost: 4000,
      reason: 'Better save protection',
    };
  }

  if (level >= 11) {
    items[items.length - 1] = {
      name: 'Cloak of Resistance +3',
      slot: 'Shoulders',
      bonus: '+3 all saves',
      cost: 9000,
      reason: 'Strong save protection',
    };
  }

  if (level >= 15) {
    items[items.length - 1] = {
      name: 'Cloak of Resistance +4',
      slot: 'Shoulders',
      bonus: '+4 all saves',
      cost: 16000,
      reason: 'Elite save protection',
    };
  }

  if (level >= 18) {
    items[items.length - 1] = {
      name: 'Cloak of Resistance +5',
      slot: 'Shoulders',
      bonus: '+5 all saves',
      cost: 25000,
      reason: 'Maximum save protection',
    };
  }
}

function addRingOfProtection(items: EquipmentItem[], level: number) {
  if (level >= 5) {
    items.push({
      name: 'Ring of Protection +1',
      slot: 'Ring',
      bonus: '+1 deflection to AC',
      cost: 2000,
      reason: 'Deflection bonus to AC',
    });
  }

  if (level >= 10) {
    items[items.length - 1] = {
      name: 'Ring of Protection +2',
      slot: 'Ring',
      bonus: '+2 deflection to AC',
      cost: 8000,
      reason: 'Better deflection bonus',
    };
  }

  if (level >= 15) {
    items[items.length - 1] = {
      name: 'Ring of Protection +3',
      slot: 'Ring',
      bonus: '+3 deflection to AC',
      cost: 18000,
      reason: 'Strong AC boost',
    };
  }

  if (level >= 20) {
    items[items.length - 1] = {
      name: 'Ring of Protection +4',
      slot: 'Ring',
      bonus: '+4 deflection to AC',
      cost: 32000,
      reason: 'Elite AC protection',
    };
  }
}

function addAmuletOfNaturalArmor(items: EquipmentItem[], level: number) {
  if (level >= 6) {
    items.push({
      name: 'Amulet of Natural Armor +1',
      slot: 'Neck (alt)',
      bonus: '+1 natural armor',
      cost: 2000,
      reason: 'Natural armor bonus to AC',
    });
  }

  if (level >= 10) {
    items[items.length - 1] = {
      name: 'Amulet of Natural Armor +2',
      slot: 'Neck (alt)',
      bonus: '+2 natural armor',
      cost: 8000,
      reason: 'Better natural armor',
    };
  }

  if (level >= 15) {
    items[items.length - 1] = {
      name: 'Amulet of Natural Armor +3',
      slot: 'Neck (alt)',
      bonus: '+3 natural armor',
      cost: 18000,
      reason: 'Strong natural armor',
    };
  }

  if (level >= 20) {
    items[items.length - 1] = {
      name: 'Amulet of Natural Armor +4',
      slot: 'Neck (alt)',
      bonus: '+4 natural armor',
      cost: 32000,
      reason: 'Elite natural armor',
    };
  }
}

function addMiscItems(items: EquipmentItem[], level: number, focus: FocusType) {
  // Utility items
  if (level >= 4) {
    items.push({
      name: 'Handy Haversack',
      slot: 'Back',
      bonus: 'Extra-dimensional storage',
      cost: 2000,
      reason: 'Convenient item storage',
    });
  }

  if (level >= 7 && (focus === 'spells' || focus === 'healing')) {
    items.push({
      name: 'Pearl of Power (1st)',
      slot: 'None',
      bonus: 'Recall 1st level spell',
      cost: 1000,
      reason: 'Extra spell slot utility',
    });
  }

  if (level >= 9) {
    items.push({
      name: 'Boots of Speed',
      slot: 'Feet',
      bonus: 'Haste 10 rounds/day',
      cost: 12000,
      reason: 'Combat mobility and extra attacks',
    });
  }

  if (level >= 12 && focus === 'melee') {
    items.push({
      name: 'Gloves of Dexterity +2',
      slot: 'Hands',
      bonus: '+2 Dexterity',
      cost: 4000,
      reason: 'Improve initiative and AC',
    });
  }
}
