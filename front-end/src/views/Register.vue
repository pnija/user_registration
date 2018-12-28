<template>
  <div class="register">
    <div class="container py-5">
      <div class="row">
        <div class="col-md-12">
          <div class="row">
            <div class="col-md-6 mx-auto">
              <div class="card rounded-0">
                <div class="card-header">
                  <h3 class="mb-0">Register</h3>
                </div>
                <div class="card-body">
                  <form class="form" role="form">
                    <div class="form-group">
                      <label for="name">Name</label>
                      <input type="text" class="form-control form-control-lg rounded-0" v-model.trim="name" v-validate="'required'" :data-vv-as="'name'" name="name">
                      <div v-show="errors.has('name')" class="error">{{errors.first('name')}}</div>
                    </div>
                    <div class="form-group">
                      <label for="email">Email</label>
                      <input type="text" v-model.trim="email" v-validate="'required|email'" :data-vv-as="'email'" class="form-control form-control-lg rounded-0" name="email">
                      <div  v-show="errors.has('email')" class="error">{{errors.first('email')}}</div>
                    </div>
                    <div class="form-group">
                      <label for="password1">Password</label>
                      <input type="password" v-model.trim="password" v-validate="'required'" :data-vv-as="'password'" class="form-control form-control-lg rounded-0" name="password1">
                      <div  class="error" v-show="errors.has('password1')">{{errors.first('password1')}}</div>
                    </div>
                    <button type="button" @click="registerUser" class="btn btn-success btn-lg float-right">Register</button>
                  </form>
                  <router-link :to="'/login'">Already a member? Click to login</router-link>
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
  name: 'register',
  data(){
    return  {
      name : '',
      email : '', 
      password : ''
    }
  },
  methods : {
    registerUser(){
      this.$validator.validateAll().then(success => {
          if (this.errors.any()) {
              return;
          }
          let request = {
            email :  this.email,
            name :  this.name,
            password : this.password
          }
          console.log(request);
          this.$http.post('usermanagement/register/', request).then(response => {
            this.$toasted.success('Registered');
            this.$router.push('/login');
          },error => {
            this.$toasted.error('Failed to register');
          });
      });  
    }
  }
}
</script>
