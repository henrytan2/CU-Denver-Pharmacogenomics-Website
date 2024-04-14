<!-- eslint-disable vue/no-parsing-error -->
<script setup lang="tsx">
import { useRoute } from 'vue-router'
import { API_URL_NAME, apiUrls } from '@/constants/paths'
import { onMounted, onBeforeMount, ref, watch } from 'vue'
import DataTable from 'datatables.net-vue3'
import DataTableCore from 'datatables.net-bs5'
import 'datatables.net-buttons-bs5'
import 'datatables.net-buttons/js/buttons.html5'
import axios from 'axios'
import PageSpinner from '@/components/page-spinner/PageSpinner.vue'

const route = useRoute()
const drugName = route.query.drugName
const urlConstructor = apiUrls[API_URL_NAME.FDA]

const url = () => {
  if (typeof urlConstructor === 'function') {
    return urlConstructor(drugName)
  }
}
let dataLoaded = false

DataTable.use(DataTableCore)

let data
let lastUpdated = ref('')
let results: any = ref([])

watch(results, (newResults) => {
  if (FDADt) {
    FDADt.clear()
    FDADt.rows.add(newResults)
    FDADt.draw()
  }
})

onBeforeMount(() => {
  axios
    .get(url()!)
    .then(async (response) => {
      if (response.status == 200) {
        const json = response.data
        data = json
        lastUpdated.value = data.meta.last_updated
        results.value = data['results']
        dataLoaded = true
      } else {
        throw Error('Get FDA drugs failed')
      }
    })
    .catch((error) => {
      console.log(error)
    })
})

const columns = [
  {
    title: 'Term',
    data: 'term',
    defaultContent: ''
  },
  {
    title: 'Count',
    data: 'count',
    defaultContent: ''
  }
]
onMounted(() => {
  FDADt = FDATable.value.dt
})

const options = ref({
  autoWidth: false,
  dom: 'Blfrtip',
  // responsive: true,
  buttons: [
    {
      extend: 'csv',
      exportOptions: {
        columns: ':visible'
      }
    }
  ]
})

let FDADt: any
let FDATable = ref()
</script>
<template>
  <PageSpinner :showSpinner="!dataLoaded" />
  <div style="margin-top: 40px">
    <p>Last updated: {{ lastUpdated }}</p>
  </div>
  <div id="fda-info">
    <h2>FDA Side Effect Data for {{ drugName }}</h2>
  </div>
  <div v-show="dataLoaded" style="margin-top: 40px; margin-bottom: 40px" class="container-fluid">
    <DataTable
      :columns="columns"
      :data="results.value"
      :options="options"
      class="display nowrap"
      width="100%"
      ref="FDATable"
    ></DataTable>
  </div>
</template>
