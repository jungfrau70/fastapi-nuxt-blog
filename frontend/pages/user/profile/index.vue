<template>
    <v-app>
      <v-container fluid>
        <v-card class="mx-auto" max-width="400px">
          <v-card-title>
            <v-row>
              <v-col class="d-flex" cols="12" xs="12" sm="6">
                <v-row align="center" justify="center">
                  <v-avatar size="96" class="mr-4">
                    <img v-if="form.imgUrl" :src="form.imgUrl" alt="Avatar" />
                    <v-icon v-else size="96">mdi-account</v-icon>
                  </v-avatar>
                </v-row>
              </v-col>
              <v-col class="d-flex" cols="12" xs="12" sm="6">
                <v-row align="center" justify="left">
                  <v-btn class="teal lighten-1" @click.native="toUpdate"
                    >Change profile</v-btn
                  >
                </v-row>
              </v-col>
            </v-row>
          </v-card-title>
          <v-card-text>
            <v-text-field
              v-model="form.userName"
              label="Username"
              readonly
            ></v-text-field>
            <v-text-field
              v-model="form.contactEmail"
              label="Email Address"
              readonly
            ></v-text-field>
          </v-card-text>
        </v-card>
      </v-container>
    </v-app>
</template>

<script>
export default {
pageTitle: "Profile",
data() {
    return {
      form: {
        imgUrl: null, 
        userName: null, 
        contactEmail: null,
      },
    };
},
methods: {
    toUpdate() {
      this.$router.push("/user/profile/update/");
    },
},
};
</script>

<!-- imgUrl: null, // this.$auth.user.icon,
userName: null, // this.$auth.user.username,
contactEmail: null //this.$auth.user.email, -->