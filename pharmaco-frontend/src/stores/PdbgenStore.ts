import { defineStore } from 'pinia'
import axios from 'axios'
import { API_URL_NAME, PATH_NAME, apiUrls, paths } from '@/constants/paths'
import { ApiLoadingState } from '@/constants/enums'
import { ProteinSource } from '@/models/refold'
import { useRefoldStore } from './refoldStore'
import type {
  FindResolutionResponse,
  FindResolutionRequest,
  FindPLDDTRequest,
  FindPLDDTResponse,
  FasprPrepRequest,
  FasprPrepResponse,
  FasprRunRequest,
  FasprRunResponse,
  StorePdbGenDataRequest,
  StorePdbGenDataResponse
} from '@/models/pdbgen'
import router from '@/router'

const refoldStore = useRefoldStore()

export const usePdbgenStore = defineStore('Pdbgen', {
  state: () => {
    return {
      findResolutionLoadingState: ApiLoadingState.Idle,
      findResolutionApiResponse: undefined as unknown as FindResolutionResponse,
      pdbgenLoadingState: ApiLoadingState.Idle,
      findPLDDTLoadingState: ApiLoadingState.Idle,
      findPLDDTRequest: undefined as unknown as FindPLDDTRequest,
      findPLDDTResponse: undefined as unknown as FindPLDDTResponse,
      fasprPrepRequest: undefined as unknown as FasprPrepRequest,
      fasprPrepResponse: undefined as unknown as FasprPrepResponse,
      fasprRunRequest: undefined as unknown as FasprRunRequest,
      fasprRunResponse: undefined as unknown as FasprRunResponse,
      fasprPrepLoadingState: ApiLoadingState.Idle,
      fasprRunLoadingState: ApiLoadingState.Idle,
      storePdbgenDataLoadingState: ApiLoadingState.Idle,
      storePdbGenDataResponse: undefined as unknown as StorePdbGenDataResponse,
      selectedProteinSource: ProteinSource.AlphaFold2,
      angstromsInput: undefined as number | undefined,
      repackResiduesOnChain: false
    }
  },
  actions: {
    findResolution: function () {
      const url = `${import.meta.env.VITE_API_BASE_URL}${apiUrls[API_URL_NAME.FIND_RESOLUTION]}`
      this.findResolutionLoadingState = ApiLoadingState.Pending
      const request: FindResolutionRequest = {
        CCID: refoldStore.selectedCCID?.hgvsp ?? undefined,
        gene_ID: refoldStore.selectedGene?.ensembl_id ?? undefined
      }
      axios
        .post(url, JSON.stringify(request), {
          headers: {
            'Content-Type': 'application/json',
            Accept: 'application/json'
          }
        })
        .then((response) => {
          if (response.status == 200) {
            this.findResolutionLoadingState = ApiLoadingState.Success
            this.findResolutionApiResponse = response.data
          } else {
            this.findResolutionLoadingState = ApiLoadingState.Failed
            throw Error('Get resolution response failed')
          }
        })
        .catch((error) => {
          this.findResolutionLoadingState = ApiLoadingState.Failed
          console.log(error)
        })
    },
    findPLDDT: function () {
      const url = `${import.meta.env.VITE_API_BASE_URL}${apiUrls[API_URL_NAME.FIND_PLDDT]}`
      this.findPLDDTLoadingState = ApiLoadingState.Pending
      const request: FindPLDDTRequest = {
        CCID: refoldStore.selectedCCID?.hgvsp ?? undefined,
        gene_ID: refoldStore.selectedGene?.ensembl_id ?? undefined
      }
      axios
        .post(url, JSON.stringify(request), {
          headers: {
            'Content-Type': 'application/json',
            Accept: 'application/json'
          }
        })
        .then((response) => {
          if (response.status == 200) {
            this.findPLDDTLoadingState = ApiLoadingState.Success
            this.findPLDDTResponse = response.data
          } else {
            this.findPLDDTLoadingState = ApiLoadingState.Failed
            throw Error('Get PLDDT response failed')
          }
        })
        .catch((error) => {
          this.findPLDDTLoadingState = ApiLoadingState.Failed
          console.log(error)
        })
    },
    fasprPrep: function () {
      const url = `${import.meta.env.VITE_API_BASE_URL}${apiUrls[API_URL_NAME.FASPR_PREP]}`
      this.fasprPrepLoadingState = ApiLoadingState.Pending
      let reportedLocation = undefined
      if (this.selectedProteinSource == ProteinSource.AlphaFold2) {
        reportedLocation = this.findPLDDTResponse.af_file_location
      } else if (this.selectedProteinSource == ProteinSource.Experimental) {
        reportedLocation = this.findResolutionApiResponse.exp_file_location
      } else {
        reportedLocation == 'undefined file location'
      }
      const request: FasprPrepRequest = {
        CCID: refoldStore.selectedCCID?.hgvsp ?? undefined,
        gene_ID: refoldStore.selectedGene?.ensembl_id ?? undefined,
        angstroms: this.angstromsInput,
        toggleAlphaFoldOn: this.selectedProteinSource == ProteinSource.AlphaFold2,
        file_location: this.findResolutionApiResponse.file_location,
        chain_id: this.findResolutionApiResponse.chain_id,
        reported_location: reportedLocation
      }
      axios
        .post(url, JSON.stringify(request), {
          headers: {
            'Content-Type': 'application/json',
            Accept: 'application/json'
          }
        })
        .then((response) => {
          if (response.status == 200) {
            this.fasprPrepLoadingState = ApiLoadingState.Success
            this.fasprPrepResponse = response.data
          } else {
            this.fasprPrepLoadingState = ApiLoadingState.Failed
            throw Error('Get Faspr Prep response failed')
          }
        })
        .catch((error) => {
          this.fasprPrepLoadingState = ApiLoadingState.Failed
          console.log(error)
        })
    },
    fasprRun: function () {
      const url = `${import.meta.env.VITE_API_BASE_URL}${apiUrls[API_URL_NAME.FASPR_RUN]}`
      this.fasprRunLoadingState = ApiLoadingState.Pending
      const request: FasprRunRequest = {
        mutated_sequence: this.fasprPrepResponse.mut_seq,
        protein_location: this.fasprPrepResponse.protein_location,
        header: this.fasprPrepResponse.header
      }
      axios
        .post(url, JSON.stringify(request), {
          headers: {
            'Content-Type': 'application/json',
            Accept: 'application/json'
          }
        })
        .then((response) => {
          if (response.status == 200) {
            this.fasprRunLoadingState = ApiLoadingState.Success
            this.fasprRunResponse = response.data
            this.storePdbGenData()
          } else {
            this.fasprRunLoadingState = ApiLoadingState.Failed
            throw Error('Get Faspr Run response failed')
          }
        })
        .catch((error) => {
          this.fasprRunLoadingState = ApiLoadingState.Failed
          console.log(error)
        })
    },
    storePdbGenData: function () {
      const url = `${import.meta.env.VITE_API_BASE_URL}${apiUrls[API_URL_NAME.STORE_PDB_GEN_DATA]}`
      this.storePdbgenDataLoadingState = ApiLoadingState.Pending
      const request: StorePdbGenDataRequest = {
        ccid: refoldStore.selectedCCID.hgvsp || '',
        length: this.fasprPrepResponse.sequence_length,
        pdb: this.fasprRunResponse.protein_structure,
        positions: this.fasprPrepResponse.residue_output
      }
      axios
        .post(url, JSON.stringify(request), {
          headers: {
            'Content-Type': 'application/json',
            Accept: 'application/json'
          }
        })
        .then((response) => {
          if (response.status == 200) {
            this.storePdbgenDataLoadingState = ApiLoadingState.Success
            this.storePdbGenDataResponse = response.data
            router.push(`${paths[PATH_NAME.PDBGEN_RESULTS]}`)
          } else {
            this.storePdbgenDataLoadingState = ApiLoadingState.Failed
            throw Error('Faspr store data failed')
          }
        })
        .catch((error) => {
          this.storePdbgenDataLoadingState = ApiLoadingState.Failed
          console.log(error)
        })
    }
  }
})
