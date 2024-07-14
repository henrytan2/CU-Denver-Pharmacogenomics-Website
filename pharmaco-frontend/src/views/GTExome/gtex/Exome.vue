<!-- eslint-disable vue/multi-word-component-names -->
<script setup lang="tsx">
import { onBeforeMount, onMounted, ref } from 'vue'
import DataTable from 'datatables.net-vue3'
import DataTableCore from 'datatables.net-bs5'
import 'datatables.net-buttons-bs5'
import 'datatables.net-buttons/js/buttons.html5'
import 'datatables.net-responsive'
import { useGTExomeStore } from '@/stores/GTExomeStore'
import { useRoute } from 'vue-router'
import { ApiLoadingState } from '@/constants/enums'
import PageSpinner from '@/components/page-spinner/PageSpinner.vue'
import GridFilter from '@/components/grid-filter/GridFilter.vue'
import type { DataTableColumn, DataTableFilter } from '@/types/data-tables'
import GridToggleColumns from '@/components/grid-toggle-columns/GridToggleColumns.vue'
import { columns } from './data/data-table-columns'
import { getHiddenColumns } from './data/hidden-columns'

const route = useRoute()
const GTExomeStore = useGTExomeStore()

let showFilters = ref(false)
const handleShowFilterClick = () => {
  showFilters.value = !showFilters.value
}

let showToggleColumns = ref(false)
const handleShowToggleColumns = () => {
  showToggleColumns.value = !showToggleColumns.value
}

onBeforeMount(() => {
  const geneId = route.query.gene_id
  GTExomeStore.fetchExome(geneId?.toString() || '')
})

DataTable.use(DataTableCore)

onMounted(() => {
  exomeDt = exomeTable.value.dt
})

const options = ref({
  autoWidth: false,
  dom: 'lfBrtip',
  layout: {},
  responsive: true,
  buttons: [
    {
      extend: 'csv',
      exportOptions: {
        columns: ':visible'
      }
    }
  ]
})
let exomeDt: any
let exomeTable = ref()

let filters: DataTableFilter[] = [
  {
    useRegex: false,
    useSmartSearch: true,
    columnIndex: undefined,
    searchText: undefined
  }
]

let hiddenColumns = ref(getHiddenColumns())

const handleFilter = () => {
  filters.forEach((filter) => {
    exomeDt
      .column(filter.columnIndex)
      .search(filter.searchText, filter.useRegex, filter.useSmartSearch)
  })
  exomeDt.draw()
}

const handleMissenseFilterClick = () => {
  const missenseFilter = {
    columnIndex: '36',
    searchText: 'missense',
    useRegex: false,
    useSmartSearch: false
  }

  if (
    !filters.some(
      (item) =>
        item.columnIndex == '36' &&
        item.searchText == 'missense' &&
        item.useRegex == false &&
        item.useSmartSearch == false
    )
  ) {
    filters.push(missenseFilter)
    handleFilter()
  }
}

const toggleHiddenColumn = (column: DataTableColumn, newHiddenColumns: DataTableColumn[]) => {
  let dtColumn = exomeDt.column(column.index)

  if (
    newHiddenColumns.some((obj) => {
      return Object.keys(obj).every(
        (key) => obj[key as keyof DataTableColumn] === column[key as keyof DataTableColumn]
      )
    })
  ) {
    dtColumn.visible(false)
  } else {
    dtColumn.visible(true)
  }
}
</script>
<template>
  <div style="margin-top: 40px; margin-bottom: 40px" class="d-flex flex-column">
    <p>Select the <b class="text-primary">HGVSp</b> link to create a pdb file for that mutation</p>
    <div class="d-flex gap-3">
      <button class="btn btn-secondary" @click="handleShowToggleColumns">Toggle Columns</button>
      <button class="btn btn-secondary" @click="handleShowFilterClick">Show Filters</button>
      <button class="btn btn-secondary" @click="handleMissenseFilterClick">Missense Only</button>
    </div>
    <PageSpinner :show-spinner="GTExomeStore.exomeLoadingState == ApiLoadingState.Pending" />
    <GridToggleColumns
      :on-toggle-hidden-column="toggleHiddenColumn"
      :columns="columns.map((col, index) => {
          return { 
            index: index, 
            name: col.title 
          } as unknown as DataTableColumn 
        })"
      :hidden-columns="hiddenColumns"
      v-show="showToggleColumns"
    />
    <GridFilter
      :columns="columns.map((col, index) => {
      return {
index: index,
name: col.title
} as unknown as DataTableColumn
    })"
      v-model:filters="filters"
      :on-filter="handleFilter"
      v-show="showFilters"
    />
    <div style="overflow: auto" class="mt-2">
      <DataTable
        :columns="columns"
        :data="GTExomeStore.exomeVariants"
        class="display"
        ref="exomeTable"
        :options="options"
      ></DataTable>
    </div>
  </div>
</template>
