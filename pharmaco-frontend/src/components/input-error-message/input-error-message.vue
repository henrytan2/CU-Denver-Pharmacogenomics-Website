<script setup lang="tsx">
defineProps<{
  show: boolean
  errorText: string
}>()
</script>

<template>
  <div class="w-30">
    <span v-if="show" class="ms-2 text-danger">{{ errorText }}</span>
  </div>
</template>
