<!-- eslint-disable vue/multi-word-component-names -->
<script setup lang="tsx">
import { onMounted, ref } from 'vue'
import { ApiLoadingState } from '@/constants/enums'
import button from '@/components/button/button.vue'
import { useDockingStore } from '@/stores/DockingStore'
import { defineStore } from 'pinia'
import Button from '@/components/button/button.vue'

const dockingStore = useDockingStore()
</script>
<template>
  <div class="mt-5">
    <form>
      <label for="docking-input" class="form-label">Ligand</label>
      <input
        class="form-control"
        type="text"
        id="docking-input"
        v-model="dockingStore.dockingInput.ligand"
      />
      <div class="mt-3">
        <Button
          :className="'btn btn-primary'"
          :button-text="'Download Docking Zip'"
          @click="dockingStore.downloadDockingResults()"
        />
      </div>
    </form>
  </div>
</template>
