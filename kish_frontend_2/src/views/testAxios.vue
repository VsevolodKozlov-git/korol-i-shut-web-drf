<script setup lang="ts">
import axios from 'axios';
import { onMounted } from 'vue';

function mountFunction(){
  axios.get(
      'http://127.0.0.1:8000/app/word_cloud/word_frequency',
      {params:{tag_type: "noun" }}
  ).then(response => {
    console.log("Normal response:");
    console.log(response);
  }).catch((error) => {
    console.log(error);
  })
}

onMounted(mountFunction);

</script>



<template>
  <h1>Hello world</h1>
</template>  


<style lang="css" scoped>

</style>