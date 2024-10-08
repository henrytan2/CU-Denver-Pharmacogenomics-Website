<script setup lang="ts">
defineProps<{
  showSpinner: boolean
}>()
</script>

<template>
  <div v-if="showSpinner" class="d-flex align-items-center justify-content-center vh-100">
    <div class="spinner-border" role="status">
      <span class="visually-hidden">Loading...</span>
    </div>
  </div>
</template>
