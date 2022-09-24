const login = {
    template:  `<section  class="ftco-section">
    <div class="container">
    <div class="row justify-content-center">
    <div class="col-md-6 text-center mb-5 ">
    <br>
    <br>
    <h2 class="heading-section" style="color:#3C3E64">{{header}}</h2>
    </div>
<div v-if="errors.length">
  <div v-for="error in errors">
<div class="alert alert-danger alert-dismissible fade show" role="alert">
    <strong>{{error}}</strong> 
    <button type="button" class="btn-close" @click="errorpop(error)"></button>
</div>
</div>
</div>

        <div class="row justify-content-center ">
            <div class="col-md-6 col-lg-4" >
                <div class="login-wrap py-5" >
              <div class="img d-flex align-items-center justify-content-center"></div>
                    <form @submit="checkForm"  class="login-form form"  novalidate="true" >
                  <div class="form-group">
                      <div class="icon d-flex align-items-center justify-content-center"><span class="fa fa-user"></span></div>
                      <input v-model="formData.username" type="text" class="form-control" name="username" placeholder="Username" >
                      <br>
                  </div>
                  <div class="form-group">
                  <div class="icon d-flex align-items-center justify-content-center"><span class="fa fa-lock"></span></div>
                <input v-model="formData.email" type="email" class="form-control" name="email" placeholder="Email" >
                <br>
              </div>
            <div class="form-group">
                <div class="icon d-flex align-items-center justify-content-center"><span class="fa fa-lock"></span></div>
              <input v-model="formData.password" type="password" class="form-control" name="password" placeholder="Password" >
              <br>
            </div>
            <div class="form-group">
                <button type="submit" class="btn form-control btn-primary rounded submit px-3"  >{{button}}</button>
            </div>
          </form>
        </div>
            </div>
        </div>
    </div>
    </div>
</section>

`,
  
    data() {
      return {
        header: "Login Page",
        button:"Login",
        errors:[],
        formData: {
          username:"",
          email: '',
          password: '',
        },
      }
    },
  
    methods: {
      async loginUser() {
        const res = await fetch('/login?include_auth_token', {
          method: 'post',
          credentials:'omit',
          headers: {
            'Content-Type': 'application/json',
          },
          credentials: 'omit',
          body: JSON.stringify(this.formData),
        }).then(response => response.json()).then(t=>
          {if (t.meta.code==200) {
            localStorage.setItem(
              'auth-token',
              t.response.user.authentication_token)
              this.$router.push('/dashboard/')
          } else {          
            if(t.meta.code==400){
              this.errors.push("Invalid Credentials");
            }
  
          }}
          );

       

      },
      checkForm: function (e) {

        this.errors = [];
    
        if (!this.formData.username) {
          this.errors.push('Name required.');
        }
        if (!this.formData.password) {
          this.errors.push('Password required.');
        }
        if (!this.formData.email) {
          this.errors.push('Email required.');
        } 
        else{
          if(this.formData.email.match(/^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/))
          {
              this.loginUser();
          }
          else
          {
            this.errors.push('Valid Email required.');
          }
        }
    
        e.preventDefault();
      },
    errorpop:function(e){
      this.errors=this.errors.filter(function(t){return t!==e})
    }, 
    
}

}
  
  export default login
  