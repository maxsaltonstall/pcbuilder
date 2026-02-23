// Utility to extract all unique source books from the data files

interface DataElement {
  source?: string;
}

export interface SourceGroup {
  category: string;
  sources: string[];
}

// Import all data files
import classesData from '../../data/classes.json';
import featsData from '../../data/feats.json';
import prestigeClassesData from '../../data/prestige-classes.json';
import spellsData from '../../data/spells.json';
import soulmeldData from '../../data/soulmelds.json';
import martialDisciplinesData from '../../data/martial-disciplines.json';

/**
 * Extracts all unique source books from the game data files
 * @returns Sorted array of unique source book names
 */
export function getAvailableSources(): string[] {
  const sources = new Set<string>();

  // Aggregate sources from all data files
  const allData: DataElement[][] = [
    classesData,
    featsData,
    prestigeClassesData,
    spellsData,
    soulmeldData,
    martialDisciplinesData,
  ];

  for (const dataArray of allData) {
    if (Array.isArray(dataArray)) {
      for (const item of dataArray) {
        if (item.source && typeof item.source === 'string') {
          sources.add(item.source);
        }
      }
    }
  }

  // Convert to sorted array
  return Array.from(sources).sort();
}

/**
 * Gets sources organized by category
 * @returns Array of source groups with category names
 */
export function getGroupedSources(): SourceGroup[] {
  const allSources = getAvailableSources();
  const groups: SourceGroup[] = [];

  // Define categorization rules
  const categories = {
    'Core Rules': (s: string) =>
      s.includes("Player's Handbook") || s.includes("Dungeon Master"),
    'Complete Series': (s: string) =>
      s.startsWith('Complete '),
    'Expansion Books': (s: string) =>
      s.includes('Epic Level') || s.includes('Expanded Psionics'),
    'Magic Systems': (s: string) =>
      s.includes('Magic of Incarnum') || s.includes('Tome of Battle') || s.includes('Dragon Magic'),
    'Fiendish & Undead': (s: string) =>
      s.includes('Fiendish Codex') || s.includes('Libris Mortis'),
    'Environment Books': (s: string) =>
      ['Sandstorm', 'Frostburn', 'Stormwrack'].some(env => s.includes(env)),
    'Racial Books': (s: string) =>
      s.startsWith('Races of'),
    'Monster & Aberration': (s: string) =>
      s.includes('Lords of Madness'),
    'Spell References': (s: string) =>
      s.includes('Spell Compendium'),
  };

  const categorized = new Set<string>();

  // Group sources by category
  for (const [category, matcher] of Object.entries(categories)) {
    const matchingSources = allSources.filter(source => {
      if (categorized.has(source)) return false;
      if (matcher(source)) {
        categorized.add(source);
        return true;
      }
      return false;
    });

    if (matchingSources.length > 0) {
      groups.push({ category, sources: matchingSources });
    }
  }

  // Add any uncategorized sources
  const uncategorized = allSources.filter(s => !categorized.has(s));
  if (uncategorized.length > 0) {
    groups.push({ category: 'Other Sources', sources: uncategorized });
  }

  return groups;
}

/**
 * Gets core/essential sources that should be selected by default
 * @returns Array of core source book names
 */
export function getCoreSources(): string[] {
  const allSources = getAvailableSources();
  const coreKeywords = ["Player's Handbook", 'Dungeon Master', 'DMG'];

  return allSources.filter(source =>
    coreKeywords.some(keyword => source.includes(keyword))
  );
}
