<template>
  <div class="home">
    <h2>Welcome to TV_TEST App</h2>
    <router-link :to="'/profile'">Click here to edit your profile</router-link>
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

