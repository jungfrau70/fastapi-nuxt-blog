<template>
    <v-container>
      <v-card class="mx-auto" max-width="600">
        <v-card-title>SignUp Form</v-card-title>
  
        <v-form>
          <v-container>
            <v-text-field v-model="login.username" label="Name"></v-text-field>
            <v-text-field v-model="login.email" label="E-mail"></v-text-field>            
            <v-text-field
              v-model="login.password"
              :append-icon="show ? 'mdi-eye' : 'mdi-eye-off'"
              :type="show ? 'text' : 'password'"
              name="password"
              label="Password"
              hint="At least 8 characters"
              class="input-group--focused"
              @click:append="show = !show"
            ></v-text-field>
          </v-container>
          <v-card-actions>
            <v-btn class="mr-4" @click="signUpUser">SignUp</v-btn>
          </v-card-actions>
        </v-form>
      </v-card>
    </v-container>
</template>
  
<script>
  export default {
    middleware({ store, redirect }) {
        if (store.$auth.loggedIn) {
            redirect("/");
        }
    },
    data() {
        return {
            show: false,
            login: {
            username: "",
            email: "",
            password: ""
            }
        };
    },
    methods: {
      async signUpUser(signUpInfo) {
        try {
          const formData = new FormData();
          formData.append("username", this.login.username);
          formData.append("email", this.login.username);
          formData.append("password", this.login.password);
          await this.$axios.post('/users', formData)

          // try {
          //     this.$auth
          //         .loginWith("local", { data: formData })

          // await this.$axios.post('/users', formData)
          await this.$auth.loginWith('local', {
            data: formData
          })
          // debugger
          this.$store.dispatch('snackbar/setSnackbar', {
            text: `Thanks for signing up, ${this.$auth.user.username}`,
          })
          this.$router.push('/')
        } catch (error) {
          this.$store.dispatch('snackbar/setSnackbar', {
            color: 'red',
            text: 'There was an issue signing up, please try again',
          })
        }

        // userSignUp() {
        //     let formData = new FormData();
        //     formData.append("username", this.login.username);
        //     formData.append("email", this.login.username);
        //     formData.append("password", this.login.password);
        //     try {
        //         this.$auth
        //             .loginWith("local", { data: formData })
        //             .then(res => {
        //             console.log("success");
        //             })
        //             .catch(err => {
        //             console.log(err);
        //             });
        //     } catch (err) {
        //         err => {
        //             console.log(err);
        //         };
        //     }
        // }
      }
    }
  };
</script>