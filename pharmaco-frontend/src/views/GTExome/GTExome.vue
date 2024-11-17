<script setup lang="tsx">
import { ApiLoadingState } from '@/constants/enums'
import { GTExomeTab } from '@/constants/enums'
import { useGTExomeStore } from '@/stores/GTExomeStore'
import GTEx from '@/views/GTExome/gtex/GTEx.vue'
import Exac from '@/views/GTExome/exac/Exac.vue'
import Refold from '@/views/GTExome/refold/refold.vue'
import { useRoute } from 'vue-router'
import Upload from './upload/upload.vue'

const GTExomeStore = useGTExomeStore()

const route = useRoute()
const CCID = route.query.CCID
const geneID = route.query.geneID

if (CCID != undefined && geneID != undefined) {
  GTExomeStore.setSelectedTab(GTExomeTab.refold)
}

if (GTExomeStore.tissueLoadingState != ApiLoadingState.Success) {
  GTExomeStore.fetchTissueTypes()
}
</script>
<template>
  <div style="margin-top: 40px; margin-bottom: 40px" class="flex-col w-100">
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
      <li class="nav-item" role="presentation">
        <button
          class="nav-link"
          @click="GTExomeStore.setSelectedTab(GTExomeTab.upload)"
          :class="{ active: GTExomeStore.selectedTab == GTExomeTab.upload }"
          id="upload-tab"
          type="button"
          role="tab"
        >
          upload
        </button>
      </li>
    </ul>
    <div v-show="GTExomeStore.selectedTab === GTExomeTab.gtex">
      <GTEx />
    </div>
    <div v-show="GTExomeStore.selectedTab === GTExomeTab.exac"><Exac /></div>
    <div v-show="GTExomeStore.selectedTab === GTExomeTab.refold"><Refold /></div>
    <div v-show="GTExomeStore.selectedTab === GTExomeTab.upload"><Upload /></div>
  </div>
</template>
