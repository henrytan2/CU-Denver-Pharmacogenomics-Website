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
  StorePdbGenDataResponse,
  PdbgenFileUploadResponse
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
      fasprPrepRequest: {} as unknown as FasprPrepRequest,
      fasprPrepResponse: undefined as unknown as FasprPrepResponse,
      fasprRunRequest: undefined as unknown as FasprRunRequest,
      fasprRunResponse: undefined as unknown as FasprRunResponse,
      fasprPrepLoadingState: ApiLoadingState.Idle,
      fasprPrepUploadLoadingState: ApiLoadingState.Idle,
      fasprPrepFileUploadResponse: undefined as unknown as PdbgenFileUploadResponse,
      fasprPrepResponseAfterGenerateForFileUpload: undefined as unknown as FasprPrepResponse,
      fasprRunLoadingState: ApiLoadingState.Idle,
      storePdbgenDataLoadingState: ApiLoadingState.Idle,
      storePdbGenDataResponse: undefined as unknown as StorePdbGenDataResponse,
      selectedProteinSource: ProteinSource.AlphaFold2,
      angstromsInput: 0 as number,
      angstromsInputFileUpload: 0 as number,
      repackResiduesOnChain: false
    }
  },
  actions: {
    setFindResolutionLoadingState: function (loadingState: ApiLoadingState) {
      this.findResolutionLoadingState = loadingState
    },
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
            this.findPLDDTLoadingState = ApiLoadingState.Failed
            throw Error('Get PLDDT response failed')
          }
        })
        .catch((error) => {
          console.log(error)
        })
    },
    setFindPlddtLoadingState: function (loadingState: ApiLoadingState) {
      this.findPLDDTLoadingState = loadingState
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
    fasprPrepUpload: function (request: FasprPrepRequest) {
      const url = `${import.meta.env.VITE_API_BASE_URL}${apiUrls[API_URL_NAME.FASPR_PREP_UPLOAD]}`
      this.fasprPrepLoadingState = ApiLoadingState.Pending
      refoldStore.selectedCCID = {
        hgvsp: request.CCID
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
            this.fasprPrepResponseAfterGenerateForFileUpload = response.data
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
    fasprRun: function (uploaded: boolean = false, redirect: boolean = false) {
      const url = `${import.meta.env.VITE_API_BASE_URL}${apiUrls[API_URL_NAME.FASPR_RUN]}`
      this.fasprRunLoadingState = ApiLoadingState.Pending
      const request: FasprRunRequest = {
        mutated_sequence: uploaded
          ? this.fasprPrepResponseAfterGenerateForFileUpload.mut_seq
          : this.fasprPrepResponse.mut_seq,
        protein_location: uploaded
          ? this.fasprPrepResponseAfterGenerateForFileUpload.protein_location
          : this.fasprPrepResponse.protein_location,
        header: uploaded
          ? this.fasprPrepResponseAfterGenerateForFileUpload.header
          : this.fasprPrepResponse.header,
        session_key: uploaded
          ? this.fasprPrepResponseAfterGenerateForFileUpload.session_key
          : this.fasprPrepResponse.session_key
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
            this.fasprRunLoadingState = ApiLoadingState.Success
            this.fasprRunResponse = response.data
            await this.storePdbGenData()
            if (redirect) {
              router.push(`${paths[PATH_NAME.PDBGEN_RESULTS]}`)
            }
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
        ccid: refoldStore.selectedCCID?.hgvsp || '',
        length:
          this.fasprPrepResponse != undefined
            ? this.fasprPrepResponse?.sequence_length
            : this.fasprPrepResponseAfterGenerateForFileUpload.sequence_length,
        pdb: this.fasprRunResponse.protein_structure,
        positions:
          this.fasprPrepResponse != undefined
            ? this.fasprPrepResponse?.residue_output ?? []
            : this.fasprPrepResponseAfterGenerateForFileUpload.residue_output
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
            return Promise.resolve()
          } else {
            this.storePdbgenDataLoadingState = ApiLoadingState.Failed
            throw Error('Faspr store data failed')
          }
        })
        .catch((error) => {
          this.storePdbgenDataLoadingState = ApiLoadingState.Failed
          console.log(error)
        })
    },
    uploadFileForFasprPrep: function (file: File) {
      const url = `${import.meta.env.VITE_API_BASE_URL}${apiUrls[API_URL_NAME.FASPR_PREP_FILE_UPLOAD]}`
      const formData = new FormData()
      formData.append('file', file)
      axios
        .post(url, formData, {
          headers: {
            'Content-Type': 'multipart/form-data',
            Accept: 'application/json'
          }
        })
        .then((response) => {
          if (response.status == 201) {
            this.fasprPrepUploadLoadingState = ApiLoadingState.Success
            this.fasprPrepFileUploadResponse = response.data
          } else {
            this.fasprPrepUploadLoadingState = ApiLoadingState.Failed
            throw Error('Get Faspr Prep response failed')
          }
        })
        .catch((error) => {
          this.fasprPrepUploadLoadingState = ApiLoadingState.Failed
          console.log(error)
        })
    }
  }
})
