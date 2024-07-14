export interface GeneIdAndCCID {
  gene_id?: string
  hgvsp?: string
}

export interface ExomeResponseRefold {
  data: {
    gene: {
      variants: GeneIdAndCCID[]
    }
  }
}

export enum ProteinSource {
  AlphaFold2,
  Experimental
}
