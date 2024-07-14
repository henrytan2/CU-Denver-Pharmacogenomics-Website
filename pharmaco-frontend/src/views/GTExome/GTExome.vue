<script setup lang="tsx">
import { ApiLoadingState } from '@/constants/enums'
import { GTExomeTab, gtexFilter } from '@/constants/enums'
import { useGTExomeStore } from '@/stores/GTExomeStore'
import Button from '@/components/button/button.vue'
import GTEx from '@/views/GTExome/gtex/GTEx.vue'
import Exac from '@/views/GTExome/exac/Exac.vue'
import Refold from '@/views/GTExome/refold/refold.vue'

const GTExomeStore = useGTExomeStore()
if (GTExomeStore.tissueLoadingState != ApiLoadingState.Success) {
  GTExomeStore.fetchTissueTypes()
}
</script>
<template>
  <div style="margin-top: 40px; margin-bottom: 40px" class="container-fluid">
    <h3 class="lead">
      Details in our
      <a href="https://www.biorxiv.org/content/10.1101/2023.11.14.567143v1" target="_blank">
        preprint and
      </a>
      walkthough <a href="https://youtu.be/GQHd-mfWrM4" target="_blank"> VIDEO </a>
    </h3>
    <ul class="nav nav-tabs" id="myTab" role="tablist">
      <li class="nav-item" role="presentation">
        <button
          class="nav-link"
          @click="GTExomeStore.setSelectedTab(GTExomeTab.gtex)"
          :class="{ active: GTExomeStore.selectedTab == GTExomeTab.gtex }"
          id="gtex-tab"
          type="button"
          role="tab"
        >
          gtex
        </button>
      </li>
      <li class="nav-item" role="presentation">
        <button
          class="nav-link"
          @click="GTExomeStore.setSelectedTab(GTExomeTab.exac)"
          :class="{ active: GTExomeStore.selectedTab == GTExomeTab.exac }"
          id="exac-tab"
          type="button"
          role="tab"
        >
          exac
        </button>
      </li>
      <li class="nav-item" role="presentation">
        <button
          class="nav-link"
          @click="GTExomeStore.setSelectedTab(GTExomeTab.refold)"
          :class="{ active: GTExomeStore.selectedTab == GTExomeTab.refold }"
          id="refold-tab"
          type="button"
          role="tab"
        >
          refold
        </button>
      </li>
    </ul>
  </div>

  <div v-show="GTExomeStore.selectedTab === GTExomeTab.gtex">
    <GTEx />
  </div>
  <div v-show="GTExomeStore.selectedTab === GTExomeTab.exac"><Exac /></div>
  <div v-show="GTExomeStore.selectedTab === GTExomeTab.refold"><Refold /></div>
</template>
