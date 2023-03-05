<template>
  <v-app id="inspire">
    <v-main>
      <v-container fluid fill-height>
        <v-layout align-center justify-center>
          <v-flex xs12 sm8 md4>
            <v-card class="elevation-12">
              <v-toolbar dark color="primary">
                <v-toolbar-title>Login</v-toolbar-title>
              </v-toolbar>
              <v-card-text>
                <v-form>
                  <v-text-field
                    v-model="email"
                    name="username"
                    label="Username"
                    type="email"
                    placeholder="Email"
                    required
                  ></v-text-field>
                  <v-text-field
                    v-model="password"
                    name="password"
                    label="Password"
                    type="password"
                    placeholder="Password"
                    required
                  ></v-text-field>
                </v-form>
              </v-card-text>
              <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn color="primary" @click="loginHandler">Login</v-btn>
              </v-card-actions>
            </v-card>
          </v-flex>
        </v-layout>
      </v-container>
    </v-main>
  </v-app>
</template>

<script>
export default {
  name: 'UserLogin',
  data() {
    return {
      email: '',
      password: '',
    }
  },
  methods: {
    async loginHandler() {
      const data = { username: this.email, password: this.password }
      console.log(data)
      try {
        // const response = await this.$auth.loginWith('local', { data: data}) || await this.$axios.post('/user/login', data)
        // console.log(response)

        const response = await this.$axios.post('/auth/signup', data)

        this.$auth.$storage.setUniversal('bearer', response.data.access_token)
        await this.$auth.setUserToken(
          response.data.access_token,
          response.data.refresh_token
        )
      } catch (e) {
        console.log(e.message)
      }
      await this.$router.push('/')
    },
  },
}
</script>

<style></style>
