<template>
<form @submit.prevent>
  <div>Песня о:</div><input type="text" v-model="userQuery" >
  <button @click="fetchMatches">Найти</button>
</form>


<div v-if="songMatches">
  <div v-for="songMatch, index in songMatches" :key="index">
    
    <div class="song-title" @click="isLyricsVisible![index] = !isLyricsVisible![index]">
      {{ songMatch.title }}
    </div>

    <div class="song-lyrics-container">
      <div :class="{'active': isLyricsVisible![index], 'song-lyrics': true}">
        <div v-for="line, index in songMatch.lyrics" :key="index">
          {{ line }}
        </div>
      </div>
    </div>

  </div>
</div>
</template>

<script setup lang="ts">
import { onMounted, ref, watch} from 'vue';
import type { Ref } from 'vue'
import axios from 'axios';

interface SongMatch{
  title: string
  lyrics: string[]
  similarity: number
}

const userQuery: Ref<null | string> = ref(null);
const songMatches: Ref<null | SongMatch[]> = ref(null)
const isLyricsVisible: Ref<boolean[] | null> = ref(null);



async function fetchMatches(){
  try {
      const response = await axios.post<SongMatch[]>(
        `http://127.0.0.1:8000/app/song/search`,{
          'query': userQuery.value,
        } );
      songMatches.value = response.data;
      isLyricsVisible.value = Array(response.data.length).fill(false);
    } 
  catch (error) {
    let isResolved = false
    if (axios.isAxiosError(error)){
      if (error.response){
        if (error.response.status === 403){
          const errorData = error.response.data;
          alert(errorData[0].detail)
          isResolved = true
        }
      }
      if (!isResolved){
        console.log(error)
      }
    }
    else {
      throw error;
    }
  }

}

</script>

<style scoped>
.song-title {
  background-color: #777;
  color: white;
  cursor: pointer;
  padding: 18px;
  width: 100%;
  border: none;
  text-align: left;
  outline: none;
  font-size: 15px;
}

.song-title:hover, .song-title.active {
  background-color: #555;
}

.song-lyrics-container{
  overflow: hidden;
}

.song-lyrics {
  padding: 0 18px;
  max-height: 0;
  transition: all 1s;
  background-color: #f1f1f1;
}

.song-lyrics.active{
  max-height: 1000px;
}
</style>