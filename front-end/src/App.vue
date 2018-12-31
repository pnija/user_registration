<template>
  <div id="app">
    <div class="top-bar">
      <router-link :to="'/home'">Home</router-link>
      <button  v-if="Object.keys($store.state.loggedInUser).length > 0"  type="button" @click="logout">Logout</button>
    </div>
    <router-view/>
  </div>
</template>
<script>
export default {
  name: 'App',
  methods : {
    logout(){
      this.$store.commit('logout', this.$router);
    }
  }
}
</script>
<style>
.top-bar{
  width: 100%;
  background-color: #dcd9d9;
  text-align: end;
}
</style>
