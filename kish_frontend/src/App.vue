<template>
  <router-link to="/visualization">visualization</router-link>
  <router-view></router-view>
</template>

<script setup>
import HelloWorld from './components/HelloWorld.vue'
import {onMounted} from "vue";
import axios from "axios";


class HttpError extends Error {
  constructor(message) {
    super(message); // Call the constructor of the Error class
    this.name = 'HttpError'; // Set the error name to 'HttpError'
    Object.setPrototypeOf(this, new.target.prototype); // Restore prototype chain
  }
}

function responseHandler(response) {
  console.log('In response handler')
  // Получаем config. Мы получаем его из запроса
  const config = response?.config;
  // Если raw, то просто вернуть
  if (config.raw) {
    return response;
  }
  // Иначе вернуть data
  if (response.status === 200) {
    const data = response?.data;
    if (!data) {
      throw new HttpError('API Error. No data!');
    }
    return data;
  }
  console.log('Сработала HttpError')
  // Вопрос: А что если ошибка 401? Будет ли вызвана эта ошибка
  throw new HttpError('API Error! Invalid status code!');
}




function responseErrorHandler(error) {
  const config = error?.config;
  if (config.raw) {
    return error;
  }
  return defaultErrorLogger(error)
}

function defaultErrorLogger(error){
  if (error.response) {
    // The request was made and the server responded with a status code
    // that falls out of the range of 2xx
    console.error("Error response status:", error.response.status);
    console.error("Error response data:", error.response.data);
    console.error("Error response headers:", error.response.headers);
  } else if (error.request) {
    // The request was made but no response was received
    console.error("No response received for request:", error.request);
  } else {
    // Something happened in setting up the request that triggered an Error
    console.error("Error in setting up the request:", error.message);
  }

  // Log the config of the request for debugging purposes
  console.error("Request config:", error.config);

  return Promise.reject(error);
}

// Register interceptor like this
axios.interceptors.response.use(responseHandler, responseErrorHandler);

function mountedFunc(){
  axios.get(
      'http://127.0.0.1:8000/app/word_cloud/word_frequency',
      {params: {tag_type:'noun'}}
  ).then((response) =>{
    console.log(response)
  })

}

onMounted(mountedFunc)
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
