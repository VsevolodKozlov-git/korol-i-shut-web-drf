<template>
<Slider 
@update-start-year="(year: number) => startYear=year"
@update-end-year="(year: number) => endYear=year"/>
<WordCloud :start-year="startYear" :end-year="endYear"></WordCloud>
</template> 


<script setup lang="ts">
import WordCloud from "@/components/WordCloud.vue"
import Slider from "@/components/Slider.vue"
import * as consts from "@/modules/consts"

import { ref, computed, watch } from 'vue';

const startYear = ref(consts.minYear);
const endYear = ref(consts.maxYear);

</script>