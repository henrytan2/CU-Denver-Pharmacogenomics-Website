<script setup lang="ts">
import { ref } from 'vue'
const props = defineProps<{
  onAdd?: (...args: any[]) => void
  onRemove?: (...args: any[]) => void
  dataTestId?: string
}>()

const buttonInAddState = ref(true)

const handleClick = () => {
  if (buttonInAddState.value) {
    props.onAdd?.()
    buttonInAddState.value = false
  } else {
    props.onRemove?.()
    buttonInAddState.value = true
  }
}
</script>

<template>
  <button
    type="button"
    class="btn btn-secondary"
    @click="handleClick"
    :data-testid="props.dataTestId ?? 'grid-add-button'"
  >
    <i :class="{ 'bi-plus-lg': buttonInAddState, 'bi-x-lg': !buttonInAddState }"></i>
  </button>
</template>
