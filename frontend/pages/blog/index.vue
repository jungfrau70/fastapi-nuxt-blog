<template>
    <v-app white>
      <v-card color="grey lighten-4" flat height="50px" tile>
        <v-navigation-drawer v-model="leftDrawer" :left="left" temporary fixed>
          <v-list>
            <v-list-item
              v-for="(item, i) in items"
              :key="i"
              :to="item.to"
              router
              exact
            >
              <v-list-item-action>
                <v-icon>{{ item.icon }}</v-icon>
              </v-list-item-action>
              <v-list-item-content>
                <v-list-item-title v-model="item.title" />
              </v-list-item-content>
            </v-list-item>
          </v-list>
        </v-navigation-drawer>
        <v-app-bar dense fixed>
          <v-app-bar-nav-icon
            @click.stop="leftDrawer = !leftDrawer"
          ></v-app-bar-nav-icon>
  
          <v-toolbar-title>{{ title }}</v-toolbar-title>
  
          <v-spacer></v-spacer>
  
          <v-btn icon to="/blog/post/">
            <v-icon>mdi-pencil</v-icon>
          </v-btn>
  
          <v-btn icon to="/blog/dashboard">
            <v-icon>mdi-dresser</v-icon>
          </v-btn>
  


        <div v-if="$auth.loggedIn">
          {{ $auth.user.username }}
          <!-- {{ $auth.user.access_token }} -->
          <!-- <v-icon>mdi-logout @click="$auth.logout()</v-icon> -->
          <v-btn text @click="$auth.logout()"><v-icon>mdi-logout</v-icon></v-btn>
          <!-- <v-icon right dark >cloud_upload</v-icon> -->
          <v-btn icon to="/blog/profile">
            <v-icon>mdi-heart</v-icon>
          </v-btn>
        </div>
        <div v-else>
          <!-- <v-btn text to="/login">Login</v-btn>
          <v-btn text to="/signup">SignUp</v-btn> -->

          <v-btn icon to="/user/login">
            <v-icon>mdi-login</v-icon>
          </v-btn>
          
          <v-btn icon to="/user/signup">
            <v-icon>mdi-account</v-icon>
          </v-btn>
        </div>

        </v-app-bar>
      </v-card>
  
      <v-main>
        <v-container>
          <nuxt keep-alive />
        </v-container>
      </v-main>
  
      <v-footer :fixed="fixed" app>
        <span>&copy; {{ new Date().getFullYear() }}</span>
      </v-footer>
    </v-app>
</template>
<script>
export default {
    data() {
      return {
        clipped: false,
        fixed: false,
        title: "Blog",
        left: true,
        leftDrawer: false,
        items: [
          {
            icon: "mdi-apps",
            title: "Home",
            to: "/blog/",
          },
          {
            icon: "mdi-newspaper-variant",
            title: "List",
            to: "/blog/list",
          },
          {
            icon: "mdi-pencil",
            title: "Post",
            to: "/blog/post",
          },
          {
            icon: "mdi-dresser",
            title: "dashboard",
            to: "/blog/dashboard",
          },
        ],
      };
    },
};
</script>