<template>
<div class="year-select-buttons">
  <div class="select-button-title">Год начала</div>
    <button 
      v-for="year in consts.albumYears" :key="year"
      @click="changStartYear(year)"
      class="select-button"
      :class = "{'button-active' : year === startYear}"
      :title="getHoverTextByYear(year)"
    >
      {{ year }}
    </button>


  <div class="select-button-title">Год конца</div>
  <button 
      v-for="year in consts.albumYears" :key="year"
      @click="changeEndYear(year)"
      class="select-button"
      :class = "{'button-active' : year === endYear}"
      :title="getHoverTextByYear(year)"
    >
      {{ year }}
    </button>
  <div class="selected-albums-text">Выбранные альбомы:</div>
  <div class="selected-albums-list">
    <ul>
      <li v-for="(album, index) in selectedAlbums" :key="index">
        {{  album.title }}
      </li>
    </ul>
  </div>

</div>


</template>


<script setup lang="ts">
import {reactive, ref, onMounted, computed, watch} from "vue";
import type {Ref} from "vue";
import * as consts from '@/modules/consts';


const emit = defineEmits<{
  updateStartYear: [year: number]
  updateEndYear: [year: number]
}>()

function changStartYear(year: number): void {
  startYear.value = year;
}

function changeEndYear(year: number): void {
  endYear.value = year;
}

function getHoverTextByYear(year: number): string {
  let hoverText = "";
  consts.albums.forEach(album => {
    if (album.year === year) {
      hoverText += `${album.title}\n`;
    }
  })
  return hoverText;
}

let startYear: Ref<number> = ref(consts.minYear);
let endYear: Ref<number> = ref(consts.maxYear);



watch( [startYear, endYear], 
  ([newStartYear, newEndYear], [oldStartYear, oldEndYear]) => {
    swapStartEndIfNeeded(newStartYear, newEndYear)
    emitIfNeeded(newStartYear, newEndYear, oldStartYear, oldEndYear);
})

function swapStartEndIfNeeded(newStartYear: number, newEndYear: number): void {
  if (newStartYear > newEndYear) {
    startYear.value = newEndYear;
    endYear.value = newStartYear;
  }
}

function emitIfNeeded(
  newStartYear: number, 
  newEndYear: number,
  oldStartYear: number,
  oldEndYear: number
){
  if (newStartYear != oldStartYear) {
    emit("updateStartYear", newStartYear);
  }
  if (newEndYear!= oldEndYear) {
    emit("updateEndYear", newEndYear);
  }
}

let selectedAlbums = computed(() => 
  consts.albums.filter(
    (album) => album.year >= startYear.value && album.year <= endYear.value
  )
)

</script>

<style scoped>
.button-active {
  color: red;
}
</style>