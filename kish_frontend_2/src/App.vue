<script setup lang="ts">
import { RouterLink, RouterView } from 'vue-router'
</script>

<template>
<v-app>
    
    <v-app-bar
    app
    color="#ffffff"
    >
      <v-app-bar-title>
        <h3 class="text-h4">КиШ Analysis</h3>
      </v-app-bar-title>
    </v-app-bar>
    
    <v-main>
      <router-view></router-view>
    </v-main>
    
  </v-app>
  <div class="wrapper">
      <nav>
        <RouterLink to="/test">Test</RouterLink>
        <RouterLink to="/word_cloud">WordCloud</RouterLink>
      </nav>
    </div>

  
</template>

<style scoped>

.white-font{
  color: #ffffff
}
</style>
