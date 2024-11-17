<!-- eslint-disable vue/multi-word-component-names -->
<script setup lang="tsx">
import { useRefoldStore } from '@/stores/refoldStore'
import { usePdbgenStore } from '@/stores/PdbgenStore'
import { Multiselect } from 'vue-multiselect'
import Button from '@/components/button/button.vue'
import { useForm, useField } from 'vee-validate'
import * as yup from 'yup'

const fileRegex = /^.*\.(pdb|biopython)$/

const RefoldStore = useRefoldStore()
const pdbgenStore = usePdbgenStore()

const fileUploadSuccess = (file: File) => {
  pdbgenStore.fasprPrepRequest.uploaded_file = file
}

const getExacGeneResults = (value: string) => {
  RefoldStore.fetchExomeForRefold(value)
  RefoldStore.fetchGeneSearchResults(value)
}

const getBestResolutionAndPlddtScore = () => {
  if (RefoldStore.selectedGene != undefined && RefoldStore.selectedCCID != undefined) {
    pdbgenStore.findPLDDT()
    pdbgenStore.findResolution()
  }
}

const schema = yup.object({
  fileUpload: yup
    .mixed<File>()
    .test('fileType', 'Only .pdb and .biopython files are allowed', (file) => {
      if (file) {
        const filePasses = fileRegex.test(file.name)
        return filePasses
      } else {
        return false
      }
    })
})

const { handleSubmit } = useForm({
  validationSchema: schema
})

const {
  value: fileUpload,
  errorMessage: fileUploadError,
  setValue: setFileValue
} = useField('fileUpload')

const onSubmit = handleSubmit((values) => {
  fileUploadSuccess(values.fileUpload)
  pdbgenStore.fasprPrep()
})
</script>
<template>
  <form @submit.prevent="onSubmit">
    <div class="d-flex-row w-100">
      <div class="d-flex-col">
        <div class="d-flex justify-content-center">
          <h2 class="align-self-center">Upload PDB</h2>
        </div>
        <div class="d-flex justify-content-center align-items-center">
          <div class="input-group mb-3 w-50">
            <input
              type="file"
              class="form-control"
              id="fileUpload"
              @change="
                (event: Event) => {
                  setFileValue((event.target as HTMLInputElement).files![0])
                }
              "
            />
            <label class="input-group-text" for="fileUpload">Upload</label>
          </div>
        </div>
        <div class="d-flex justify-content-center align-items-center">
          <span class="ms-2 text-danger">{{ fileUploadError }}</span>
        </div>
      </div>
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
          @select="() => getBestResolutionAndPlddtScore()"
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
          @select="() => getBestResolutionAndPlddtScore()"
          :disabled="RefoldStore.selectedGene == undefined"
        ></Multiselect>
      </div>
      <div>
        <Button :className="'btn btn-primary'" :button-type="'submit'" :buttonText="'Submit'" />
      </div>
    </div>
  </form>
</template>
