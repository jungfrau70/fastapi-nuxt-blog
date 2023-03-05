<template>
  <v-container>
    <v-card class="mx-auto" max-width="600">
      <v-card-title>SignUp Form</v-card-title>

      <v-form>
        <v-container>
          <v-text-field v-model="signUpInfo.username" label="Name"></v-text-field>
          <v-text-field v-model="signUpInfo.email" label="E-mail"></v-text-field>          
          <v-text-field
            v-model="signUpInfo.password"
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
// import UserAuthForm from '@/components/UserAuthForm'

export default {
  // components: {
  //   UserAuthForm,
  // },
  data() {
    return {
        show: false,
        signUpInfo: {
            username: "",
            email: "",
            password: ""
        }

    };
  },
  methods: {
    // async registerUser() {
    //   this.loading = true;
    //   let data = this.register;
    //   try {
    //     await this.$axios.post("/signup", data);
    //     this.$router.push("/login");
    //     this.loading = false;
    //     this.$notify({
    //       group: "success",
    //       title: "Success!",
    //       text: "Account created successfully"
    //     });
    //   } catch (error) {
    //     this.loading = false;
    //     this.$notify({
    //       group: "error",
    //       title: "Error!",
    //       text: error.response
    //         ? error.response.data.error
    //         : "Sorry an error occured, check your internet"
    //     });
    //   }
    // }
    
    async signUpUser() {
      const formData = new FormData();
      formData.append("username", this.signUpInfo.username);
      formData.append("email", this.signUpInfo.email);      
      formData.append("password", this.signUpInfo.password);
      console.log(formData)
      try {
        await this.$axios.post('/users', FormData)
        await this.$auth.loginWith('local', {
          data: FormData
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
    },
  },
}
</script>

<style lang="scss" scoped>
</style>