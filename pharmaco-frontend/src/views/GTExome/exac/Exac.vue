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
import InputErrorMessage from '@/components/input-error-message/input-error-message.vue'
import '@/scss/accordion.scss'

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
    <div class="container text-center" style="margin-top: 20px">
      <div class="row">
        <div class="accordion custom-accordion" id="exacAccordion">
          <div class="accordion-item">
            <h2 class="accordion-header">
              <button
                class="accordion-button collapsed"
                type="button"
                data-bs-toggle="collapse"
                data-bs-target="#exacAccordionItem"
                aria-expanded="true"
                aria-controls="exacAccordionItem"
              >
                Exac Tutorial
              </button>
            </h2>
            <div
              id="exacAccordionItem"
              class="accordion-collapse collapse"
              data-bs-parent="#exacAccordion"
            >
              <div class="accordion-body">
                <div
                  style="
                    position: relative;
                    padding-bottom: calc(77.2093% + 41px);
                    height: 0px;
                    width: 100%;
                  "
                >
                  <!--ARCADE EMBED START-->
                  <div
                    style="
                      position: relative;
                      padding-bottom: calc(77.2992% + 41px);
                      height: 0px;
                      width: 100%;
                    "
                  >
                    <iframe
                      src="https://demo.arcade.software/POP3t6qH37in6VGAP6EH?embed&embed_mobile=tab&embed_desktop=inline&show_copy_link=true"
                      title="Search a gene in ExAC and filter variants for export or mutation details"
                      frameborder="0"
                      loading="lazy"
                      webkitallowfullscreen
                      mozallowfullscreen
                      allowfullscreen
                      allow="clipboard-write"
                      style="
                        position: absolute;
                        top: 0;
                        left: 0;
                        width: 100%;
                        height: 100%;
                        color-scheme: light;
                      "
                    ></iframe>
                  </div>
                  <!--ARCADE EMBED END-->
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div>
      <label style="margin-top: 10px"> Gene Symbol </label>
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
    <InputErrorMessage :show="geneSymbolError != undefined" :error-text="geneSymbolError ?? ''" />
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
