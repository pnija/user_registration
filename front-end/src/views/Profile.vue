<template>
  <div class="profile">
    <div class="container py-5">
      <div class="row">
        <div class="col-md-12">
          <div class="row">
            <div class="col-md-6 mx-auto">
              <div class="card rounded-0">
                <div class="card-header">
                  <h3 class="mb-0">Update Profile</h3>
                </div>
                <div class="card-body">
                  <form class="form" role="form">
                    <div class="form-group">
                      <label for="name">Name</label>
                      <input type="text" class="form-control form-control-lg rounded-0" v-model.trim="userDetails.name" v-validate="'required'" :data-vv-as="'name'" name="name">
                      <div v-show="errors.has('name')" class="error">{{errors.first('name')}}</div>
                    </div>
                    <div class="form-group">
                      <label for="email">Email</label>
                      <input type="text" v-model.trim="userDetails.email" v-validate="'required|email'" :data-vv-as="'email'" class="form-control form-control-lg rounded-0" name="email">
                      <div  v-show="errors.has('email')" class="error">{{errors.first('email')}}</div>
                    </div>
                    <div  v-show="generalError != ''" class="error">{{generalError}}</div>
                    <button type="button" @click="updateUser" class="btn btn-success btn-lg float-right">Edit</button>
                  </form>
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
      userDetails : {
        name : '',
        email : '',
      },
      generalError : ''
    }
  },
  methods : {
    updateUser(){
      this.generalError = '';
      this.$validator.validateAll().then(success => {
          if (this.errors.any()) {
              return;
          }
          let request = {
            email :  this.userDetails.email,
            name :  this.userDetails.name
          }
          this.$http.post('usermanagement/update_details/', request).then(response => {
            this.$toasted.success('Profile updated');
            this.$store.commit('updateName', response.data.name);
            this.getUserDetails();
          },error => {
            this.generalError = error.response.data;
            this.$toasted.error('Failed to update profile');
          });
      });  
    },
    getUserDetails(){
      this.$http.get('usermanagement/user_details/').then(response => {
        this.userDetails = response.data;
      });
    }
  },
  created(){
    this.getUserDetails();
  }
}
</script>
