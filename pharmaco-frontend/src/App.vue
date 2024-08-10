<script setup lang="ts">
import { RouterView } from 'vue-router'
import './scss/styles.scss'
import NavBar from './components/navbar/NavBar.vue'
import Footer from './components/footer/Footer.vue'
</script>

<template>
  <NavBar />
  <div class="d-flex flex-col">
    <RouterView />
  </div>
  <Footer />
</template>
