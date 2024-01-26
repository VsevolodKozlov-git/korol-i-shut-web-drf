<template>
 <h1>Hello world</h1>
  <div v-if="wordCloudAll">
    <div v-html="wordCloudAll"></div>
  </div>
</template>

<script setup>

import {onMounted, ref} from "vue";
import axios from "axios";

const wordCloudAll = ref(null)

function fetchWordClouds(){
  axios.get(
      'http://127.0.0.1:8000/app/word_cloud/all'
  ).catch(
      (error) =>{
        if (error.response) {
          // The request was made and the server responded with a status code
          // that falls out of the range of 2xx
          console.log(error.response.data);
          console.log(error.response.status);
          console.log(error.response.headers);
        } else if (error.request) {
          // The request was made but no response was received
          // `error.request` is an instance of XMLHttpRequest in the browser and an instance of
          // http.ClientRequest in node.js
          console.log(error.request);
        } else {
          // Something happened in setting up the request that triggered an Error
          console.log('Error', error.message);
        }
        console.log(error.config);
        throw error;
      }
  ).then(
      (response) =>{
        wordCloudAll.value = response.data['svg']
      }
  )
}

onMounted(fetchWordClouds)
</script>

<style scoped>

</style>