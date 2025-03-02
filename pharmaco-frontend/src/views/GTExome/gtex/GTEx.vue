<!-- eslint-disable no-irregular-whitespace -->
<script setup lang="tsx">
import { ApiLoadingState, GTExomeTab } from '@/constants/enums'
import { gtexFilter } from '@/constants/enums'
import { useGTExomeStore } from '@/stores/GTExomeStore'
import { computed } from 'vue'
import { Multiselect } from 'vue-multiselect'
import { type GTexomeRangeModel } from '@/models/gtexome'
import Button from '@/components/button/button.vue'
import InfoModal from '@/components/info-modal/info-modal.vue'
import { Form, useField, useForm } from 'vee-validate'
import * as yup from 'yup'

const GTExomeStore = useGTExomeStore()
if (GTExomeStore.tissueLoadingState != ApiLoadingState.Success) {
  GTExomeStore.fetchTissueTypes()
}

const selectedTissues = computed({
  get: () => GTExomeStore.selectedTissues,
  set: (newTissue) => GTExomeStore.setSelectedTissues(newTissue)
})

const updateSelectedTissues = (tissues: string[]) => {
  GTExomeStore.setSelectedTissues(tissues)
  GTExomeStore.setTissueRatios(
    tissues.map((tissue) => {
      return {
        range: {},
        tissue: tissue
      } as GTexomeRangeModel
    })
  )
}

const schema = yup.object({
  tissue: yup.string().required('Tissue type(s) required')
})

const { handleSubmit } = useForm({
  validationSchema: schema
})

const { value: tissue, errorMessage: tissueError } = useField('selected-tissue-types')

const onSubmit = handleSubmit(() => {})

const infoModalText = `GTExome is a tool to connect genotype expression data to exome data by filtering the GTEx
    database for specific TPM ranges in different tissue types to get a list of genes. From the list
    of genes, you can view the exome data sourced from
    <a href="https://gnomad.broadinstitute.org/">gnomAD/ExAC</a>. To go directly to refold a protein
    you must have an Ensemble ENSG number and mutation info (CCID). To get a list of mutations for a
    protein use the exac tab and enter a gnomad valid protein name. GTEX Directions: <br/>1. Select
    'Filter By TPM Ratio' or 'Filter By TPM Range'. <br/>2. Add tissue types from the left list by
    clicking the plus button. <br/> a. If 'Filter By TPM Ratio' is selected. Choose a lower and upper
    bound for the ratio to filter by or leave blank for unbounded lower/upper range. <br/>Ratio
    calculated by summing the TPM of selected tissues as the numerator and the sum of non-selected
    tissues as the denominator.<br/> b. If 'Filter By TPM Range' is selected. For each selected tissue,
    enter a lower and upper bound for the expression in TPM.<br/> 3. Hit the Submit button once you are
    done. <br/>4. You will be redirected to a results page with a list of genes available in csv format.
    <br/> 5. Each Gene ID is a link to exome data available in csv format.`
</script>

<template>
  <form @submit.prevent="onSubmit">
    <InfoModal v-if="GTExomeStore.selectedTab == GTExomeTab.gtex" :modal-text="infoModalText" />
    <div class="container text-center" style="margin-top: 20px">
      <div class="row">
        <div
          class="btn-group-horizontal"
          role="group"
          aria-label="Horizontal radio toggle button group"
        >
          <input
            type="radio"
            class="btn-check"
            id="ratio-btn-radio"
            :checked="GTExomeStore.filterType == gtexFilter.ratio"
            @click="GTExomeStore.setSelectedFilter(gtexFilter.ratio)"
          />
          <label class="btn btn-outline-secondary" for="ratio-btn-radio">Filter By TPM Ratio</label>
          <input
            type="radio"
            class="btn-check"
            id="range-btn-radio"
            :checked="GTExomeStore.filterType == gtexFilter.range"
            @click="GTExomeStore.setSelectedFilter(gtexFilter.range)"
          />
          <label class="btn btn-outline-secondary" for="range-btn-radio">Filter By TPM Range</label>
        </div>
      </div>
      <div class="row" style="margin-top: 20px">
        <label> Selected Tissue Types </label>
        <Multiselect
          v-model="selectedTissues"
          id="selected-tissue-types"
          :options="GTExomeStore.tissues"
          @update:modelValue="updateSelectedTissues"
          multiple
        ></Multiselect>
      </div>
      <div
        class="row"
        v-show="GTExomeStore.filterType == gtexFilter.range"
        style="margin-top: 10px"
      >
        <div v-for="tissue in GTExomeStore.tissueRatios" :key="tissue.tissue">
          <div style="margin-bottom: 10px">
            {{ tissue.tissue }}
            <input type="number" v-model="tissue.range.lower" placeholder="e.g. .05" />
            <label>&nbsp;to&nbsp;</label>
            <input type="number" v-model="tissue.range.upper" placeholder="e.g .5" />
          </div>
        </div>
      </div>
      <div class="row" v-show="GTExomeStore.filterType == gtexFilter.ratio">
        <label>Ratio Range (Leave blank for unbounded lower/upper)</label>
        <div>
          <input type="number" v-model="GTExomeStore.ratioLowerBound" placeholder="e.g. .05" />
          <label>&nbsp;≤&nbsp;</label>
          <input type="number" v-model="GTExomeStore.ratioUpperBound" placeholder="e.g .5" />
        </div>
      </div>
    </div>
    <!-- Display Error Message if Validation Fails -->
    <div class="w-30">
      <span v-if="tissueError" class="ms-2 text-danger">{{ tissueError }}</span>
    </div>
    <div class="d-flex justify-content-end" style="margin-top: 10px">
      <Button
        :className="'btn btn-primary'"
        :buttonText="'Submit'"
        :showSpinner="
          GTExomeStore.ratioResultsLoadingState == ApiLoadingState.Pending ||
          GTExomeStore.rangeResultsLoadingState == ApiLoadingState.Pending
        "
        :onClick="GTExomeStore.fetchResults"
        :disabled="GTExomeStore.selectedTissues.length <= 0"
      />
    </div>
  </form>
</template>
<style>
input::-webkit-outer-spin-button,
input::-webkit-inner-spin-button {
  -webkit-appearance: none;
  margin: 0;
}
</style>
