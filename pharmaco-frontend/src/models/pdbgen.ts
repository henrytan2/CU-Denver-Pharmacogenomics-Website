export interface FindResolutionResponse {
  resolution: string
  file_location: string
  chain_id: string
  exp_file_location: string
}

export interface FindResolutionRequest {
  gene_ID?: string
  CCID?: string
}

export interface FindPLDDTRequest {
  gene_ID?: string
  CCID?: string
}

export interface FindPLDDTResponse {
  plddt_snv?: string
  plddt_avg?: number
  af_file_location?: string
  charge_change?: string
  disulfide_check?: string
  proline_check?: string
  buried?: string
  hydrogen_bond?: string
  salt_bridge?: string
  fetchingpLDDT?: boolean
  recommendation?: string
  pocket_info?: string | Object
}

export interface FasprPrepRequest {
  CCID?: string
  gene_ID?: string
  angstroms?: number
  toggleAlphaFoldOn: boolean
  file_location: string
  chain_id: string
  reported_location?: string
}

export interface FasprPrepResponse {
  residue_output: number[]
  sequence_length: number
  mut_seq: string
  repack_pLDDT: number
  protein_location: string
}
