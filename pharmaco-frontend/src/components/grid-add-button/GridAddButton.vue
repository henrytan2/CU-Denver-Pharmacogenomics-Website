<script setup lang="ts">
import { ref } from 'vue'
const props = defineProps<{
  onAdd?: (...args: any[]) => void
  onRemove?: (...args: any[]) => void
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
  <button type="button" class="btn btn-secondary" @click="handleClick">
    <i :class="{ 'bi-plus-lg': buttonInAddState, 'bi-x-lg': !buttonInAddState }"></i>
  </button>
</template>
