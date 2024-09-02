<!-- eslint-disable vue/multi-word-component-names -->
<script setup lang="tsx">
import { Multiselect } from 'vue-multiselect'
import { useExacStore } from '@/stores/ExacStore'
import type { ExacGeneSearchResponse } from '@/models/exac'
import { ref } from 'vue'
import { ApiLoadingState } from '@/constants/enums'
import Button from '@/components/button/button.vue'
import { useRouter } from 'vue-router'
import { paths } from '@/constants/paths'
import { PATH_NAME } from '@/constants/paths'

const ExacStore = useExacStore()
const router = useRouter()

let selectedGene = ref<ExacGeneSearchResponse | undefined>(undefined)

const getExacGeneResults = (value: string) => {
  ExacStore.fetchGeneSearchResults(value)
}

const redirectToExacPage = () => {
  router.push(`${paths[PATH_NAME.GTEXOME_EXOME]}?gene_id=${selectedGene.value?.ensembl_id}`)
}
</script>
<template>
  <div>
    <Multiselect
      v-model="selectedGene"
      :options="
        ExacStore.geneSearchResults == undefined ? [] : ExacStore.geneSearchResults.data.gene_search
      "
      label="symbol"
      @update:modelValue="getExacGeneResults"
      @search-change="(value: string) => getExacGeneResults(value)"
      placeholder="e.g. ENPP4"
    ></Multiselect>
  </div>
  <span style="font-size: small"
    >must be valid gnomad v2.1 (https://gnomad.broadinstitute.org/) name.
  </span>
  <div class="d-flex flex-row-reverse" style="margin-top: 10px">
    <Button
      :className="'btn btn-primary'"
      :buttonText="'Submit to Exac'"
      :showSpinner="ExacStore.geneSearchRequestLoadingState == ApiLoadingState.Pending"
      :onClick="redirectToExacPage"
    />
  </div>
</template>
