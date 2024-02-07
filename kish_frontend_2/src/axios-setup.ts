import axios from "axios";
import type { AxiosResponse, AxiosError} from "axios";

declare module "axios"{
  export interface AxiosRequestConfig {
    raw?: boolean;
  }
}

class HttpError extends Error{
  constructor(message?: string){
    super(message)
    this.name = 'HttpError'
    Object.setPrototypeOf(this, new.target.prototype)
  }
}


function responseHandler(response: AxiosResponse<any>): AxiosResponse{ 
  // Run only if 2xx response
  const config = response.config;
  if (config.raw){
    return response;
  }
  if (response.status == 200){
    const data = response.data;
    if (!data) {
      throw new HttpError('API Error. No data!')
    }
    return data
  }
  // If 2xx and != 200 
  throw new HttpError("Api error: " + response.statusText);

}

function errorHandler(error: AxiosError){
  // 
  const config = error.config;
  if (!config){
    console.log("Config is undefined in error. Error happened during request setUP")
    return Promise.reject(error);
  }
  if (config.raw){
    return Promise.reject(error);
  }
  return defaultErrorLogger(error);
}


function defaultErrorLogger(error: AxiosError){
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
axios.interceptors.response.use(responseHandler, errorHandler);