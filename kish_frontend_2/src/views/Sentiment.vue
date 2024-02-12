<template>
  <Slider 
  @update-start-year="(year: number) => startYear=year"
  @update-end-year="(year: number) => endYear=year"/>
  <SentimentVizulization :start-year="startYear" :end-year="endYear"/>
  </template> 
  
  
  <script setup lang="ts">
  import SentimentVizulization from "@/components/SentimentVizualization.vue"
  import Slider from "@/components/Slider.vue"
  import * as consts from "@/modules/consts"
  import { ref } from 'vue';
  
  const startYear = ref(consts.minYear);
  const endYear = ref(consts.maxYear);
  
  </script>