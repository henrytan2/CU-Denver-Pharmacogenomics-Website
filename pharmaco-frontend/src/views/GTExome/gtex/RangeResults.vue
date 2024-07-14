<script setup lang="tsx">
import { onMounted, ref, render } from 'vue'
import DataTable from 'datatables.net-vue3'
import DataTableCore from 'datatables.net-bs5'
import 'datatables.net-buttons-bs5'
import 'datatables.net-buttons/js/buttons.html5'
import 'datatables.net-responsive'
import { useGTExomeStore } from '@/stores/GTExomeStore'
import { paths, PATH_NAME } from '@/constants/paths'

DataTable.use(DataTableCore)
const GTExomeStore = useGTExomeStore()
const columns = [
  {
    title: 'Gene ID',
    data: 'gene_id',
    defaultContent: ''
  },
  {
    title: 'Description',
    data: 'description',
    defaultContent: ''
  }
]
onMounted(() => {
  rangeResultsDt = rangeResultsTable.value.dt
})
const options = ref({
  autoWidth: false,
  dom: 'Blfrtip',
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
let rangeResultsDt
let rangeResultsTable = ref()
</script>
<template>
  <div style="margin-top: 40px; margin-bottom: 40px" class="container-fluid">
    <DataTable
      :columns="columns"
      :data="GTExomeStore.rangeResults"
      class="display"
      ref="rangeResultsTable"
      :options="options"
    ></DataTable>
  </div>
</template>
