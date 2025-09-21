<!-- eslint-disable vue/multi-word-component-names -->
<script setup lang="tsx">
import InfoModal from '@/components/info-modal/info-modal.vue'
import { Multiselect } from 'vue-multiselect'
import { useRefoldStore } from '@/stores/refoldStore'
import { computed, onMounted, ref, watch, watchEffect } from 'vue'
import { usePdbgenStore } from '@/stores/PdbgenStore'
import Button from '@/components/button/button.vue'
import { ApiLoadingState } from '@/constants/enums'
import { useRoute } from 'vue-router'
import { useGTExomeStore } from '@/stores/GTExomeStore'
import { GTExomeTab } from '@/constants/enums'
import { debounce } from 'lodash'
import { useField, useForm } from 'vee-validate'
import * as yup from 'yup'
import type { ExacGeneSearchResponse } from '@/models/exac'
import type { GeneIdAndCCID } from '@/models/refold'
import { useDockingStore } from '@/stores/DockingStore'
import { useToastStore } from '@/stores/ToastStore'

const infoModalText = `You will arrive at this page with a geneID and mutation (CCID) populated.
A search for experimental and AlphaFold2 structures starts automatically.
In some cases, these searches will time out and a page refresh may be necessary.
When the searches are complete, you can decide how much of the protein to repack by setting a radius in Angstroms surrounding the mutation.
Clicking Check will return a list of residues that will be repacked. Clicking Submit will generate the structure and provide a preview of the 3D structure.
You can change the mutation (CCID) or the repack radius and hit return to update the information provided.
To change the geneID and restart a search for experimental structures it is necessary to change the URL with the new geneID or return to the previous page and start your search over.
A bad geneID will return no information.`

const route = useRoute()
const CCID = route.query.CCID
const geneID = route.query.geneID

const RefoldStore = useRefoldStore()
const pdbgenStore = usePdbgenStore()
const GTExomeStore = useGTExomeStore()
const DockingStore = useDockingStore()
const toastStore = useToastStore()

DockingStore.loadingState = ApiLoadingState.Idle

const schema = yup.object({
  geneSymbol: yup
    .object()
    .required('Gene symbol is required')
    .typeError('Please select a valid gene symbol'),
  ccid: yup.object().required('CCID is required').typeError('Please select a valid CCID'),
  angstroms: yup.number().required('Angstroms is required').typeError('Please input numbers only')
})

const { handleSubmit, validate, values } = useForm({
  validationSchema: schema
})

const { value: geneSymbol, errorMessage: geneSymbolError } =
  useField<ExacGeneSearchResponse>('geneSymbol')

const { value: ccid, errorMessage: ccidError } = useField<GeneIdAndCCID>('ccid')

const { value: angstroms, errorMessage: angstromsError } = useField<number>('angstroms')

const getExacGeneResults = debounce(async (value: string) => {
  await RefoldStore.fetchGeneSearchResults(value)
}, 500)

const getExomeSearchResults = debounce(async () => {
  await RefoldStore.fetchExomeForRefold(geneSymbol.value.symbol ?? '')
}, 500)

watch(
  () => geneSymbol.value,
  async () => {
    if (geneSymbol.value != undefined) {
      getExomeSearchResults()
    }
  }
)

const onPDBAddToDocking = () => {
  DockingStore.dockingInputAF.fileName = pdbgenStore.findPLDDTResponse.af_file_location ?? ''
  toastStore.setToastState({
    show: true,
    header: 'Docking Prep',
    message: `${pdbgenStore.findPLDDTResponse.af_file_location} has been prepped for Docking!`
  })
}

const getBestResolutionAndPlddtScore = () => {
  if (geneSymbol.value != undefined && ccid.value != undefined) {
    RefoldStore.selectedGene = geneSymbol.value
    RefoldStore.selectedCCID = ccid.value
    pdbgenStore.findPLDDT()
    pdbgenStore.findResolution()
  }
}

const check = () => {
  pdbgenStore.angstromsInput = angstroms.value
  pdbgenStore.fasprPrepLoadingState = ApiLoadingState.Pending
  pdbgenStore.fasprPrep()
}

onMounted(async () => {
  if (CCID != undefined && geneID != undefined) {
    await RefoldStore.fetchGeneSearchResults(geneID as string)
    RefoldStore.setSelectedGene(RefoldStore.geneSearchResults.data.gene_search[0])
    RefoldStore.setSelectedCCID({
      hgvsp: CCID as string
    })
    getExacGeneResults(geneID as string)
    getBestResolutionAndPlddtScore()
  }
})

interface Highlight {
  start: number
  end: number
}

let highlights = ref<Highlight[]>([])

watchEffect(() => {
  if (pdbgenStore.fasprPrepLoadingState == ApiLoadingState.Success) {
    highlights.value = []
    pdbgenStore.fasprPrepResponse.residue_output.forEach((index: number) => {
      highlights.value.push({
        start: index - 1,
        end: index
      } as unknown as Highlight)
    })
  }
})

const highlightText = (text: string, highlights: Highlight[]) => {
  let result: string = ''
  let lastIndex: number = 0

  // Sort highlights by start index
  highlights.sort((a, b) => a.start - b.start)

  highlights.forEach(({ start, end }) => {
    // Add text before the highlight
    result += text.slice(lastIndex, start)
    // Add the highlighted text
    result += `<span class="highlight" title="Position: ${end}">${text.slice(start, end)}</span>`
    lastIndex = end
  })

  // Add any remaining text after the last highlight
  result += text.slice(lastIndex)
  return result
}

const highlightedText = computed(() => {
  return highlightText(pdbgenStore.fasprPrepResponse?.mut_seq || '', highlights.value)
})

const onSubmit = handleSubmit(
  (values) => {
    console.log(values)
    pdbgenStore.fasprRun()
  },
  (errors) => {
    console.log(errors)
  }
)
</script>
<template>
  <form @submit.prevent="onSubmit">
    <div style="margin-top: 40px; margin-bottom: 40px" class="container-fluid d-flex">
      <div class="d-flex-col">
        <div>
          <span
            >Select preferred source of protein data and then repack amino acids
            <a href="https://zhanggroup.org/FASPR/">(using FASPR)</a> surrounding the SNV by
            entering a diameter (in Angstroms)</span
          >
        </div>
        <InfoModal
          v-if="GTExomeStore.selectedTab == GTExomeTab.refold"
          :modal-text="infoModalText"
        />
        <div class="d-flex d-flex-row flex-shrink-0 flex-grow-0 justify-content-between ms-4 me-4">
          <div class="me-4 w-100">
            <h2>Protein Source</h2>
            <div>
              <label> Gene Symbol </label>
              <Multiselect
                v-model="geneSymbol"
                :options="
                  RefoldStore.geneSearchResults == undefined
                    ? []
                    : RefoldStore.geneSearchResults.data.gene_search
                "
                label="symbol"
                @search-change="(value: string) => getExacGeneResults(value)"
                @select="() => getBestResolutionAndPlddtScore()"
                placeholder="e.g. ENPP4"
              ></Multiselect>
            </div>
            <div>
              <label> CCID </label>
              <Multiselect
                v-model="ccid"
                :options="RefoldStore.geneAndCCIDs == undefined ? [] : RefoldStore.geneAndCCIDs"
                id="ccid"
                label="hgvsp"
                placeholder="e.g p.His144Gln"
                @select="() => getBestResolutionAndPlddtScore()"
                :disabled="geneSymbol == undefined"
              ></Multiselect>
            </div>
            <div>
              <div v-if="pdbgenStore.findResolutionLoadingState === ApiLoadingState.Pending">
                <span role="status">Searching for experimental structures </span>
                <div class="spinner-border spinner-border-sm text-primary">
                  <span class="visually-hidden">Loading...</span>
                </div>
              </div>
              <div
                v-else-if="pdbgenStore.findResolutionLoadingState === ApiLoadingState.Idle"
              ></div>
              <div v-else-if="pdbgenStore.findResolutionLoadingState === ApiLoadingState.Failed">
                Failed to load best resolution
              </div>
              <div v-else style="display: inline">
                <span style="display: inline">
                  <p style="display: inline">Experimental structure available at:&nbsp;</p>
                  <p style="color: blue; display: inline">
                    {{ pdbgenStore.findResolutionApiResponse?.resolution }}
                  </p>
                  <p style="display: inline">&nbsp;Angstrom resolution</p>
                </span>
              </div>
            </div>
            <div v-if="pdbgenStore.findPLDDTLoadingState === ApiLoadingState.Pending">
              <span role="status">Searching for AlphaFold2 structures </span>
              <div class="spinner-border spinner-border-sm text-primary">
                <span class="visually-hidden">Loading...</span>
              </div>
            </div>
            <div v-else-if="pdbgenStore.findPLDDTLoadingState === ApiLoadingState.Idle"></div>
            <div v-else-if="pdbgenStore.findPLDDTLoadingState === ApiLoadingState.Failed">
              Failed to load pLDDT response
            </div>
            <div v-else class="ms-4">
              Warnings based on AF stucture
              <p style="color: blue">
                Average plDDT score: {{ pdbgenStore.findPLDDTResponse?.plddt_avg }}
              </p>
              <p style="color: blue">{{ pdbgenStore.findPLDDTResponse?.plddt_snv }}</p>
              <p style="color: blue">{{ pdbgenStore.findPLDDTResponse?.charge_change }}</p>
              <p style="color: blue">{{ pdbgenStore.findPLDDTResponse?.proline_check }}</p>
              <p style="color: blue">{{ pdbgenStore.findPLDDTResponse?.buried }}</p>
              <p style="color: blue">{{ pdbgenStore.findPLDDTResponse?.hydrogen_bond }}</p>
              <p style="color: blue">{{ pdbgenStore.findPLDDTResponse?.salt_bridge }}</p>
              <p style="color: blue">{{ pdbgenStore.findPLDDTResponse?.recommendation }}</p>
              <p style="color: blue">{{ pdbgenStore.findPLDDTResponse?.af_file_location }}</p>
              <p style="color: blue">
                List of SNV adjacent pockets: {{ pdbgenStore.findPLDDTResponse?.pocket_info }}
              </p>
            </div>
          </div>
          <div class="flex-grow-0 flex-shrink-0 w-50">
            <h2>Repacking Parameters</h2>
            <div class="btn-group" role="group" aria-label="Basic radio toggle button group">
              <input
                type="radio"
                class="btn-check"
                name="btnradio"
                id="btnradio1"
                autocomplete="off"
                checked
              />
              <label class="btn btn-outline-info" for="btnradio1">AlphaFold2</label>

              <input
                type="radio"
                class="btn-check"
                name="btnradio"
                id="btnradio2"
                autocomplete="off"
              />
              <label class="btn btn-outline-info" for="btnradio2">Experimental</label>
            </div>
            <div>Angstroms</div>
            <input
              type="number"
              class="form-control mb-1 flex-grow-0 flex-shrink-0 w-50"
              v-model="angstroms"
            />
            <label class="mb-1">
              <input type="checkbox" v-model="pdbgenStore.repackResiduesOnChain" />
              Repack all residues on chain
            </label>
            <div class="mb-3">
              <Button
                :className="'btn btn-primary'"
                :buttonText="'Check'"
                :show-spinner="pdbgenStore.fasprPrepLoadingState == ApiLoadingState.Pending"
                :on-click="check"
                :disabled="
                  !(
                    pdbgenStore.findResolutionLoadingState == ApiLoadingState.Success &&
                    pdbgenStore.findPLDDTLoadingState == ApiLoadingState.Success &&
                    angstroms != undefined &&
                    angstroms > 0
                  )
                "
              />
            </div>
            <div>
              <Button
                :className="'btn btn-primary'"
                :buttonText="'View Structure'"
                :button-type="'submit'"
                :disabled="pdbgenStore.fasprPrepLoadingState != ApiLoadingState.Success"
              />
              <Button
                :className="'btn btn-primary ms-2'"
                :buttonText="'Save PDB For Docking'"
                :button-type="'button'"
                data-bs-toggle="tooltip"
                data-bs-placement="top"
                title="Prep protein PDB for docking"
                :disabled="pdbgenStore.fasprPrepLoadingState != ApiLoadingState.Success"
                @click="onPDBAddToDocking"
              />
            </div>
            <div>
              <span
                >Protein sequence with residues to be repacked in CAPS have an average pLDDT score
                of:</span
              >
              <div>
                <div
                  v-if="pdbgenStore.fasprPrepLoadingState === ApiLoadingState.Pending"
                  class="spinner-border spinner-border-sm text-primary"
                  role="status"
                >
                  <span class="visually-hidden">Loading...</span>
                </div>
                <div v-else-if="pdbgenStore.fasprPrepLoadingState === ApiLoadingState.Failed">
                  Failed to load faspr response
                </div>
                <div v-else>
                  <p>{{ pdbgenStore.fasprPrepResponse?.repack_pLDDT }}</p>
                  <p
                    id="text-container"
                    class="text-break flex-grow-0 flex-shrink-0 w-50"
                    v-html="highlightedText"
                  ></p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </form>
</template>

<style>
.highlight {
  background-color: yellow;
  font-weight: bold;
}
</style>
