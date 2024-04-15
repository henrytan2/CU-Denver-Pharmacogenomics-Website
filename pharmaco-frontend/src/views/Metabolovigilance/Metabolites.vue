<!-- eslint-disable vue/multi-word-component-names -->
<script setup lang="tsx">
import { onMounted, ref } from 'vue'
import DataTable from 'datatables.net-vue3'
import DataTableCore from 'datatables.net-bs5'
import 'datatables.net-buttons-bs5'
import 'datatables.net-buttons/js/buttons.html5'
import { useMetabolovigilanceStore } from '@/stores/metabolovigilanceStore'
import GridAddButton from '@/components/grid-add-button/GridAddButton.vue'

DataTable.use(DataTableCore)
const metabolovigilanceStore = useMetabolovigilanceStore()

const metaboliteColumns = [
  {
    data: undefined,
    name: 'show_structure',
    render: '#showStructureButton'
  },
  {
    data: 'drug_name',
    title: 'Drug Name',
    name: 'drug_name'
  },
  {
    data: 'precursor_logp',
    title: 'Precursor logp',
    name: 'precursor_logp'
  },
  {
    data: 'metabolite_InChiKey',
    title: 'Metabolite InChiKey',
    name: 'metabolite_InChiKey'
  },
  {
    data: 'biosystem',
    title: 'Biosystem',
    name: 'biosystem'
  },
  {
    data: 'metabolite_logp',
    title: 'Metabolite logp',
    name: 'metabolite_logp'
  },
  {
    data: 'enzyme',
    title: 'Enzyme',
    name: 'enzyme'
  },
  {
    data: 'reaction',
    title: 'Reaction',
    name: 'reaction'
  },
  {
    data: 'metabolite_smile_string',
    title: 'Metabolite Smile String',
    name: 'metabolite_smile_string'
  }
]

onMounted(() => {
  metaboliteDt = metaboliteTable.value.dt
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

let metaboliteDt: any
let metaboliteTable = ref()

const showStructure = (props: any) => {
  let row = metaboliteDt.row(props.rowIndex)
  const smileString = props.rowData.metabolite_smile_string
  const structureHTML = getStructureHTML(smileString)
  row.child(structureHTML).show()
}

const hideStructure = (props: any) => {
  let row = metaboliteDt.row(props.rowIndex)
  row.child.hide()
}

const getStructureHTML = (smileString: string) => {
  const div = document.createElement('div')
  div.innerHTML = `<div class="card">
          <div class="card-body">
            <label>Structure:</label>
            <img
              width="200px"
              height="200px"
              src="https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/smiles/${smileString}/PNG"
            />
          </div>
        </div>`
  return div
}
</script>
<template>
  <div style="margin-top: 40px; margin-bottom: 40px" class="container-fluid">
    <DataTable
      :columns="metaboliteColumns"
      :data="metabolovigilanceStore.metabolites"
      :options="options"
      class="display"
      ref="metaboliteTable"
    >
      <template #showStructureButton="props">
        <GridAddButton :onAdd="() => showStructure(props)" :onRemove="() => hideStructure(props)" />
      </template>
    </DataTable>
  </div>
</template>
