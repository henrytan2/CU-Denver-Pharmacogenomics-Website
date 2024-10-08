<script setup lang="tsx">
import type { DataTableColumn } from '@/types/data-tables'
import { ref, watch } from 'vue'
const props = withDefaults(
  defineProps<{
    columns: DataTableColumn[]
    hiddenColumns: DataTableColumn[]
    onToggleHiddenColumn: (column: DataTableColumn, newHiddenColumns: DataTableColumn[]) => void
  }>(),
  {}
)

const { columns, hiddenColumns, onToggleHiddenColumn } = props

const localHiddenColumns = ref(hiddenColumns)

const emit = defineEmits<{
  (e: 'update:hiddenColumns', hiddenColumns: DataTableColumn[]): void
}>()

watch(localHiddenColumns, (newHiddenColumns) => {
  emit('update:hiddenColumns', newHiddenColumns)
})

const addHiddenColumn = (column: DataTableColumn) => {
  localHiddenColumns.value.push(column)
}

const removeHiddenColumn = (column: DataTableColumn) => {
  localHiddenColumns.value = localHiddenColumns.value.filter((obj) => {
    return obj.index !== column.index
  })
}

const handleCheckboxToggle = (event: Event, column: DataTableColumn) => {
  if ((event.target as HTMLInputElement).checked) {
    addHiddenColumn(column)
  } else {
    removeHiddenColumn(column)
  }
  onToggleHiddenColumn(column, localHiddenColumns.value)
}

const isChecked = (column: DataTableColumn) => {
  return hiddenColumns.some((obj) => {
    return Object.keys(obj).every(
      (key) => obj[key as keyof DataTableColumn] === column[key as keyof DataTableColumn]
    )
  })
}
</script>
<template>
  <div class="card mt-4 mb-4">
    <div class="card-header">Hidden Columns:</div>
    <ul v-if="columns" style="list-style: none" class="multi-column">
      <li v-for="column in columns" style="width: 20em" :key="column.name">
        <label class="form-check-label">
          <input
            :checked="isChecked(column)"
            class="form-check-input"
            :true-value="1"
            :false-value="0"
            @change="
              (event) => {
                handleCheckboxToggle(event, column)
              }
            "
            name="column"
            type="checkbox"
          />
          {{ column.name }}
        </label>
      </li>
    </ul>
  </div>
</template>
