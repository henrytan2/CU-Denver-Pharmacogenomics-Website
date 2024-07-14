export interface GTexomeRangeModel {
  tissue: string
  range: {
    lower?: number
    upper?: number
  }
}

export interface GTexomeRangeResult {
  gene_id: string
  description: string
}

export interface GTexomeRatioRequest {
  lower: number
  upper: number
  tissues: string[]
}

export interface GTexomeRatioResult {
  ratio: number
  gene_id: string
  description: string
}

export interface ExomeResponse {
  data: {
    gene: {
      variants: VariantModel[]
    }
  }
}

export interface ExomeModel {
  ac: number
  ac_hemi: number
  ac_hom: number
  an: number
  af: number
  filters?: string[]
  populations: PopulationModel[]
}

export interface PopulationModel {
  id: string
  ac: number
  an: number
}

export interface VariantModel {
  gene_id: string
  variantId: string
  exome?: ExomeModel
  flags: string[]
  chrom: string
  pos: number
  alt: string
  consequence: string
  consequence_in_canonical_transcript: string
  hgvs: string
  hgvsc: string
  hgvsp?: string
  lof?: string
  lof_filter?: string
  lof_flags?: string
  rsid: string
}
