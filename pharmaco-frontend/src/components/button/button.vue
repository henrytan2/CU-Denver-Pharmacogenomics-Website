<!-- eslint-disable vue/multi-word-component-names -->
<script setup lang="ts">
defineProps<{
  className: string
  buttonText: string
  buttonType?: 'button' | 'reset' | 'submit' | undefined
  disabled?: boolean
  onClick?: (...args: any[]) => any
  showSpinner?: boolean
}>()
</script>
<template>
  <button
    :type="buttonType == undefined ? 'button' : buttonType"
    :class="className"
    @click="onClick"
    :disabled="disabled"
  >
    <div
      v-if="showSpinner"
      class="spinner-border spinner-border-sm"
      role="status"
      data-testid="button-spinner"
    >
      <span class="visually-hidden">Loading...</span>
    </div>
    <div v-else>
      {{ buttonText }}
    </div>
  </button>
</template>
