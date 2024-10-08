<!-- eslint-disable vue/multi-word-component-names -->
<script setup lang="tsx">
import { onMounted, ref } from 'vue'
import DataTable from 'datatables.net-vue3'
import DataTableCore from 'datatables.net-bs5'
import 'datatables.net-buttons-bs5'
import 'datatables.net-buttons/js/buttons.html5'
import { useMetabolovigilanceStore } from '@/stores/metabolovigilanceStore'
import GridAddButton from '@/components/grid-add-button/GridAddButton.vue'
import { type Api as DataTableApi } from 'datatables.net'
import { type Metabolite } from '@/models/metabolite'

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

let metaboliteDt: DataTableApi
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

let metaboliteLogPLower: number
let metaboliteLogPUpper: number
let precursorLogPLower: number
let precursorLogPUpper: number

const applyFilters = () => {
  let filteredData: Metabolite[] = []
  metabolovigilanceStore.metabolites.forEach((metabolite) => {
    let result = true
    let metaboliteLogP = metabolite.metabolite_logp
    let precursorLogP = metabolite.precursor_logp

    if (metaboliteLogPLower || metaboliteLogPLower === 0) {
      result = result && metaboliteLogPLower <= metaboliteLogP
    }

    if (metaboliteLogPUpper) {
      result = result && metaboliteLogP <= metaboliteLogPUpper
    }

    if (precursorLogPLower) {
      result = result && precursorLogPLower <= precursorLogP
    }

    if (precursorLogPUpper) {
      result = result && precursorLogP <= precursorLogPUpper
    }

    if (result == true) {
      filteredData.push(metabolite)
    }
  })
  metaboliteDt.clear()
  metaboliteDt.rows.add(filteredData)
  metaboliteDt.draw()
}

const filter = () => {
  applyFilters()
}
</script>
<template>
  <div style="margin-top: 40px; margin-bottom: 40px" class="container-fluid">
    <p>
      <a
        class="btn btn-secondary"
        data-bs-toggle="collapse"
        href="#multiCollapseExample1"
        role="button"
        aria-expanded="false"
        aria-controls="multiCollapseExample1"
        >Show Filters</a
      >
    </p>
    <div class="collapse multi-collapse" id="multiCollapseExample1">
      <div class="card card-body">
        <table class="table">
          <thead>
            <tr>
              <th>Column</th>
              <th>Value</th>
            </tr>
            <tr>
              <td>Metabolite logp</td>
              <td>
                <div class="form-horizontal row">
                  <input
                    class="form-control form-control-sm w-25"
                    type="number"
                    v-model="metaboliteLogPLower"
                    @keyup="filter"
                  />
                  &nbsp;≤&nbsp;
                  <input
                    class="form-control form-control-sm w-25"
                    type="number"
                    v-model="metaboliteLogPUpper"
                    @keyup="filter"
                  />
                </div>
              </td>
            </tr>
            <tr>
              <td>Precursor logp</td>
              <td>
                <div class="form-horizontal row">
                  <input
                    class="form-control form-control-sm w-25"
                    type="number"
                    v-model="precursorLogPLower"
                    @keyup="filter"
                  />
                  &nbsp;≤&nbsp;
                  <input
                    class="form-control form-control-sm w-25"
                    type="number"
                    v-model="precursorLogPUpper"
                    @keyup="filter"
                  />
                </div>
              </td>
            </tr>
          </thead>
        </table>
      </div>
    </div>
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
