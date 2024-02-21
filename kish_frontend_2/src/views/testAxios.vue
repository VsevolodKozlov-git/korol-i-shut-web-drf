


<template>
<div>
<div>
  <div class="song-title" @click="r1=!r1">
    Title
  </div>

  <div class="song-lyrics-container">
    <div :class="{'song-lyrics': true, 'active': r1}">
      Some text inside
    </div>
  </div>
</div>

<div>
  <div class="song-title" @click="r2=!r2">
    Title
  </div>

  <div class="song-lyrics-container">
    <div :class="{'song-lyrics': true, 'active': r2}">
      Some text inside
    </div>
  </div>
</div>
</div>

  
</template>  

<script setup lang="ts">
import {ref} from "vue"
import type {Ref} from "vue"

const r1 = ref(false)
const r2 = ref(false)
</script>


<style lang="css" scoped>

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
  margin-top: -100%;
  transition: all 0.2s ease-out;
  background-color: #f1f1f1;
}

.song-lyrics.active{
  margin-top: 0;
}

</style>