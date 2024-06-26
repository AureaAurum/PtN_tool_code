export interface Material {
  id: number;
  category: string;
  rarity: number | string;
  name: string;
  required: number | "";
  owned: number | "";
  short: number;
  totalRequired : number;
}
export interface Categories {
  [category:string] : Material[]
}

export interface Condition {
  level: number;
  target_level: number;
  ru1: string;
  ru2: string;
  ru3: string;
  slv: number[];
  target_slv:number[];
}

export interface Character {
  name: string;
  ename:string;
  rarity: string;
  sin: string;
  rankup_material1: string;
  rankup_material2: string;
  skill_material: string;
  naikai: string;
  condition: Condition;
}

export interface Characters {
  [character:string] : Character
}

export interface ChJsonData {
  Characters: Characters;
  createdDate: string;
}
