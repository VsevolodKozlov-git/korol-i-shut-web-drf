<template>
  <Slider 
@update-albums="(newAlbums: string[]) => albumsTitles=newAlbums"/>
  <SentimentVizulization :albumsTitles="albumsTitles"/>
</template> 
  
  
  <script setup lang="ts">
  import SentimentVizulization from "@/components/SentimentVizualization.vue"
  import Slider from "@/components/Slider.vue"
  import * as consts from "@/modules/consts"
  import { ref } from 'vue';
  
  const albumsTitles = ref(consts.albums.map(album => album.title))
  
  </script>