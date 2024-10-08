<script setup lang="tsx">
import type { DataTableColumn, DataTableFilter } from '@/types/data-tables'
import { ref, watch } from 'vue'
const props = withDefaults(
  defineProps<{
    columns: DataTableColumn[]
    filters: DataTableFilter[]
    onFilter: () => unknown
  }>(),
  {
    columns: undefined,
    filters: () =>
      [
        {
          columnIndex: undefined,
          searchText: undefined,
          useRegex: false,
          useSmartSearch: true
        }
      ] as DataTableFilter[],
    onFilter: undefined
  }
)

const { columns, filters, onFilter } = props

const localFilters = ref(filters)

const addNewFilter = () => {
  localFilters.value.push({
    columnIndex: undefined,
    searchText: undefined,
    useRegex: false,
    useSmartSearch: true
  } as DataTableFilter)
}

const emit = defineEmits<{
  (e: 'update:filters', filters: DataTableFilter[]): void
}>()

watch(localFilters, (newFilters) => {
  emit('update:filters', newFilters)
})

const removeFilter = (colIndex: number) => {
  localFilters.value.splice(colIndex, 1)
}
</script>

<template>
  <div class="card mt-4 mb-4">
    <div class="card-header"><h4>Filters:</h4></div>
    <div class="card-body">
      <table class="table">
        <thead>
          <tr>
            <th>Column</th>
            <th>Search text</th>
            <th>Use regex</th>
            <th>Use smart search</th>
            <th>Remove</th>
          </tr>
        </thead>
        <tbody v-if="filters.length">
          <tr v-for="(filter, index) in localFilters" :key="filter.columnIndex">
            <td>
              <select
                id="column-list"
                v-on:change="onFilter"
                v-model="filter.columnIndex"
                class="form-control-sm"
              >
                <option v-for="column in columns" :value="column.index" :key="column.index">
                  {{ column.name }}
                </option>
              </select>
            </td>
            <td>
              <input
                v-on:keyup="onFilter"
                v-model="filter.searchText"
                type="text"
                class="form-control form-control-sm"
              />
            </td>
            <td style="text-align: center">
              <input
                type="checkbox"
                v-model="filter.useRegex"
                v-on:change="onFilter"
                class="form-check-input"
              />
            </td>
            <td style="text-align: center">
              <input
                type="checkbox"
                v-model="filter.useSmartSearch"
                v-on:change="onFilter"
                class="form-check-input"
              />
            </td>
            <td style="text-align: center">
              <button class="btn btn-outline-secondary" v-on:click="removeFilter(index)">
                <i class="bi bi-trash3"></i>
              </button>
            </td>
          </tr>
        </tbody>
      </table>
      <button class="btn btn-secondary" @click="addNewFilter">Add New Filter</button>
    </div>
  </div>
</template>
