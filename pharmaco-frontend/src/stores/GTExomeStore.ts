import { defineStore } from 'pinia'
import axios from 'axios'
import { API_URL_NAME, apiUrls, PATH_NAME, paths } from '@/constants/paths'
import router from '@/router'
import { ApiLoadingState, gtexFilter, GTExomeTab } from '@/constants/enums'
import type {
  ExomeResponse,
  GTexomeRangeModel,
  GTexomeRangeResult,
  GTexomeRatioRequest,
  GTexomeRatioResult,
  VariantModel
} from '@/models/gtexome'

export const useGTExomeStore = defineStore('GTExome', {
  state: () => {
    return {
      exomeLoadingState: ApiLoadingState.Idle,
      selectedTab: GTExomeTab.gtex,
      filterType: gtexFilter.ratio,
      selectedTissues: [] as string[],
      tissueRatios: [] as GTexomeRangeModel[],
      tissues: [] as string[],
      tissueLoadingState: ApiLoadingState.Idle,
      rangeResultsLoadingState: ApiLoadingState.Idle,
      rangeResults: [] as GTexomeRangeResult[],
      rangeLowerBound: undefined as number | undefined,
      rangeUpperBound: undefined as number | undefined,
      ratioResultsLoadingState: ApiLoadingState.Idle,
      ratioResults: [] as GTexomeRatioResult[],
      ratioLowerBound: undefined as number | undefined,
      ratioUpperBound: undefined as number | undefined,
      exomeVariants: [] as VariantModel[]
    }
  },
  actions: {
    setSelectedTab: function (selectedTab: GTExomeTab) {
      this.selectedTab = selectedTab
    },
    setSelectedFilter: function (selectedFilter: gtexFilter) {
      this.filterType = selectedFilter
    },
    setSelectedTissues: function (tissues: string[]) {
      this.selectedTissues = tissues
    },
    setTissueRatios: function (tissueRatios: GTexomeRangeModel[]) {
      this.tissueRatios = tissueRatios
    },
    setTissues: function (tissues: string[]) {
      this.tissues = tissues
    },
    setRangeResults: function (rangeResults: GTexomeRangeResult[]) {
      this.rangeResults = rangeResults
    },
    setRatioResults: function (ratioResults: GTexomeRatioResult[]) {
      this.ratioResults = ratioResults
    },
    fetchTissueTypes: function () {
      const url = `${import.meta.env.VITE_API_BASE_URL}${apiUrls[API_URL_NAME.GET_TISSUE_TYPES]}`
      this.tissueLoadingState = ApiLoadingState.Pending
      axios
        .get(url)
        .then(async (response) => {
          if (response.status == 200) {
            this.tissueLoadingState = ApiLoadingState.Success
            const json = response.data
            this.setTissues(json)
          } else {
            this.tissueLoadingState = ApiLoadingState.Failed
            throw Error('Get tissues failed')
          }
        })
        .catch((error) => {
          this.tissueLoadingState = ApiLoadingState.Failed
          console.log(error)
        })
    },
    fetchResults: function () {
      if (this.filterType == gtexFilter.ratio) {
        this.getRatioResults()
      }
      if (this.filterType == gtexFilter.range) {
        this.getRangeResults()
      }
    },
    fetchExome: function (geneId: string) {
      this.exomeLoadingState = ApiLoadingState.Pending
      const url = 'https://gnomad.broadinstitute.org/api/'
      const query = `
      query {
        gene(gene_id: "${geneId}", reference_genome: GRCh37) {
          variants(dataset: gnomad_r2_1) {
            gene_id
            variantId
            exome {
              ac
              ac_hemi
              ac_hom
              an
              af
              filters
              populations {
                id
                ac
                an
              }
            }
            flags
            chrom
            pos
            alt
            consequence
            consequence_in_canonical_transcript
            hgvs
            hgvsc
            hgvsp
            lof
            lof_filter
            lof_flags
            rsid
            }      
          }
        }
      `
      axios
        .post(url, { query: query })
        .then(async (response) => {
          if (response.status == 200) {
            this.exomeLoadingState = ApiLoadingState.Success
            const json: ExomeResponse = response.data
            this.setExomeVariants(json.data.gene.variants)
          } else {
            this.exomeLoadingState = ApiLoadingState.Failed
            throw Error('Get exome variants failed')
          }
        })
        .catch((error) => {
          this.exomeLoadingState = ApiLoadingState.Failed
          console.log(error)
        })
    },
    getRangeResults: function () {
      this.rangeResultsLoadingState = ApiLoadingState.Pending
      const url = `${import.meta.env.VITE_API_BASE_URL}${apiUrls[API_URL_NAME.GET_RANGE_RESULTS]}`
      axios
        .post(url, JSON.stringify(this.tissueRatios), {
          headers: {
            'Content-Type': 'application/json',
            Accept: 'application/json'
          }
        })
        .then(async (response) => {
          if (response.status == 200) {
            this.rangeResultsLoadingState = ApiLoadingState.Success
            const json = response.data
            this.setRangeResults(json)
          } else {
            this.rangeResultsLoadingState = ApiLoadingState.Failed
            console.log('Failed loading range results')
          }
        })
        .catch((error) => {
          this.rangeResultsLoadingState = ApiLoadingState.Failed
          console.log(error)
        })
    },
    getRatioResults: function () {
      this.ratioResultsLoadingState = ApiLoadingState.Pending
      const url = `${import.meta.env.VITE_API_BASE_URL}${apiUrls[API_URL_NAME.GET_RATIO_RESULTS]}`
      const request = {
        lower: this.ratioLowerBound,
        upper: this.ratioUpperBound,
        tissues: this.selectedTissues
      } as GTexomeRatioRequest
      axios
        .post(url, JSON.stringify(request), {
          headers: {
            'Content-Type': 'application/json',
            Accept: 'application/json'
          }
        })
        .then(async (response) => {
          if (response.status == 200) {
            this.ratioResultsLoadingState = ApiLoadingState.Success
            const json = response.data
            this.setRatioResults(json)
            router.push(paths[PATH_NAME.GTEXOME_RATIO_RESULTS])
          } else {
            this.ratioResultsLoadingState = ApiLoadingState.Failed
            console.log('Failed loading ratio results')
          }
        })
        .catch((error) => {
          this.ratioResultsLoadingState = ApiLoadingState.Failed
          console.log(error)
        })
    },
    setRangeLowerBound: function (rangeLowerBound: number) {
      this.ratioLowerBound = rangeLowerBound
    },
    setRangeUpperBound: function (rangeUpperBound: number) {
      this.ratioUpperBound = rangeUpperBound
    },
    setExomeVariants: function (exomeVariants: VariantModel[]) {
      this.exomeVariants = exomeVariants
    }
  }
})
