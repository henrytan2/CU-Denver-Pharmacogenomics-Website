import { defineStore } from 'pinia'
import axios from 'axios'
import { API_URL_NAME, apiUrls } from '@/constants/paths'
import { ApiLoadingState } from '@/constants/enums'
import type { DockingModel, DockingModelAF } from '@/models/docking'
import { useToastStore } from './ToastStore'

const toastStore = useToastStore()

export const useDockingStore = defineStore('Docking', {
  state: () => {
    return {
      loadingState: ApiLoadingState.Idle,
      dockingInput: { ligand: '' } as DockingModel,
      dockingInputAF: { fileName: '', drugName: '', metaboliteSmilesCode: '' } as DockingModelAF
    }
  },
  actions: {
    downloadDockingResults: function () {
      const url = `${import.meta.env.VITE_API_BASE_URL}${apiUrls[API_URL_NAME.DOWNLOAD_DOCKING_RESULTS]}`
      this.loadingState = ApiLoadingState.Pending
      axios
        .get(url, {
          params: { ligand_name: this.dockingInput.ligand },
          responseType: 'blob',
          headers: { Accept: 'application/zip' }
        })
        .then((response) => {
          if (response.status === 200) {
            this.loadingState = ApiLoadingState.Success
            const blob = new Blob([response.data], { type: 'application/octet-stream' })
            const link = document.createElement('a')
            link.href = window.URL.createObjectURL(blob)
            link.download = `docking_results_${this.dockingInput.ligand}.zip`
            link.click()
          } else {
            this.loadingState = ApiLoadingState.Failed
            throw Error('Download docking results failed')
          }
        })
        .catch((error) => {
          console.error(error)
          this.loadingState = ApiLoadingState.Failed
        })
    },
    downloadDockingResultsAF: function (fileName: string, drugName: string, smilesCode: string) {
      const url = `${import.meta.env.VITE_API_BASE_URL}${apiUrls[API_URL_NAME.DOWNLOAD_DOCKING_RESULTS_AF]}`
      this.loadingState = ApiLoadingState.Pending
      axios
        .get(url, {
          params: { file_name: fileName, drug_name: drugName, smiles_code: smilesCode },
          responseType: 'blob',
          headers: { Accept: 'application/zip' }
        })
        .then((response) => {
          if (response.status === 200) {
            this.loadingState = ApiLoadingState.Success
            const blob = new Blob([response.data], { type: 'application/octet-stream' })
            const link = document.createElement('a')
            link.href = window.URL.createObjectURL(blob)
            link.download = `docking_results_af_${fileName}.zip`
            link.click()
          } else {
            this.loadingState = ApiLoadingState.Failed
            toastStore.setToastState({
              show: true,
              header: 'Error',
              message: 'Download Docking AF failed'
            })
            throw Error('Download Docking AF failed')
          }
        })
        .catch((error) => {
          console.error(error)
          toastStore.setToastState({
            show: true,
            header: 'Error',
            message: 'Download Docking AF failed'
          })
          this.loadingState = ApiLoadingState.Failed
        })
    }
  }
})
