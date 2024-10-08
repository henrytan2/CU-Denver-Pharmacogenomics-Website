<script setup lang="tsx">
import { usePdbgenStore } from '@/stores/PdbgenStore'

const pdbgenStore = usePdbgenStore()
const apiBaseUrl = import.meta.env.VITE_PDBGEN_URL
</script>
<template>
  <iframe
    class="d-flex border-0 w-100"
    height="800px"
    id="pdbgen-results"
    :src="`${apiBaseUrl}/pdbgen-backend/pdbgen-results/?session_key=${pdbgenStore.storePdbGenDataResponse.session_key}`"
  ></iframe>
</template>
