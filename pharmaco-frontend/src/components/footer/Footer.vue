<!-- eslint-disable vue/multi-word-component-names -->
<script setup lang="ts">
const currentYear = new Date().getFullYear()
</script>
<template>
  <footer class="footer fixed-bottom" style="color: #ffffff; background: #2b2f31">
    <div style="height: 2.5em; font-size: 1.25em">&copy; {{ currentYear }}</div>
  </footer>
</template>
