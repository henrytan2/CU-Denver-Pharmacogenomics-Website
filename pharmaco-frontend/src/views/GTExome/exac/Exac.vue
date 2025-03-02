<!-- eslint-disable vue/multi-word-component-names -->
<script setup lang="tsx">
import { Multiselect } from 'vue-multiselect'
import { useExacStore } from '@/stores/ExacStore'
import type { ExacGeneSearchResponse } from '@/models/exac'
import { ApiLoadingState } from '@/constants/enums'
import Button from '@/components/button/button.vue'
import { useRouter } from 'vue-router'
import { paths } from '@/constants/paths'
import { PATH_NAME } from '@/constants/paths'
import { useField, useForm } from 'vee-validate'
import * as yup from 'yup'

const ExacStore = useExacStore()
const router = useRouter()

const getExacGeneResults = (value: string) => {
  ExacStore.fetchGeneSearchResults(value)
}

const redirectToExacPage = () => {
  if (geneSymbol.value) {
    router.push(`${paths[PATH_NAME.GTEXOME_EXOME]}?gene_id=${geneSymbol.value.ensembl_id}`)
  }
}

const schema = yup.object({
  geneSymbol: yup
    .object()
    .required('Gene symbol is required')
    .typeError('Please select a valid gene symbol')
})

const { handleSubmit } = useForm({
  validationSchema: schema
})

const { value: geneSymbol, errorMessage: geneSymbolError } =
  useField<ExacGeneSearchResponse>('geneSymbol')

const onSubmit = handleSubmit(() => {
  if (geneSymbol.value) {
    redirectToExacPage()
  }
})
</script>

<template>
  <form @submit.prevent="onSubmit">
    <div>
      <label> Gene Symbol </label>
      <Multiselect
        v-model="geneSymbol"
        :options="
          ExacStore.geneSearchResults == undefined
            ? []
            : ExacStore.geneSearchResults.data.gene_search
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
    <!-- Display Error Message if Validation Fails -->
    <div class="w-30">
      <span v-if="geneSymbolError" class="ms-2 text-danger">{{ geneSymbolError }}</span>
    </div>
    <div class="d-flex flex-row-reverse" style="margin-top: 10px">
      <Button
        :className="'btn btn-primary'"
        :buttonText="'Submit to Exac'"
        :button-type="'submit'"
        :showSpinner="ExacStore.geneSearchRequestLoadingState == ApiLoadingState.Pending"
      />
    </div>
  </form>
</template>
