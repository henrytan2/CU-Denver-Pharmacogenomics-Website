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
    title: 'Ratio',
    data: 'ratio',
    defaultContent: '',
    className: 'dt-body-left dt-head-left'
  },
  {
    title: 'Gene ID',
    data: 'gene_id',
    defaultContent: '',
    render: (data: any) => {
      const url = `${paths[PATH_NAME.GTEXOME_EXOME]}?gene_id=${data}`
      let response = `<a href = "${url}">${data}</a>`
      return response
    }
  },
  {
    title: 'Description',
    data: 'description',
    defaultContent: ''
  }
]
onMounted(() => {
  ratioResultsDt = ratioResultsTable.value.dt
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
let ratioResultsDt
let ratioResultsTable = ref()
</script>
<template>
  <div style="margin-top: 40px; margin-bottom: 40px" class="container-fluid">
    <DataTable
      :columns="columns"
      :data="GTExomeStore.ratioResults"
      class="display"
      ref="ratioResultsTable"
      :options="options"
    ></DataTable>
  </div>
</template>
