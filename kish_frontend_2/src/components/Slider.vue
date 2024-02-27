<template>

<div class="year-select-buttons">
  <v-card class="ma-10">
    <v-sheet class="mb-4" color="#323232">
      <v-container>
      <v-row justify="center">
        <div class="select-button-title ">Год начала</div>
      </v-row>

      <v-row  class="mt-5 px-11" justify="center">
        <v-btn 
        v-for="year in consts.albumYears"  :key="year" 
        @click="startYear = year"
        class="select-button my-2 mx-3"
        :class = "{'button-active' : year === startYear}"
        :title="getHoverTextByYear(year)">
          {{ year }}
        </v-btn>
      </v-row>
    </v-container>
    </v-sheet>

    <v-sheet color="#323232" rounded=100>
      <v-container>
        <v-row justify="center" class="select-button-title">
          Год конца
        </v-row>
        <v-row class="mt-5 px-11" justify="center">
            <v-btn v-for="year in consts.albumYears" :key="year" 
            @click="endYear = year"
            class="select-button my-2 mx-3"
            :class = "{'button-active' : year === endYear}"
            :title="getHoverTextByYear(year)">
              {{ year }}
            </v-btn>

        </v-row>
      </v-container>
    </v-sheet>
  </v-card>
    

  <v-card class="ma-10">
    <v-sheet color="#323232">
      <v-container>
        <v-row justify="center">
          <div class="select-button-title">Альбомы</div>
        </v-row>

        <v-row justify="center">
          <v-btn v-for="(albumElement, index) in albumElements" :key="index"
          class="mx-2 my-1"
          :class="{'button-active': albumElement.isSelected}"
          @click="albumElement.isSelected = !albumElement.isSelected"
          >
            {{  albumElement.title }}
          </v-btn>
        </v-row>
      </v-container>
    </v-sheet>
  </v-card>
</div>


</template>


<script setup lang="ts">
import {ref, computed, watch} from "vue";
import type {Ref} from "vue";
import * as consts from '@/modules/consts';

const emit = defineEmits<{
  updateAlbums: [albums: string[]]
}>()

let startYear: Ref<number> = ref(consts.minYear);
let endYear: Ref<number> = ref(consts.maxYear);

const albumElements = ref(getAlbumElements())

interface AlbumElement{
  title: string;
  isSelected: boolean;
}

function getAlbumElements(): AlbumElement[] {
  const yearFiltered = consts.albums.filter(
    (album) => album.year >= startYear.value && album.year <= endYear.value
  )
  const result: AlbumElement[] = [];
  yearFiltered.forEach((album) => {
    result.push({
      title: album.title,
      isSelected: true
    })
  })
  return result
}

watch( [startYear, endYear], 
  ([newStartYear, newEndYear], [oldStartYear, oldEndYear]) => {
    albumElements.value = getAlbumElements()
    swapStartEndIfNeeded(newStartYear, newEndYear)
})

function swapStartEndIfNeeded(newStartYear: number, newEndYear: number): void {
  if (newStartYear > newEndYear) {
    startYear.value = newEndYear;
    endYear.value = newStartYear;
  }
}

let selectedAlbumsTitles = computed(() => 
  albumElements.value.filter(
    (album) => album.isSelected
  ).map(
    album => album.title
  )
)

watch(selectedAlbumsTitles, 
  () => {
    emit('updateAlbums', selectedAlbumsTitles.value);
})


function getHoverTextByYear(year: number): string {
  let hoverText = "";
  consts.albums.forEach(album => {
    if (album.year === year) {
      hoverText += `${album.title}\n`;
    }
  })
  return hoverText;
}

</script>

<style scoped>

.button-active {
  /* color: red; */
  background-color: #2A73C5;
}

.select-button-title{
  font-weight: bold;
}
</style>