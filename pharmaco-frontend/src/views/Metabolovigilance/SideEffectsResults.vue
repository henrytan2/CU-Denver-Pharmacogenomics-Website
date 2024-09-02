<script setup lang="tsx">
import DataTable from 'datatables.net-vue3'
import DataTablesCore from 'datatables.net-bs5'
import { onMounted, ref } from 'vue'
import { useMetabolovigilanceStore } from '@/stores/metabolovigilanceStore'
import { PATH_NAME, paths } from '@/constants/paths'
import Button from '@/components/button/button.vue'

DataTable.use(DataTablesCore)

const metabolovigilanceStore = useMetabolovigilanceStore()

const columns = [
  {
    title: 'Drug ID',
    data: 'drug_id',
    defaultContent: ''
  },
  {
    title: 'StereoIsomer ID',
    data: 'stereoisomer',
    defaultContent: ''
  },
  {
    data: null,
    title: 'Drug Name',
    defaultContent: '',
    render: function (data: any) {
      const drugName = data['drug_name']
      const url = `${paths[PATH_NAME.METABOLOVIGILANCE_SIDE_EFFECT_FDA]}?drugName=${drugName}`
      let response = `<a href="${url}"">${drugName}</a>`
      return response
    }
  },
  {
    title: 'UMLS Concept ID',
    data: 'umls_concept_id',
    defaultContent: ''
  },
  {
    title: 'Frequency (%)',
    data: 'frequency_percent',
    defaultContent: ''
  },
  {
    title: 'Frequency Lower',
    data: 'frequency_lower',
    defaultContent: ''
  },
  {
    title: 'Frequency Upper',
    data: 'frequency_upper',
    defaultContent: ''
  },
  {
    title: 'Side Effect',
    data: 'side_effect',
    defaultContent: ''
  },
  {
    title: 'ATC Code',
    data: 'atc_code',
    defaultContent: ''
  }
]

onMounted(() => {
  sideEffectResultDt = sideEffectResultTable.value.dt
})

let sideEffectResultDt
let sideEffectResultTable = ref()

const handleViewDrugsRankedClick = () => {
  metabolovigilanceStore.fetchRankedDrugs()
}
</script>
<template>
  <div>
    <div style="margin-top: 40px; margin-bottom: 40px" class="container-fluid">
      <div class="d-flex justify-content-end">
        <Button
          :buttonText="'View Drugs Ranked'"
          :className="'btn btn-primary'"
          :onClick="handleViewDrugsRankedClick"
        />
      </div>
      <DataTable
        :columns="columns"
        :data="metabolovigilanceStore.drugsFromSelectedSideEffects"
        class="display"
        ref="sideEffectResultTable"
      >
      </DataTable>
    </div>
  </div>
</template>
