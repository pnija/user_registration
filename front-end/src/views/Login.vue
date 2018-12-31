<template>
  <div class="login">
    <div class="container py-5">
      <div class="row">
        <div class="col-md-12">
          <h2 class="text-center text-black mb-4">TV_TEST App</h2>
          <div class="row">
            <div class="col-md-6 mx-auto">
              <div class="card rounded-0">
                <div class="card-header">
                  <h3 class="mb-0">Login</h3>
                </div>
                <div class="card-body">
                  <form class="form">
                    <div class="form-group">
                      <label for="username">Username</label>
                      <input type="text" class="form-control form-control-lg rounded-0" name="username" v-model.trim="username" v-validate="'required'" :data-vv-as="'username'">
                      <div class="error" v-show="errors.has('username')">{{errors.first('username')}}</div>
                    </div>
                    <div class="form-group">
                      <label>Password</label>
                      <input type="password" class="form-control form-control-lg rounded-0" name="password" v-model.trim="password" v-validate="'required'" :data-vv-as="'password'">
                      <div class="error" v-show="errors.has('password')">{{errors.first('password')}}</div>
                    </div>
                    <div class="error" v-show="generalError !== ''">{{generalError}}</div>
                    <button type="button" class="btn btn-success btn-lg float-right" @click="login">Login</button>
                  </form>
                  <router-link :to="'/register'">New user? Click to register</router-link>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>

export default {
  name: 'login',
  data(){
    return {
      username : '',
      password : '',
      generalError : ''
    }
  },
  methods : {
    login(){
      this.generalError = '';
      this.$validator.validateAll().then(success => {
          if (this.errors.any()) {
              return;
          }
          let request = {
            name :  this.username,
            password : this.password
          }
          this.$http.post('usermanagement/login/', request).then(response => {
            this.$store.commit("login", response.data);
            this.$router.push('/home');
          },error => {
            this.generalError = error.response.data.status;
          });
      }); 
    }
  },
  created(){
    this.$store.commit("initializeState", {});
  }
}
</script>
