<template>
  <div class="home">
    <h2>Welcome to TV_TEST App</h2>
    <p>
      Logged in as {{$store.state.loggedInUser.name}}. <router-link :to="'/profile'">Click here to edit your profile</router-link>
    </p>
  </div>
</template>

<script>

export default {
  name: 'home',
}
</script>
<style scoped>
.home{
  text-align: center
}
</style>

