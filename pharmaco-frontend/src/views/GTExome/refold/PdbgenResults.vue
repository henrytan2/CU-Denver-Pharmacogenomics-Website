<script setup lang="tsx">
import { usePdbgenStore } from '@/stores/PdbgenStore'

const pdbgenStore = usePdbgenStore()
const apiBaseUrl = import.meta.env.VITE_PDBGEN_URL

const downloadProtein = () => {
  const pdbBlob = new Blob([pdbgenStore.fasprRunResponse.protein_structure], {
    type: 'text/plain;charset=utf-8'
  })
  const url = window.URL.createObjectURL(pdbBlob)
  const link = document.createElement('a')
  link.href = url
  link.download = 'repacked_protein.pdb'
  link.click()
  window.URL.revokeObjectURL(url)
}
</script>
<template>
  <div class="d-flex w-100" style="margin-top: 40px">
    <div class="d-flex-row w-100">
      <button class="btn btn-primary" @click="downloadProtein">Download protein</button>
      <iframe
        class="d-flex border-0 w-100"
        height="800px"
        id="pdbgen-results"
        :src="`${apiBaseUrl}?session_key=${pdbgenStore.storePdbGenDataResponse.session_key}`"
      ></iframe>
    </div>
  </div>
</template>
