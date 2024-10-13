<script setup lang="tsx">
import { onMounted, ref } from 'vue'
import DataTable from 'datatables.net-vue3'
import DataTableCore from 'datatables.net-bs5'
import 'datatables.net-buttons-bs5'
import 'datatables.net-buttons/js/buttons.html5'
import { useMetabolovigilanceStore } from '@/stores/metabolovigilanceStore'
import { PATH_NAME, paths } from '@/constants/paths'
import Button from '@/components/button/button.vue'
import { ApiLoadingState } from '@/constants/enums'

DataTable.use(DataTableCore)
const metabolovigilanceStore = useMetabolovigilanceStore()

const precursorColumns = [
  {
    data: null,
    title: 'Drug Name',
    defaultContent: '',
    render: function (data: any) {
      const drugName = data['DrugName']
      const url = `${paths[PATH_NAME.METABOLOVIGILANCE_SIDE_EFFECT_FDA]}?drugName =${drugName}`
      let response = `<a href="${url}"">${drugName}</a>`
      return response
    }
  },
  {
    data: null,
    title: 'Drug ID',
    defaultContent: '',
    render: function (data: any) {
      let drugID = data['DrugID'].substring(3)
      const url = `https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/CID/${drugID}/record/SDF/?record_type=3d&response_type=save&response_basename=Conformer3D_CID`
      let response = `<a href="${url}"">${drugID}</a>`
      return response
    }
  },
  {
    data: null,
    title: 'Metabolites',
    defaultContent: '',
    render: '#action'
  }
]

onMounted(() => {
  precursorDt = precursorTable.value.dt
})

const options = ref({
  autoWidth: false,
  dom: 'Blfrtip',
  buttons: [
    {
      extend: 'csv',
      exportOptions: {
        columns: ':visible'
      }
    }
  ]
})

let precursorDt: any
let precursorTable = ref()

const fetchMetabolitesForDrug = (row: any) => {
  const precursorUUID = row.UUID
  metabolovigilanceStore.fetchMetabolites([precursorUUID], false)
}
</script>
<template>
  <div style="margin-top: 40px; margin-bottom: 40px" class="container-fluid d-flex">
    <div>
    <p>
      Each Drug ID below downloads a 3D structure from <a href =https://pubchem.ncbi.nlm.nih.gov>PubChem.</a> PubChem may not have a 3D structure
      of every substance below, look on <a href =https://zinc15.docking.org/substances/home>ZINC15</a> if the link below does not download the 3D structure.
    </p>
    <p class="d-flex flex-row-reverse" color="red">Viewing all metabolites for the list below can take a long period if the list is long</p>
    <div class="d-flex flex-row-reverse">
      <Button :className="'btn btn-primary'" :buttonText="'View All Metabolites'"
      :showSpinner="metabolovigilanceStore.metabolitesLoadingState == ApiLoadingState.Pending"
      :onClick="
      () => {
            const precursors = metabolovigilanceStore.precursors.map((p) => p.UUID)
            metabolovigilanceStore.fetchMetabolites(precursors, true)
          }" />
    </div>
    <DataTable
      :columns="precursorColumns"
      :data="metabolovigilanceStore.precursors"
      :options="options"
      class="display"
      ref="precursorTable"
    >
      <template #action="props">
        <Button
          :className="'btn btn-secondary'"
          :onClick="() => fetchMetabolitesForDrug(props.rowData)"
          :buttonText="'View Metabolites'"
        />
      </template>
    </DataTable>
  </div>
  </div>
</template>
