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
const wordToColor = ref(null)
const wordFrequency = ref(null)


const yearMin = ref(null)
const yearMax = ref(null)




function fetchWordClouds(){
  axios.get(
      'http://127.0.0.1:8000/app/word_cloud/word_frequency',
      {params: {year_min: yearMin.value, year_max: yearMax.value}}
  ).catch(
      (error) =>{
        if (error.response) {
          // The request was made and the server responded with a status code
          // that falls out of the range of 2xx

          console.log(`Response with code error: ${error.response.status}`);
          console.log(`Failed response data: ${error.response.data}`);
          console.log(`Response headers: ${error.response.headers}`);
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