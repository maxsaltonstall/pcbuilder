/**
 * Character Storage Service
 * Handles saving and loading characters to/from JSON files
 */

import { CharacterState } from '../types/character';

export interface SavedCharacter extends CharacterState {
  version: string;
  savedAt: string;
  characterName?: string;
}

/**
 * Export character to JSON string
 */
export function exportCharacterToJSON(state: CharacterState, characterName?: string): string {
  const savedCharacter: SavedCharacter = {
    ...state,
    version: '1.0.0',
    savedAt: new Date().toISOString(),
    characterName: characterName || state.concept || 'Unnamed Character',
  };

  return JSON.stringify(savedCharacter, null, 2);
}

/**
 * Import character from JSON string
 */
export function importCharacterFromJSON(jsonString: string): SavedCharacter {
  const parsed = JSON.parse(jsonString);

  // Validate required fields
  if (!parsed.totalLevel || !parsed.concept) {
    throw new Error('Invalid character file: missing required fields');
  }

  // Version compatibility check
  if (parsed.version && parsed.version !== '1.0.0') {
    console.warn(`Character saved with version ${parsed.version}, current version is 1.0.0`);
  }

  return parsed as SavedCharacter;
}

/**
 * Generate filename for character
 */
export function generateFilename(characterName: string): string {
  const sanitized = characterName
    .replace(/[^a-z0-9]/gi, '-')
    .replace(/-+/g, '-')
    .toLowerCase();
  const date = new Date().toISOString().split('T')[0];
  return `${sanitized}-${date}.json`;
}

/**
 * Save character to file (browser download)
 */
export function saveCharacterToFile(state: CharacterState, characterName?: string): void {
  const json = exportCharacterToJSON(state, characterName);
  const blob = new Blob([json], { type: 'application/json' });
  const url = URL.createObjectURL(blob);

  const link = document.createElement('a');
  link.href = url;
  link.download = generateFilename(characterName || state.concept || 'character');
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
  URL.revokeObjectURL(url);
}

/**
 * Load character from file (browser file picker)
 */
export function loadCharacterFromFile(): Promise<SavedCharacter> {
  return new Promise((resolve, reject) => {
    const input = document.createElement('input');
    input.type = 'file';
    input.accept = '.json';

    input.onchange = (e) => {
      const file = (e.target as HTMLInputElement).files?.[0];
      if (!file) {
        reject(new Error('No file selected'));
        return;
      }

      const reader = new FileReader();
      reader.onload = (event) => {
        try {
          const json = event.target?.result as string;
          const character = importCharacterFromJSON(json);
          resolve(character);
        } catch (error) {
          reject(error);
        }
      };
      reader.onerror = () => reject(new Error('Failed to read file'));
      reader.readAsText(file);
    };

    input.click();
  });
}

// ============================================
// LocalStorage Functions (Auto-save)
// ============================================

const STORAGE_KEY = 'dnd-character-builder-autosave';
const STORAGE_LIST_KEY = 'dnd-character-builder-saved-list';

/**
 * Save character to localStorage (auto-save)
 */
export function saveCharacterToLocalStorage(state: CharacterState, characterName?: string): void {
  try {
    const json = exportCharacterToJSON(state, characterName);
    localStorage.setItem(STORAGE_KEY, json);

    // Also add to saved characters list
    const list = getSavedCharactersList();
    const id = `char-${Date.now()}`;
    const entry = {
      id,
      name: characterName || state.concept || 'Unnamed Character',
      level: state.totalLevel,
      savedAt: new Date().toISOString(),
    };

    // Keep only last 5 auto-saves
    const updated = [entry, ...list].slice(0, 5);
    localStorage.setItem(STORAGE_LIST_KEY, JSON.stringify(updated));
  } catch (error) {
    console.error('Failed to save to localStorage:', error);
    // localStorage might be full or disabled
  }
}

/**
 * Load character from localStorage (auto-save)
 */
export function loadCharacterFromLocalStorage(): SavedCharacter | null {
  try {
    const json = localStorage.getItem(STORAGE_KEY);
    if (!json) return null;

    return importCharacterFromJSON(json);
  } catch (error) {
    console.error('Failed to load from localStorage:', error);
    return null;
  }
}

/**
 * Check if auto-save exists
 */
export function hasAutoSave(): boolean {
  return localStorage.getItem(STORAGE_KEY) !== null;
}

/**
 * Clear auto-save
 */
export function clearAutoSave(): void {
  localStorage.removeItem(STORAGE_KEY);
}

/**
 * Get list of saved characters
 */
export function getSavedCharactersList(): Array<{
  id: string;
  name: string;
  level: number;
  savedAt: string;
}> {
  try {
    const json = localStorage.getItem(STORAGE_LIST_KEY);
    return json ? JSON.parse(json) : [];
  } catch (error) {
    console.error('Failed to load saved characters list:', error);
    return [];
  }
}

/**
 * Get localStorage usage info
 */
export function getStorageInfo(): {
  used: number;
  available: number;
  percentUsed: number;
} {
  try {
    let total = 0;
    for (let key in localStorage) {
      if (localStorage.hasOwnProperty(key)) {
        total += localStorage[key].length + key.length;
      }
    }

    // Most browsers allow ~5-10MB, assume 5MB
    const available = 5 * 1024 * 1024;

    return {
      used: total,
      available,
      percentUsed: (total / available) * 100,
    };
  } catch (error) {
    return { used: 0, available: 0, percentUsed: 0 };
  }
}
