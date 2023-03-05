<template>
  <v-container>
    <!-- <h1>SignUp</h1> -->
    <UserAuthForm
      button-text="SignUp"
      :submit-form="signUpUser"
      has-name="true"
    />
  </v-container>
</template>
  
<script>
import UserAuthForm from '@/components/UserAuthForm'

export default {
  components: {
    UserAuthForm,
  },
  // data() {
  //   return {
  //     show: false,
  //     login: {
  //       username: "",
  //       password: ""
  //     }
  // };
  // },
  methods: {
    userLogin(loginInfo) {
        const formData = new FormData();
        formData.append("username", loginInfo.email);
        formData.append("password", loginInfo.password);
        try {
            this.$auth
                .loginWith("local", { data: formData })
                .then(res => {
                console.log("success");
                })
                .catch(err => {
                console.log(err);
                });
        } catch (err) {
          console.log(err);
        }
    },

    async signUpUser(signUpInfo) {
      // const formData = new FormData();
      // formData.append("username", this.signUpInfo.email);
      // formData.append("password", this.signUpInfo.password);
      try {
        await this.$axios.post('/users', signUpInfo)
        await this.userLogin(signUpInfo)
        // await this.$auth.loginWith("local", { data: formData })
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