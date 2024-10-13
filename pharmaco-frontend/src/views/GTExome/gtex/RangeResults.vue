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
    data: null,
    defaultContent: '',
    render: (data: any) => {
      const gene_id = data['gene_id']
      const url = `<a href="${paths[PATH_NAME.GTEXOME_EXOME]}?gene_id=${gene_id}">${gene_id}</a>`
      return url
    }
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
