import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import VeeValidate from 'vee-validate';
import axios from "axios"
window.jQuery = window.$ = require("jquery");
import 'bootstrap';
import 'bootstrap/dist/css/bootstrap.min.css';
import Toasted from 'vue-toasted';
require("./assets/common.css")
Vue.use(Toasted, {
  position : 'top-center',
  duration : 2000
})


Vue.config.productionTip = false
Vue.use(VeeValidate);
axios.defaults.baseURL = process.env.VUE_APP_API_URL;
Vue.prototype.$http = axios;


new Vue({
  router,
  store,
  render: h => h(App)
}).$mount('#app')
