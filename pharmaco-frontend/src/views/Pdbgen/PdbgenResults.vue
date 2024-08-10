<script setup lang="tsx">
import { usePdbgenStore } from '@/stores/PdbgenStore'

const pdbgenStore = usePdbgenStore()
</script>
<template>
  <iframe
    class="d-flex border-0 w-100"
    height="800px"
    id="pdbgen-results"
    :src="`http://localhost:8000/pdbgen/pdbgen-results/?session_key=${pdbgenStore.storePdbGenDataResponse.session_key}`"
  ></iframe>
</template>
