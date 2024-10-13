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
    async fetchGeneSearchResults(geneSymbol: string) {
      const url = `${apiUrls[API_URL_NAME.GTEXOME_GENE_SEARCH_RESULTS]}`
      this.geneSearchRequestLoadingState = ApiLoadingState.Pending

      const requestBody: ExacSearchRequest = {
        query: `query GeneSearch($query: String!, $referenceGenome: ReferenceGenomeId!) {
                  gene_search(query: $query, reference_genome: $referenceGenome) {
                    ensembl_id
                    symbol
                  }
                }`,
        variables: {
          query: geneSymbol,
          referenceGenome: 'GRCh37'
        }
      }

      try {
        const response = await axios.post(url, JSON.stringify(requestBody), {
          headers: {
            'Content-Type': 'application/json',
            Accept: 'application/json'
          }
        })

        if (response.status === 200) {
          this.geneSearchRequestLoadingState = ApiLoadingState.Success
          const json = response.data
          this.setGeneSearchResults(json)
          return Promise.resolve() // Resolve the promise when successful
        } else {
          this.geneSearchRequestLoadingState = ApiLoadingState.Failed
          return Promise.reject('Get gene search results failed')
        }
      } catch (error) {
        this.geneSearchRequestLoadingState = ApiLoadingState.Failed
        console.error('Error fetching gene search results:', error)
        return Promise.reject(error) // Ensure the promise is rejected if there's an error
      }
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
