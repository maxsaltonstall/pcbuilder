import { Requirement } from './requirements';

export interface Feat {
  id: string;
  name: string;
  description: string;
  prerequisites: Requirement[];
  benefits: string;
  type: FeatType[];
  source: string;
}

export type FeatType =
  | 'General'
  | 'Fighter Bonus'
  | 'Metamagic'
  | 'Item Creation'
  | 'Special';

export interface FeatSelection {
  featId: string;
  featName: string;
  gainedAtLevel: number;
}
