import { defineStore } from 'pinia'
import type { ExacGeneSearchResponse, ExacSearchRequest, ExacSearchResults } from '@/models/exac'
import axios from 'axios'
import { API_URL_NAME, apiUrls } from '@/constants/paths'
import { ApiLoadingState } from '@/constants/enums'
import type { ExomeResponseRefold, GeneIdAndCCID } from '@/models/refold'

export const useRefoldStore = defineStore('refold', {
  state: () => {
    return {
      exomeLoadingState: ApiLoadingState.Idle,
      geneSearchRequestLoadingState: ApiLoadingState.Idle,
      geneSearchResults: undefined as unknown as ExacSearchResults,
      geneAndCCIDs: [] as GeneIdAndCCID[],
      selectedCCID: undefined as unknown as GeneIdAndCCID,
      selectedGene: undefined as unknown as ExacGeneSearchResponse
    }
  },
  actions: {
    setSelectedGene: function (gene: ExacGeneSearchResponse) {
      this.selectedGene = gene
    },
    setSelectedCCID: function (ccid: GeneIdAndCCID) {
      this.selectedCCID = ccid
    },
    setGeneSearchResults: function (geneSearchResults: ExacSearchResults) {
      this.geneSearchResults = geneSearchResults
    },
    fetchGeneSearchResults: function (geneSymbol: string) {
      const url = `${apiUrls[API_URL_NAME.GTEXOME_GENE_SEARCH_RESULTS]}`
      this.geneSearchRequestLoadingState = ApiLoadingState.Pending
      const requestBody: ExacSearchRequest = {
        query: `\n          query GeneSearch($query: String!, $referenceGenome: ReferenceGenomeId!) {\n            gene_search(query: $query, reference_genome: $referenceGenome) {\n              ensembl_id\n              symbol\n            }\n          }\n        `,
        variables: {
          query: geneSymbol,
          referenceGenome: 'GRCh37'
        }
      }
      axios
        .post(url, JSON.stringify(requestBody), {
          headers: {
            'Content-Type': 'application/json',
            Accept: 'application/json'
          }
        })
        .then(async (response) => {
          if (response.status == 200) {
            this.geneSearchRequestLoadingState = ApiLoadingState.Success
            const json = response.data
            this.setGeneSearchResults(json)
          } else {
            this.geneSearchRequestLoadingState = ApiLoadingState.Failed
            throw Error('Get gene search results failed')
          }
        })
        .catch((error) => {
          this.geneSearchRequestLoadingState = ApiLoadingState.Failed
          console.log(error)
        })
    },
    fetchExomeForRefold: function (geneId: string) {
      this.exomeLoadingState = ApiLoadingState.Pending
      const url = 'https://gnomad.broadinstitute.org/api/'
      const query = `
      query {
        gene(gene_symbol: "${geneId}", reference_genome: GRCh37) {
          variants(dataset: gnomad_r2_1) {
            gene_id
            hgvsp
            }      
          }
        }
      `
      axios
        .post(url, { query: query })
        .then(async (response) => {
          if (response.status == 200) {
            this.exomeLoadingState = ApiLoadingState.Success
            const json: ExomeResponseRefold = response.data
            this.geneAndCCIDs = json.data.gene.variants.filter((o) => o.hgvsp != null)
          } else {
            this.exomeLoadingState = ApiLoadingState.Failed
            throw Error('Get exome variants failed')
          }
        })
        .catch((error) => {
          this.exomeLoadingState = ApiLoadingState.Failed
          console.log(error)
        })
    }
  }
})
