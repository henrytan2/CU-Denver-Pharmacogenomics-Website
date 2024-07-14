import { defineStore } from 'pinia'
import axios from 'axios'
import { API_URL_NAME, apiUrls, PATH_NAME, paths } from '@/constants/paths'
import router from '@/router'
import { ApiLoadingState } from '@/constants/enums'
import { ProteinSource } from '@/models/refold'
import { useRefoldStore } from './refoldStore'
import type {
  FindResolutionResponse,
  FindResolutionRequest,
  FindPLDDTRequest,
  FindPLDDTResponse,
  FasprPrepRequest,
  FasprPrepResponse
} from '@/models/pdbgen'

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
      fasprPrepLoadingState: ApiLoadingState.Idle,
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
        .then(async (response) => {
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
        .then(async (response) => {
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
        .then(async (response) => {
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
    }
  }
})
