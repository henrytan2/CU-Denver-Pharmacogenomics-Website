export interface ExacSearchRequest {
  query: string
  variables: ExacSearchVariables
}

export interface ExacSearchVariables {
  query: string
  referenceGenome: string
}

export interface ExacSearchResults {
  data: { gene_search: ExacGeneSearchResponse[] }
}

export interface ExacGeneSearchResponse {
  ensembl_id?: string
  symbol?: string
}
