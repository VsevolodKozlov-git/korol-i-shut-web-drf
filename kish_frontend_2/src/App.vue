<template>
<v-app class="app">
    
  <v-app-bar app>
    <v-app-bar-nav-icon  @click.stop="drawer=!drawer"/>

    
    <v-app-bar-title>
      <div style="display: flex; flex-direction: row; align-items: center;">
        <h3 class="text-h4">Анализ творчества КиШ</h3>
        <img src="@/assets/panki_hoi.svg" alt="" style="height:60px; margin-right:16px;">
      </div>
    </v-app-bar-title>
  </v-app-bar>

  

  <v-navigation-drawer v-model="drawer" rail floating expand-on-hover width="100px">
    <v-list>
      <v-list-item 
      prepend-icon="mdi-chat-outline" 
      title="Облако слов" 
      :href="getHref('wordcloud')">
    </v-list-item>

      <v-list-item 
      prepend-icon="mdi-chart-box-outline" 
      title="Эмоциональный анализ" 
      :href="getHref('sentiment')"/>

      <v-list-item 
      prepend-icon="mdi-text-search" 
      title="Поиск по песням" 
      :href="getHref('songSearch')"/>
    </v-list>
  </v-navigation-drawer>
    
    
    <v-main>
      <router-view></router-view>
    </v-main>
  </v-app>
</template>


<script setup lang="ts">
import { RouterView } from 'vue-router'
import {ref} from "vue"
import type {Ref} from "vue"
import { useRouter } from 'vue-router';

const router = useRouter()

function getHref(name: string){
  return router.resolve({name: name}).href
}


const drawer: Ref<boolean> = ref(true)
</script>

<style scoped>

</style>
