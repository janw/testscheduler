import Vue from 'vue';

import BootstrapVue from 'bootstrap-vue';
Vue.use(BootstrapVue);

import VueSpinners from 'vue-spinners';
Vue.use(VueSpinners);

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
