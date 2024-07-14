import { defineStore } from 'pinia'
import type { ExacSearchRequest, ExacSearchResults } from '@/models/exac'
import axios from 'axios'
import { API_URL_NAME, apiUrls } from '@/constants/paths'
import { ApiLoadingState } from '@/constants/enums'

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
    }
  }
})
