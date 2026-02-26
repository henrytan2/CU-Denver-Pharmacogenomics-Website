<!-- eslint-disable vue/multi-word-component-names -->
<script setup lang="tsx">
import { useRefoldStore } from '@/stores/refoldStore'
import { usePdbgenStore } from '@/stores/PdbgenStore'
import { Multiselect } from 'vue-multiselect'
import Button from '@/components/button/button.vue'
import { useForm, useField } from 'vee-validate'
import * as yup from 'yup'
import { useUserStore } from '@/stores/UserStore'
import { paths, PATH_NAME } from '@/constants/paths'
import { ApiLoadingState } from '@/constants/enums'
import type { FasprPrepResponse } from '@/models/pdbgen'

const fileRegex = /^.*\.(pdb|biopython)$/

const pdbgenStore = usePdbgenStore()

pdbgenStore.fasprPrepResponse = undefined as unknown as FasprPrepResponse

const userStore = useUserStore()
const hgvsProteinRegex =
  /^p\.[A-Z][a-z]{2}\d+([A-Z][a-z]{2}|=|del|ins|dup|fs|_)?(del|ins|dup|[A-Z][a-z]{2})?$/

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
    }),
  CCIDInput: yup.string().required('CCID is required').matches(hgvsProteinRegex, {
    message: 'Invalid CCID format. Must be in format of p.[Protein]###[Protein]'
  }),
  angstromsInput: yup
    .number()
    .required('Angstroms is required')
    .positive('Angstroms must be greater than 0')
})

const { handleSubmit, validateField, errors, defineField, validate } = useForm({
  validationSchema: schema,
  initialValues: {
    CCIDInput: '', // Initialize fields
    fileUpload: null,
    angstromsInput: null
  }
})

const handleFileUpload = async (event: Event) => {
  fileUploadField.handleChange(event)
  await fileUploadField.validate()
  if (fileUploadField.errors.value.length == 0) {
    pdbgenStore.uploadFileForFasprPrep(fileUploadField.value.value)
  }
}

const [CCIDField, CCIDFieldProps] = defineField('CCIDInput')

const [angstromField, angstromFieldProps] = defineField('angstromsInput')

const fileUploadField = useField<File>('fileUpload')

const handleGeneratePdbStructure = async () => {
  const validateFormResponse = await validate()
  if (validateFormResponse.errors != null) {
    pdbgenStore.fasprPrepUpload({
      CCID: CCIDField.value,
      angstroms: angstromField.value!,
      file_location: pdbgenStore.fasprPrepFileUploadResponse.destinationFileName,
      toggleAlphaFoldOn: 'uploaded'
    })
  }
}

const onSubmit = handleSubmit(
  (values) => {
    console.log(values)
    pdbgenStore.fasprRun(true, true)
  },
  (errors) => {
    console.log(errors)
  }
)
</script>
<template>
  <div class="d-flex justify-content-center">
    <h2 class="align-self-center">Upload PDB</h2>
  </div>
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
              Upload Tutorial
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
                    src="https://demo.arcade.software/OeQUiBaXLrfR8jcUEpbK?embed&embed_mobile=tab&embed_desktop=inline&show_copy_link=true"
                    title="Upload a PDB and generate a structure for a specific variant"
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
  <!-- <form @submit.prevent="onSubmit" v-if="userStore.getAPITokenResponse != undefined">
     -->
  <form @submit.prevent="onSubmit" v-if="true" style="margin-top: 20px">
    <div class="d-flex-row w-100">
      <div class="d-flex-col">
        <div class="d-flex justify-content-center align-items-center">
          <div class="input-group mb-3 w-50">
            <input type="file" class="form-control" id="fileUpload" @change="handleFileUpload" />
            <label class="input-group-text" for="fileUpload">Upload</label>
          </div>
        </div>
        <div class="d-flex justify-content-center align-items-center">
          <span class="ms-2 text-danger">{{ fileUploadField.errorMessage }}</span>
        </div>
      </div>
      <div>
        <label> CCID </label>
        <input
          v-model="CCIDField"
          v-bind="CCIDFieldProps"
          placeholder="e.g p.His144Gln"
          class="form-control mb-1 flex-grow-0"
          id="CCIDInput"
          @blur="() => validateField('CCIDInput')"
        />
        <div class="d-flex justify-content-center align-items-center">
          <span class="ms-2 text-danger">{{ errors.CCIDInput }}</span>
        </div>
      </div>
      <div>Angstroms</div>
      <input
        type="number"
        class="form-control mb-1 flex-grow-0"
        id="angstromsInput"
        v-model="angstromField"
        v-bind="angstromFieldProps"
        @blur="() => validateField('angstromsInput')"
      />
      <div class="d-flex justify-content-center align-items-center">
        <span class="ms-2 text-danger">{{ errors.angstromsInput }}</span>
      </div>
      <div>
        <Button
          :className="'btn btn-primary mt-1 mb-1'"
          :button-type="'button'"
          :buttonText="'Generate PDB Structure'"
          :disabled="
          !(errors.CCIDInput?.length! > 0 ||
            errors.fileUpload?.length! > 0 ||
            errors.angstromsInput?.length! > 0) && 
            !(CCIDField.length > 0 && fileUploadField != undefined && angstromField! > 0)
          "
          :on-click="handleGeneratePdbStructure"
        />
        <div v-if="pdbgenStore.fasprPrepUploadLoadingState === ApiLoadingState.Pending">
          <div class="spinner-border spinner-border-sm text-primary" .ml="1">
            <span class="visually-hidden">Loading...</span>
          </div>
        </div>
      </div>
      <div>
        <Button
          :className="'btn btn-primary'"
          :button-type="'submit'"
          :buttonText="'Faspr Run'"
          :disabled="pdbgenStore.fasprPrepResponseAfterGenerateForFileUpload == undefined || (!(errors.CCIDInput?.length! > 0 ||
            errors.fileUpload?.length! > 0 ||
            errors.angstromsInput?.length! > 0) && 
            !(CCIDField.length > 0 && fileUploadField != undefined && angstromField! > 0))
          "
        />
      </div>
    </div>
  </form>
  <div v-else>
    Please <a :href="paths[PATH_NAME.API_ACCESS]">log in</a> to access Upload PDB page.
  </div>
</template>
