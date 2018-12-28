<template>
  <div id="app">
    <button  v-if="Object.keys($store.state.loggedInUser).length > 0" class="float-right" type="button" @click="logout">Logout</button>
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
  background-color: red
}
</style>
