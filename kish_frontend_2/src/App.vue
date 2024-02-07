<script setup lang="ts">
import { RouterLink, RouterView } from 'vue-router'
</script>

<template>
  <header>
    <div class="wrapper">
      <nav>
        <RouterLink to="/test">Test</RouterLink>
        <RouterLink to="/word_cloud">WordCloud</RouterLink>
      </nav>
    </div>

  </header>

  <RouterView />
</template>

<style scoped>
</style>
