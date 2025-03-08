import { defineStore } from 'pinia'
import type { ExacSearchRequest, ExacSearchResults } from '@/models/exac'
import axios from 'axios'
import { API_URL_NAME, apiUrls } from '@/constants/paths'
import { ApiLoadingState } from '@/constants/enums'
import { axiosWithRetry } from '@/utils/axios-utils'

export const useExacStore = defineStore('exac', {
  state: () => {
    return {
      geneSearchRequestLoadingState: ApiLoadingState.Idle,
      geneSearchResults: undefined as unknown as ExacSearchResults
    }
  },
  actions: {
    setGeneSearchResults: function (geneSearchResults: ExacSearchResults) {
      this.geneSearchResults = geneSearchResults
    },
    fetchGeneSearchResults: async function (geneSymbol: string) {
      const url = `${apiUrls[API_URL_NAME.GTEXOME_GENE_SEARCH_RESULTS]}`
      this.geneSearchRequestLoadingState = ApiLoadingState.Pending
      const requestBody: ExacSearchRequest = {
        query: `\n          query GeneSearch($query: String!, $referenceGenome: ReferenceGenomeId!) {\n            gene_search(query: $query, reference_genome: $referenceGenome) {\n              ensembl_id\n              symbol\n            }\n          }\n        `,
        variables: {
          query: geneSymbol,
          referenceGenome: 'GRCh37'
        }
      }
      const headers = {
        'Content-Type': 'application/json',
        Accept: 'application/json'
      }

      try {
        const response = await axiosWithRetry<ExacSearchResults>(url, requestBody, headers, 3)

        if (response.status === 200) {
          this.geneSearchRequestLoadingState = ApiLoadingState.Success
          const json = response.data
          // Process and set your data here
          console.log('Gene search results:', json)
          this.geneSearchResults = json
        } else {
          this.geneSearchRequestLoadingState = ApiLoadingState.Failed
          throw new Error('Get gene search results failed')
        }
      } catch (error) {
        this.geneSearchRequestLoadingState = ApiLoadingState.Failed
        console.error('Error fetching gene search results:', error)
      }
    }
  }
})
