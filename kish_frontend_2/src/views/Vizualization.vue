<template>
<Slider 
@update-albums="(newAlbums: string[]) => albumsTitles=newAlbums"/>
<WordCloud :albums="albumsTitles"></WordCloud>
</template> 


<script setup lang="ts">
import WordCloud from "@/components/WordCloud.vue"
import Slider from "@/components/Slider.vue"
import * as consts from "@/modules/consts"

import { ref, computed, watch } from 'vue';

const albumsTitles = ref(consts.albums.map(album => album.title))


</script>