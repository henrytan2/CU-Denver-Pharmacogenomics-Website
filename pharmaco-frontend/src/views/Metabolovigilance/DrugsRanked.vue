<script setup lang="tsx">
import { onMounted, ref } from 'vue'
import DataTable from 'datatables.net-vue3'
import DataTableCore from 'datatables.net-bs5'
import 'datatables.net-buttons-bs5'
import 'datatables.net-buttons/js/buttons.html5'
import 'datatables.net-responsive'
import Button from '@/components/button/button.vue'
import { useMetabolovigilanceStore } from '@/stores/metabolovigilanceStore'
import { paths, PATH_NAME } from '@/constants/paths'

DataTable.use(DataTableCore)
const metabolovigilanceStore = useMetabolovigilanceStore()
const columns = [
  {
    title: 'Drug Name',
    data: 'drug_name',
    defaultContent: '',
    render: (data: any) => {
      const url = `${paths[PATH_NAME.METABOLOVIGILANCE_SIDE_EFFECT_FDA]}?drugName=${data}`
      let response = `<a href="${url}"">${data}</a>`
      return response
    }
  },
  {
    title: 'Drug ID',
    data: 'drug_id',
    defaultContent: '',
    render: (data: any) => {
      let drugID = data.substring(3)
      let url =
        'https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/CID/' +
        drugID +
        '/record/SDF/?record_type=3d&response_type=save&response_basename=Conformer3D_CID'
      let response = '<a href=' + url + '>' + drugID + '</a>'
      return response
    }
  },
  {
    title: 'Count',
    data: 'dcount',
    defaultContent: ''
  },
  {
    title: 'Metabolites',
    defaultContent: ''
  }
]
onMounted(() => {
  drugsRankedDt = drugsRankedTable.value.dt
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

let drugsRankedDt: any
let drugsRankedTable = ref()
</script>
<template>
  <div style="margin-top: 40px">
    <h1>Metabolovigilence - Drugs Ranked</h1>
    <p>
      Each Drug ID below downloads a 3D structure from
      <a href="https://pubchem.ncbi.nlm.nih.gov/">PubChem</a>. PubChem may not have a 3D structure
      of every substance below, look on
      <a href="https://zinc15.docking.org/substances/home/">ZINC15</a>
      if the link below does not download the 3D structure.
    </p>
  </div>
  <div>
    <DataTable
      :columns="columns"
      :data="metabolovigilanceStore.rankedDrugs"
      ref="drugsRankedTable"
      class="display nowrap"
      :options="options"
    ></DataTable>
  </div>
</template>
