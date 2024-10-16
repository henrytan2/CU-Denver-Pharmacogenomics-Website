import { defineStore } from 'pinia'
import type {
  Drug,
  RankedDrug,
  SideEffect,
  Precursor,
  FetchPrecursorsForDrugsRequest,
  FetchPrecursorsForDrugsResponse
} from '@/models/sideEffect'
import axios from 'axios'
import { API_URL_NAME, apiUrls, PATH_NAME, paths } from '@/constants/paths'
import { ApiLoadingState, MetabolovigilanceTab } from '@/constants/enums'
import router from '@/router'
import type { Metabolite } from '@/models/metabolite'

export const useMetabolovigilanceStore = defineStore('metabolovigilance', {
  state: () => {
    return {
      drugLoadingState: ApiLoadingState.Idle,
      drugs: [] as Drug[],
      selectedDrugs: [] as Drug[],
      selectedTab: MetabolovigilanceTab.SideEffects,
      sideEffects: [] as SideEffect[],
      sideEffectLoadingState: ApiLoadingState.Idle,
      selectedSideEffects: [] as SideEffect[],
      drugsFromSelectedSideEffects: [] as Drug[],
      drugsFromSelectedSideEffectsLoadingState: ApiLoadingState.Idle,
      rankedDrugs: [] as RankedDrug[],
      rankedDrugsLoadingState: ApiLoadingState.Idle,
      metabolites: [] as Metabolite[],
      metabolitesLoadingState: ApiLoadingState.Idle,
      precursors: [] as Precursor[],
      precursorsLoadingState: ApiLoadingState.Idle
    }
  },
  actions: {
    setDrugs: function (drugs: Drug[]) {
      this.drugs = drugs
    },
    pushSelectedDrug: function (drug: Drug) {
      this.selectedDrugs.push(drug)
    },
    removeSelectedDrug: function (drug: Drug) {
      const index = this.selectedDrugs.indexOf(drug)
      this.selectedDrugs.splice(index, 1)
    },
    fetchDrugs: function () {
      const url = `${import.meta.env.VITE_API_BASE_URL}${apiUrls[API_URL_NAME.GET_DRUGS]}`
      this.drugLoadingState = ApiLoadingState.Pending
      axios
        .get(url)
        .then(async (response) => {
          if (response.status == 200) {
            this.drugLoadingState = ApiLoadingState.Success
            const json = response.data
            this.setDrugs(json)
          } else {
            this.drugLoadingState = ApiLoadingState.Failed
            throw Error('Get drugs failed')
          }
        })
        .catch((error) => {
          this.drugLoadingState = ApiLoadingState.Failed
          console.log(error)
        })
    },
    fetchDrugsFromSelectedSideEffects: function () {
      const url = `${import.meta.env.VITE_API_BASE_URL}${apiUrls[API_URL_NAME.GET_DRUGS_BY_SELECTED_SIDE_EFFECTS]}`
      this.drugsFromSelectedSideEffectsLoadingState = ApiLoadingState.Pending
      const selectedSideEffects = this.selectedSideEffects.map((sideEffect) => {
        return sideEffect.side_effect
      })
      const request = {
        selectedSideEffects: selectedSideEffects
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
            this.drugsFromSelectedSideEffectsLoadingState = ApiLoadingState.Success
            const json = response.data
            this.drugsFromSelectedSideEffects = json
            router.push(paths[PATH_NAME.METABOLOVIGILANCE_SIDE_EFFECT_RESULTS])
          } else {
            this.drugsFromSelectedSideEffectsLoadingState = ApiLoadingState.Failed
            throw Error('Get drugs from selected side effects failed')
          }
        })
        .catch((error) => {
          this.drugsFromSelectedSideEffectsLoadingState = ApiLoadingState.Failed
          console.log(error)
        })
    },
    setSelectedTab: function (selectedTab: MetabolovigilanceTab) {
      this.selectedTab = selectedTab
    },
    setSideEffects: function (sideEffects: SideEffect[]) {
      this.sideEffects = sideEffects
    },
    pushSelectedSideEffect: function (sideEffect: SideEffect) {
      this.selectedSideEffects.push(sideEffect)
    },
    removeSelectedSideEffect: function (sideEffect: SideEffect) {
      const index = this.selectedSideEffects.indexOf(sideEffect)
      this.selectedSideEffects.splice(index, 1)
    },
    fetchSideEffects: function () {
      const url = `${import.meta.env.VITE_API_BASE_URL}${apiUrls[API_URL_NAME.GET_SIDE_EFFECTS]}`
      this.sideEffectLoadingState = ApiLoadingState.Pending
      axios
        .get(url)
        .then(async (response) => {
          if (response.status == 200) {
            this.sideEffectLoadingState = ApiLoadingState.Success
            const json = response.data
            this.setSideEffects(json)
          } else {
            this.sideEffectLoadingState = ApiLoadingState.Failed
            throw Error('Get side effects failed')
          }
        })
        .catch((error) => {
          this.sideEffectLoadingState = ApiLoadingState.Failed
          console.log(error)
        })
    },
    fetchRankedDrugs: function () {
      const url = `${import.meta.env.VITE_API_BASE_URL}${apiUrls[API_URL_NAME.GET_RANKED_DRUGS]}`
      this.rankedDrugsLoadingState = ApiLoadingState.Pending
      const selectedSideEffects = this.selectedSideEffects.map((sideEffect) => {
        return sideEffect.side_effect
      })
      const request = {
        selectedSideEffects: selectedSideEffects
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
            this.rankedDrugsLoadingState = ApiLoadingState.Success
            const json = response.data
            this.rankedDrugs = json
            router.push(paths[PATH_NAME.METABOLOVIGILANCE_DRUGS_RANKED])
          } else {
            this.rankedDrugsLoadingState = ApiLoadingState.Failed
            throw Error('Get ranked drugs failed')
          }
        })
        .catch((error) => {
          this.rankedDrugsLoadingState = ApiLoadingState.Failed
          console.log(error)
        })
    },
    fetchMetabolites: function (precursorUUIDs: string[], isMultiple?: boolean) {
      const url = isMultiple
        ? `${import.meta.env.VITE_API_BASE_URL}${apiUrls[API_URL_NAME.METABOLITES_FOR_MULTIPLE_PRECURSORS]}`
        : `${import.meta.env.VITE_API_BASE_URL}${apiUrls[API_URL_NAME.METABOLITES_FOR_ONE_PRECURSOR]}`
      this.metabolitesLoadingState = ApiLoadingState.Pending
      const request = {
        precursorUUIDs: precursorUUIDs
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
            this.metabolitesLoadingState = ApiLoadingState.Success
            const json = response.data
            this.metabolites = json
            router.push(paths[PATH_NAME.METABOLOVIGILANCE_METABOLITES])
          } else {
            this.metabolitesLoadingState = ApiLoadingState.Failed
            throw Error('Get Metabolites failed.')
          }
        })
        .catch((error) => {
          this.metabolitesLoadingState = ApiLoadingState.Failed
          console.log(error)
        })
    },
    fetchPrecursorsForDrugs: function (
      fetchPrecursorsForDrugsRequest: FetchPrecursorsForDrugsRequest
    ) {
      const url = `${import.meta.env.VITE_API_BASE_URL}${apiUrls[API_URL_NAME.FETCH_PRECURSORS_FOR_DRUGS]}`
      this.precursorsLoadingState = ApiLoadingState.Pending
      axios
        .post(url, JSON.stringify(fetchPrecursorsForDrugsRequest), {
          headers: {
            'Content-Type': 'application/json',
            Accept: 'application/json'
          }
        })
        .then(async (response) => {
          if (response.status == 200) {
            this.precursorsLoadingState == ApiLoadingState.Success
            const json = response.data as FetchPrecursorsForDrugsResponse
            this.precursors = json.precursors
            router.push(paths[PATH_NAME.PRECURSOR_RESULTS])
          } else {
            this.precursorsLoadingState = ApiLoadingState.Failed
            throw Error('Get Precursors Failed')
          }
        })
        .catch((error) => {
          this.precursorsLoadingState = ApiLoadingState.Failed
          console.log(error)
        })
    }
  }
})
