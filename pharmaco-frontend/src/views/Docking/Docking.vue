<!-- eslint-disable vue/multi-word-component-names -->
<script setup lang="tsx">
import { useDockingStore } from '@/stores/DockingStore'
import Button from '@/components/button/button.vue'

const dockingStore = useDockingStore()
</script>
<template>
  <div class="mt-5 w-75">
    <h2>Docking</h2>
    <p>
      Download software suite for your OS and place into zip folder from download before beginning
      <a href="https://ccsb.scripps.edu/adfr/downloads/"
        >https://ccsb.scripps.edu/adfr/downloads/</a
      >
    </p>
    <form class="d-flex-col align-items-center">
      <label for="docking-AF-file-input" class="form-label">AlphaFold File Name</label>
      <input
        class="form-control"
        type="text"
        id="docking-AF-file-input"
        v-model="dockingStore.dockingInputAF.fileName"
      />
      <label for="docking-smiles-code-input" class="form-label">Smiles Code</label>
      <input
        class="form-control"
        type="text"
        id="docking-smiles-code-input"
        v-model="dockingStore.dockingInputAF.metaboliteSmilesCode"
      />
      <div class="d-flex">
        <div class="ms-auto mt-3">
          <Button
            :className="'btn btn-primary'"
            :button-text="'Download Docking Zip'"
            @click="
              () =>
                dockingStore.downloadDockingResultsAF(
                  dockingStore.dockingInputAF.fileName,
                  dockingStore.dockingInputAF.drugName,
                  dockingStore.dockingInputAF.metaboliteSmilesCode
                )
            "
          />
        </div>
      </div>
    </form>
  </div>
</template>
