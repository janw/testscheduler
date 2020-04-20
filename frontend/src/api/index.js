import axios from 'axios';

const apiRoot = process.env.API_ROOT ? process.env.API_ROOT : null;
const api = axios.create({
  baseURL: apiRoot,
});

const createErrorHandlerInterceptor = (api) => {
  return api.interceptors.response.use(
    (response) => {
      return response;
    },
    (error) => {
      console.error(error);
      return Promise.reject(error.response);
    }
  );
};

export default {
  install(Vue) {
    createErrorHandlerInterceptor(api);
    Vue.prototype.$api = api;
  },
};
