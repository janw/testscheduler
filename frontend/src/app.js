import Vue from 'vue';

import { LayoutPlugin, SpinnerPlugin, CardPlugin } from 'bootstrap-vue';
Vue.use(LayoutPlugin);
Vue.use(SpinnerPlugin);
Vue.use(CardPlugin);

import Api from './api';
Vue.use(Api);

import router from './router';
import Main from './components/Main';

import VueSocketIO from 'vue-socket.io'
Vue.use(new VueSocketIO({
  connection: '//',
  options: { path: "/sock" }
}))


export default new Vue({
  el: '#app',
  router,
  template: '<Main/>',
  components: { Main },
});

import './scss/main.scss';
