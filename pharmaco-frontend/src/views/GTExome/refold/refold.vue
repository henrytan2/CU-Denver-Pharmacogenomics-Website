<!-- eslint-disable vue/multi-word-component-names -->
<script setup lang="tsx">
import { Multiselect } from 'vue-multiselect'
import { useRefoldStore } from '@/stores/refoldStore'
import { ApiLoadingState } from '@/constants/enums'
import Button from '@/components/button/button.vue'
import { usePdbgenStore } from '@/stores/PdbgenStore'
import { watchEffect } from 'vue'
import router from '@/router'
import { paths, PATH_NAME } from '@/constants/paths'

const RefoldStore = useRefoldStore()
const pdbgenStore = usePdbgenStore()

const getExacGeneResults = (value: string) => {
  RefoldStore.fetchExomeForRefold(value)
  RefoldStore.fetchGeneSearchResults(value)
}

const findBestResolutionForPdbGen = async () => {
  pdbgenStore.findResolution()
  pdbgenStore.findPLDDT()
}

watchEffect(() => {
  if (
    pdbgenStore.findPLDDTLoadingState == ApiLoadingState.Success &&
    pdbgenStore.findResolutionLoadingState == ApiLoadingState.Success
  ) {
    router.push(`${paths[PATH_NAME.PDBGEN_REFOLD]}`)
  }
})
</script>
<template>
  <div>
    <div>
      <label> Gene Symbol </label>
      <Multiselect
        v-model="RefoldStore.selectedGene"
        :options="
          RefoldStore.geneSearchResults == undefined
            ? []
            : RefoldStore.geneSearchResults.data.gene_search
        "
        label="symbol"
        @update:modelValue="getExacGeneResults"
        @search-change="(value: string) => getExacGeneResults(value)"
        placeholder="e.g. ENPP4"
      ></Multiselect>
    </div>
    <div>
      <label> CCID </label>
      <Multiselect
        v-model="RefoldStore.selectedCCID"
        :options="RefoldStore.geneAndCCIDs == undefined ? [] : RefoldStore.geneAndCCIDs"
        label="hgvsp"
        placeholder="e.g p.His144Gln"
        :disabled="RefoldStore.selectedGene == undefined"
      ></Multiselect>
    </div>
    <div class="d-flex flex-row-reverse" style="margin-top: 10px">
      <Button
        :className="'btn btn-primary'"
        :buttonText="'Submit to refold'"
        :showSpinner="pdbgenStore.findResolutionLoadingState == ApiLoadingState.Pending"
        :onClick="findBestResolutionForPdbGen"
      />
    </div>
  </div>
</template>
