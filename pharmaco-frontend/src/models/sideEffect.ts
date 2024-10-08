export interface Drug {
  id: number
  drug_id: string
  stereoisomer: string
  umls_concept_id: string
  frequency_percent: string
  frequency_lower: string
  frequency_upper: string
  concept_type: string
  side_effect: string
  drug_name: string
  UUID: string
}

export interface SideEffect {
  side_effect: string
}

export interface RankedDrug {
  UUID: string
  drug_name: string
  drug_id: string
  dcount: number
}

export interface Precursor {
  UUID: string
  DrugID: string
  DrugName: string
  SmileCode: string
  InChiKey: string
  logp: string
  max_rmsd: string
}

export interface FetchPrecursorsForDrugsResponse {
  precursors: Precursor[]
}

export interface FetchPrecursorsForDrugsRequest {
  precursor_UUIDs: string[]
}
