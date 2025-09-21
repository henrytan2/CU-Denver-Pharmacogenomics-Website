<!-- eslint-disable vue/multi-word-component-names -->
<script setup lang="tsx">
import { useToastStore } from '@/stores/ToastStore'

const toastStore = useToastStore()
</script>

<template>
  <div class="position-fixed top-0 end-0 p-5 mt-5" style="z-index: 11">
    <div
      :class="`toast fade ${toastStore.state.show ? 'show' : 'hide'}`"
      role="alert"
      aria-live="assertive"
      aria-atomic="true"
    >
      <div class="toast-header">
        <strong class="me-auto">{{ toastStore.state.header }}</strong>
        <button
          type="button"
          class="btn-close"
          data-bs-dismiss="toast"
          aria-label="Close"
          @click="toastStore.dismissToast"
        ></button>
      </div>
      <div class="toast-body">{{ toastStore.state.message }}</div>
    </div>
  </div>
</template>
