import Vue from 'vue'
import Vuex from 'vuex'
import createPersistedState from 'vuex-persistedstate';
Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    loggedInUser : {}
  },
  mutations: {
    login (state, payload) {
      state.loggedInUser = payload;
    },
    initializeState (state) {
      state.loggedInUser = {};
    },
    updateName (state,payload) {
      state.loggedInUser.name = payload;
    },
    logout (state, router) {
      state.loggedInUser = {};
      router.push('/login');
    }
  },
  actions: {

  },
  plugins: [createPersistedState()]
})
