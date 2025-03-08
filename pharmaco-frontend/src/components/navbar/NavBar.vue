<script setup lang="ts">
import logo from '../../assets/logo-black.png'
import { RouterLink, useRoute } from 'vue-router'
import { PATH_NAME, paths } from '../../constants/paths'

const route = useRoute()

const isActive = (path: string) => {
  return route.path === path
}
</script>

<template>
  <nav class="navbar fixed-top navbar-expand-lg" style="color: #ffffff; background: #2b2f31">
    <div class="container-fluid">
      <a class="navbar-brand text-white" href="/">
        <img height="30" width="30" :src="logo" />
        CU Denver Pharmacogenomics
      </a>
      <button
        class="navbar-toggler"
        type="button"
        data-bs-toggle="collapse"
        data-bs-target="#navbarSupportedContent"
        aria-controls="navbarSupportedContent"
        aria-expanded="false"
        aria-label="Toggle navigation"
      >
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse" id="navbarSupportedContent">
        <ul class="navbar-nav me-auto mb-2 mb-lg-0">
          <li class="nav-item">
            <RouterLink
              class="nav-link text-white"
              :class="{ active: isActive(paths[PATH_NAME.METABOLOVIGILANCE]) }"
              :to="paths[PATH_NAME.METABOLOVIGILANCE]"
              >Metabolovigilance</RouterLink
            >
          </li>
          <li class="nav-item">
            <RouterLink
              class="nav-link text-white"
              :class="{ active: isActive(paths[PATH_NAME.GTEXOME]) }"
              :to="paths[PATH_NAME.GTEXOME]"
              >GTExome</RouterLink
            >
          </li>
          <li class="nav-item">
            <RouterLink
              class="nav-link text-white"
              :class="{ active: isActive(paths[PATH_NAME.PEOPLE]) }"
              :to="paths[PATH_NAME.PEOPLE]"
              >People</RouterLink
            >
          </li>
          <li class="nav-item">
            <RouterLink
              class="nav-link text-white"
              :class="{ active: isActive(paths[PATH_NAME.CONTACT]) }"
              :to="paths[PATH_NAME.CONTACT]"
              >Contact</RouterLink
            >
          </li>
          <li class="nav-item">
            <RouterLink
              class="nav-link text-white"
              :class="{ active: isActive(paths[PATH_NAME.API_ACCESS]) }"
              :to="paths[PATH_NAME.API_ACCESS]"
              >API Access</RouterLink
            >
          </li>
        </ul>
      </div>
    </div>
  </nav>
</template>
