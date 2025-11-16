<!-- eslint-disable vue/multi-word-component-names -->
<script setup lang="tsx">
import { useDockingStore } from '@/stores/DockingStore'
import Button from '@/components/button/button.vue'
import Multiselect from 'vue-multiselect'
import * as yup from 'yup'
import { useField, useForm } from 'vee-validate'
import type { DockingLigandModel } from '@/models/docking'
import InputErrorMessage from '@/components/input-error-message/input-error-message.vue'
import { usePdbgenStore } from '@/stores/PdbgenStore'
import { useToastStore } from '@/stores/ToastStore'

const dockingStore = useDockingStore()
const pdbgenStore = usePdbgenStore()
const toastStore = useToastStore()

const schema = yup.object({
  smilesCode: yup
    .object()
    .required('Smiles code is required')
    .typeError('Please select a valid smiles code'),
  alphaFoldFile: yup.string().required('AlphaFold File Name is required')
})
const { handleSubmit, validate, values } = useForm({
  validationSchema: schema
})

const { value: smilesCodeAndDrugName, errorMessage: smilesCodeError } =
  useField<DockingLigandModel>('smilesCode')
const { value: alphaFoldFile, errorMessage: alphaFoldFileError } = useField<string>(
  'alphaFoldFile',
  undefined,
  {
    initialValue: dockingStore.dockingInputAF.fileName
  }
)

const onSubmit = handleSubmit((values) => {
  if (pdbgenStore.fasprRunResponse == undefined) {
    toastStore.setToastState({
      show: true,
      message:
        'Repacked Protein PDB is undefined. Please go back to GTExome Refold and click "View Structure" to continue docking.',
      header: 'Docking Error'
    })
  } else {
    dockingStore.downloadDockingResultsAF(
      alphaFoldFile.value,
      pdbgenStore.fasprRunResponse.protein_structure,
      smilesCodeAndDrugName.value.drugName,
      smilesCodeAndDrugName.value.smilesCode
    )
  }
})

const onRemoveSmilesCode = () => {
  const index = dockingStore.dockingInputAF.dockingLigandModels.findIndex(
    (o) => o.smilesCode === smilesCodeAndDrugName.value.smilesCode
  )
  if (index !== -1) {
    dockingStore.dockingInputAF.dockingLigandModels.splice(index, 1)
  }
}

const onClearAllSmilesCode = () => {
  dockingStore.dockingInputAF.dockingLigandModels = []
}
</script>
<template>
  <div class="mt-5 w-85">
    <h2>Docking</h2>
    <p>
      Download software suite for your OS and place into zip folder from download before beginning
      <a href="https://ccsb.scripps.edu/adfr/downloads/"
        >https://ccsb.scripps.edu/adfr/downloads/</a
      >
    </p>
    <form class="d-flex-col align-items-center" @submit.prevent="onSubmit">
      <label for="docking-AF-file-input" class="form-label">AlphaFold File Name</label>
      <input class="form-control" type="text" id="docking-AF-file-input" v-model="alphaFoldFile" />
      <InputErrorMessage
        :show="alphaFoldFileError != undefined"
        :error-text="alphaFoldFileError ?? ''"
      />
      <label for="docking-smiles-code-input" class="form-label">Smiles Code</label>
      <div class="d-flex d-flex-row">
        <Multiselect
          class="w-75"
          v-model="smilesCodeAndDrugName"
          :options="dockingStore.dockingInputAF.dockingLigandModels"
          id="docking-smiles-code-input"
          type="text"
          placeholder="Select Smiles Code"
        ></Multiselect>
        <button type="button" class="btn btn-secondary ms-2" @click="onRemoveSmilesCode">
          Remove
        </button>
        <button type="button" class="btn btn-secondary ms-2" @click="onClearAllSmilesCode">
          Clear all
        </button>
      </div>
      <InputErrorMessage :show="smilesCodeError != undefined" :error-text="smilesCodeError ?? ''" />

      <div class="d-flex">
        <div class="mt-3">
          <Button
            :className="'btn btn-primary'"
            :button-text="'Download Docking Zip'"
            :button-type="'submit'"
          />
        </div>
      </div>
    </form>
  </div>
</template>
