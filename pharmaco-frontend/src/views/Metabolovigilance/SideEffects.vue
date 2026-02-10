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
  <div>
    <div style="margin-top: 40px; margin-bottom: 40px" class="container-fluid">
      <h1>Metabolovigilance</h1>
      <p>
        <b>Pharmacovigilance:</b> Tracking the side effects of pharmaceuticals.
        <b>Metabolomics:</b> Studying the small molecules produced by metabolism.
        <b>Metabolovigilance:</b> A tool to aid identification of the drugs and drug metabolites
        that cause side effects. Note: Placebo side effects have been removed. Drug names in the
        following tables are links to get updated side effects from the
        <a href="https://www.fda.gov">FDA</a>.<br />
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
      </p>
      <div class="accordion" id="dockingAccordion">
        <div class="accordion-item">
          <h2 class="accordion-header">
            <button
              class="accordion-button collapsed"
              type="button"
              data-bs-toggle="collapse"
              data-bs-target="#dockingAccordionItem"
              aria-expanded="true"
              aria-controls="dockingAccordionItem"
            >
              Metabolovigilance Tutorial
            </button>
          </h2>
        </div>
        <div
          id="dockingAccordionItem"
          class="accordion-collapse collapse"
          data-bs-parent="#dockingAccordion"
        >
          <div class="accordion-body">
            <div
              style="
                position: relative;
                padding-bottom: calc(77.2093% + 41px);
                height: 0px;
                width: 100%;
              "
            >
              <!--ARCADE EMBED START-->
              <iframe
                src="https://demo.arcade.software/vgH36FFoKT1fdhqE6hNK?embed&embed_mobile=tab&embed_desktop=inline&show_copy_link=true"
                title="Find drugs and metabolites linked to selected side effects"
                frameborder="0"
                loading="lazy"
                webkitallowfullscreen
                mozallowfullscreen
                allowfullscreen
                allow="clipboard-write"
                style="
                  position: absolute;
                  top: 0;
                  left: 0;
                  width: 100%;
                  height: 100%;
                  color-scheme: light;
                "
              ></iframe>
            </div>
            <!--ARCADE EMBED END-->
          </div>
        </div>
      </div>

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
                :data-test-id="`grid-add-button-${props.rowIndex}`"
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
                :data-test-id="`grid-add-button-${props.rowIndex}`"
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
              :on-click="
                () =>
                  metabolovigilanceStore.fetchPrecursorsForDrugs({
                    precursor_UUIDs: metabolovigilanceStore.selectedDrugs.map((drug) => drug.UUID)
                  })
              "
            />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
