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
// Add a request interceptor
axios.interceptors.request.use(function (config) {
  if(Object.keys(store.state.loggedInUser).length > 0){
    config.headers.Authorization = JSON.stringify(store.state.loggedInUser);
  }
  return config;
});
Vue.prototype.$http = axios;

//Configure router for authorized access
router.beforeEach((to, from, next) => {
  // redirect to login page if not logged in and trying to access a restricted page
  const publicPages = ['login', 'register'];
  var authRequired =  true;
  if(publicPages.includes(to.name)){
    authRequired = false
    store.commit('initializeState');
  }
  if (authRequired && !(Object.keys(store.state.loggedInUser).length > 0)) {
    return next('/login');
  }
  next();
})


new Vue({
  router,
  store,
  render: h => h(App)
}).$mount('#app')
