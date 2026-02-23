export type Alignment =
  | 'LG' | 'NG' | 'CG'
  | 'LN' | 'N' | 'CN'
  | 'LE' | 'NE' | 'CE';

export interface Domain {
  id: string;
  name: string;
  description: string;
  grantedPower: string;
  /** Domain spells by spell level (0-9) */
  domainSpells: {
    [level: number]: string; // spell name
  };
  source: string;
}

export interface Deity {
  id: string;
  name: string;
  title: string;
  alignment: Alignment;
  domains: string[]; // domain IDs
  favoredWeapon: string;
  portfolio: string;
  worshipers: string;
  source: string;
}

export interface CharacterDeitySelection {
  deityId: string;
  deityName: string;
  selectedDomains: string[]; // Usually 2 domains for clerics
}
