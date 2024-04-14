<!-- eslint-disable vue/multi-word-component-names -->
<script setup lang="tsx">
import DataTable from 'datatables.net-vue3'
import DataTablesCore from 'datatables.net-bs5'
import { onBeforeMount, onMounted, ref } from 'vue'
import type { Drug, SideEffect } from '@/models/sideEffect'
import GridAddButton from '@/components/grid-add-button/GridAddButton.vue'
import { useMetabolovigilanceStore } from '@/stores/metabolovigilanceStore'
import { ApiLoadingState, MetabolovigilanceTab } from '@/constants/enums'
import Button from '@/components/button/button.vue'
import PageSpinner from '@/components/page-spinner/PageSpinner.vue'

DataTable.use(DataTablesCore)

const metabolovigilanceStore = useMetabolovigilanceStore()

const sideEffectColumns = [
  {
    data: 'side_effect',
    title: 'Side Effect',
    name: 'side_effect'
  },
  {
    defaultContent: '',
    orderable: false,
    title: 'Actions',
    name: 'Actions',
    data: null,
    render: '#action'
  }
]

const drugColumns = [
  {
    data: 'UUID',
    visible: false
  },
  {
    data: 'DrugID',
    title: 'DrugID',
    name: 'DrugID'
  },
  {
    data: 'DrugName',
    title: 'DrugName',
    name: 'DrugName'
  },
  {
    data: null,
    defaultContent: '',
    orderable: false,
    title: 'Actions',
    name: 'Actions',
    render: '#action'
  }
]

onBeforeMount(() => {
  if (metabolovigilanceStore.sideEffectLoadingState != ApiLoadingState.Success) {
    metabolovigilanceStore.fetchSideEffects()
  }
  if (metabolovigilanceStore.drugLoadingState != ApiLoadingState.Success) {
    metabolovigilanceStore.fetchDrugs()
  }
})

const onAddSideEffect = (sideEffect: SideEffect) => {
  metabolovigilanceStore.pushSelectedSideEffect(sideEffect)
}

const onRemoveSideEffect = (sideEffect: SideEffect) => {
  metabolovigilanceStore.removeSelectedSideEffect(sideEffect)
}

const onAddDrug = (drug: Drug) => {
  metabolovigilanceStore.pushSelectedDrug(drug)
}
const onRemoveDrug = (drug: Drug) => {
  metabolovigilanceStore.removeSelectedDrug(drug)
}

onMounted(() => {
  sideEffectDt = sideEffectTable.value.dt
  drugDt = drugsTable.value.dt
})

let sideEffectDt
let sideEffectTable = ref()
let drugDt
let drugsTable = ref()
</script>

<template>
  <div style="margin-top: 40px; margin-bottom: 40px" class="container-fluid">
    <h1>Metabolovigilance</h1>
    <p>
      <b>Pharmacovigilance:</b> Tracking the side effects of pharmaceuticals.
      <b>Metabolomics:</b> Studying the small molecules produced by metabolism.
      <b>Metabolovigilance:</b> A tool to aid identification of the drugs and drug metabolites that
      cause side effects. Note: Placebo side effects have been removed. Drug names in the following
      tables are links to get updated side effects from the
      <a href="https://www.fda.gov">FDA</a>.<br />
      <b>Instructions:</b><br />
      1. Select tab, then add the Side Effects or Drugs using the plus button. Hit Submit. <br />
      2. You will be redirected to a page with a filtered list of the side effects you chose <br />
      3. From that page you can view the drugs ranked by count by clicking on the 'View Drugs
      Ranked' button<br />
      4. Both result pages are available for download in CSV format. <br />
      If you use Metabolovigilance please cite:
      <a href="https://onlinelibrary.wiley.com/doi/10.1002/minf.202100261"
        >Tan, H. and Reed, S. M. Molecular Informatics,</a
      >
      <i>41</i>, <b>2022.</b><br />
      Feedback welcome:
      <a href="https://github.com/henrytan2/CU-Denver-Pharmacogenomics-Website">GitHub</a><br />

      Dataset comes from SIDER Version 4.1 (October 21, 2015)
      <a href="http://sideeffects.embl.de/">SIDER</a><br />
      Metabolites were created using
      <a href="https://jcheminf.biomedcentral.com/articles/10.1186/s13321-018-0324-5"
        >Biotransformer</a
      ><br />
      <a href="https://youtu.be/NwXIbgUmT0g">Video walkthrough</a><br />
    </p>
    <PageSpinner
      :showSpinner="
        metabolovigilanceStore.sideEffectLoadingState == ApiLoadingState.Pending ||
        metabolovigilanceStore.drugLoadingState == ApiLoadingState.Pending
      "
    />
    <div
      v-show="
        metabolovigilanceStore.drugLoadingState != ApiLoadingState.Pending ||
        metabolovigilanceStore.sideEffectLoadingState != ApiLoadingState.Pending
      "
    >
      <ul class="nav nav-tabs" id="myTab" role="tablist">
        <li class="nav-item" role="presentation">
          <button
            class="nav-link"
            @click="metabolovigilanceStore.setSelectedTab(MetabolovigilanceTab.SideEffects)"
            :class="{
              active: metabolovigilanceStore.selectedTab == MetabolovigilanceTab.SideEffects
            }"
            id="side-effects-tab"
            type="button"
            role="tab"
          >
            Side Effects
          </button>
        </li>
        <li class="nav-item" role="presentation">
          <button
            class="nav-link"
            @click="metabolovigilanceStore.setSelectedTab(MetabolovigilanceTab.Drugs)"
            :class="{ active: metabolovigilanceStore.selectedTab == MetabolovigilanceTab.Drugs }"
            id="drugs-tab"
            type="button"
            role="tab"
          >
            Drugs
          </button>
        </li>
      </ul>
      <div
        v-show="
          metabolovigilanceStore.sideEffectLoadingState != ApiLoadingState.Pending &&
          metabolovigilanceStore.selectedTab == MetabolovigilanceTab.SideEffects
        "
      >
        <DataTable
          :columns="sideEffectColumns"
          :data="metabolovigilanceStore.sideEffects"
          class="display"
          ref="sideEffectTable"
        >
          <template #action="props">
            <GridAddButton
              :onAdd="() => onAddSideEffect(props.rowData)"
              :onRemove="() => onRemoveSideEffect(props.rowData)"
            />
          </template>
        </DataTable>
        <div class="d-flex justify-content-end">
          <Button
            :className="'btn btn-primary'"
            :buttonText="'Submit'"
            :showSpinner="
              metabolovigilanceStore.drugsFromSelectedSideEffectsLoadingState ==
              ApiLoadingState.Pending
            "
            :onClick="metabolovigilanceStore.fetchDrugsFromSelectedSideEffects"
            :disabled="metabolovigilanceStore.selectedSideEffects.length <= 0"
          />
        </div>
      </div>
      <div
        v-show="
          metabolovigilanceStore.drugLoadingState != ApiLoadingState.Pending &&
          metabolovigilanceStore.selectedTab == MetabolovigilanceTab.Drugs
        "
      >
        <DataTable
          :columns="drugColumns"
          :data="metabolovigilanceStore.drugs"
          class="display"
          ref="drugsTable"
        >
          <template #action="props">
            <GridAddButton
              :onAdd="() => onAddDrug(props.rowData)"
              :onRemove="() => onRemoveDrug(props.rowData)"
            />
          </template>
        </DataTable>
        <div class="d-flex justify-content-end">
          <Button
            :className="'btn btn-primary'"
            :buttonText="'Submit'"
            :disabled="metabolovigilanceStore.selectedDrugs.length <= 0"
          />
        </div>
      </div>
    </div>
  </div>
</template>
