<template>
   <v-app id="inspire">
      <v-main>
         <v-container fluid fill-height>
            <v-layout align-center justify-center>
               <v-flex xs12 sm8 md4>
                  <v-card class="elevation-12">
                     <v-toolbar dark color="primary">
                        <v-toolbar-title>Signup</v-toolbar-title>
                     </v-toolbar>
                     <v-card-text>
                        <v-form ref="form" v-model="valid" lazy-validation>
                            <v-text-field
                              name="name"
                              label="Name"
                              type="text"
                              v-model="name"
                              :rules="nameRules"                              
                              placeholder="Name"
                              required
                           ></v-text-field>
                           <v-text-field
                              name="email"
                              label="Email"                          
                              type="text"
                              v-model="email"
                              placeholder="Email"
                              :rules="emailRules"                                  
                              required
                           ></v-text-field>
                           <v-text-field
                              name="password"
                              label="Password"
                              type="password"
                              v-model="password"
                              placeholder="Password"
                              required
                           ></v-text-field>
                        </v-form>
                     </v-card-text>
                     <v-card-actions>
                        <v-spacer></v-spacer>
                        <v-btn color="primary" @click="signupHandler">Signup</v-btn>
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
   name: 'UserSignup',
   data() {
      return {
         valid: true,
         name: '',
            nameRules: [
            v => !!v || 'Name is required',
            v => (v && v.length <= 10) || 'Name must be less than 10 characters',
            ],
            email: '',
            emailRules: [
            v => !!v || 'E-mail is required',
            v => /.+@.+\..+/.test(v) || 'E-mail must be valid',
            ],  
         password: null,
      }
   },
   methods: {
      validate () {
        this.$refs.form.validate()
      },      
      async signupHandler() {
         const data = {
            'name': this.name,
            'email': this.email,
            'password': this.password
         }
         console.log(data);
         try {
             const res = await this.$axios.post('/auth/signup', data)
             console.log(res)
         }
         catch(e) {
             console.log(e.message)
         }
         await this.$router.push('/auth/login');               
      }
   }
};
</script>

<style></style>
