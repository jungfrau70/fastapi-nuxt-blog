<template>
  <v-app dark>
    <div v-if="$auth.loggedIn">
      <v-navigation-drawer
        v-model="drawer"
        :mini-variant="miniVariant"
        :clipped="clipped"
        fixed
        app
      >
        <v-list>
          <v-list-item
            v-for="(item, i) in items"
            :key="i"
            :to="item.to"
            router
            exact
          >
            <v-list-item-action>
              <!-- <v-icon>{{ item.icon }}</v-icon> -->
              <v-icon>{{ item.icon || item.title.charAt(0) }}</v-icon>
            </v-list-item-action>
            <v-list-item-content>
              <v-list-item-title ma-0 pa-0 auto>{{
                item.title
              }}</v-list-item-title>
            </v-list-item-content>
          </v-list-item>
        </v-list>
      </v-navigation-drawer>
    </div>
    <v-app-bar :clipped-left="clipped" fixed app>
      <!-- <v-toolbar-title>{{ title }}</v-toolbar-title>     -->
      <v-app-bar-nav-icon @click.stop="drawer = !drawer" />        
      <!-- <v-spacer /> -->
      <v-spacer></v-spacer>

      <div v-if="$auth.loggedIn">
        <v-btn icon to="/blog/list/">
          <v-icon>mdi-note</v-icon>
        </v-btn>

        <v-btn icon to="/blog/post/">
          <v-icon>mdi-pencil</v-icon>
        </v-btn>

        <v-btn icon to="/blog/dashboard">
          <v-icon>mdi-dresser</v-icon>
        </v-btn>
      </div>
      <v-spacer></v-spacer>

      <div v-if="$auth.loggedIn">
  
        {{ $auth.user.email }}
        <v-btn text @click="$auth.logout()">Logout</v-btn>
        <v-btn text to="/user/profile">Profile</v-btn>
      </div>
      <div v-else>
        <!-- <v-toolbar-title>{{ title }}</v-toolbar-title> -->   
        <v-spacer />        
        <v-btn text to="/user/login">Login</v-btn>
        <v-btn text to="/user/signup">SignUp</v-btn>
      </div>
    </v-app-bar>

    <v-main>
      <v-container>
        <Nuxt />
        <!-- <nav-footer />         -->
      </v-container>
    </v-main>

    <v-navigation-drawer v-model="rightDrawer" :right="right" temporary fixed>
      <v-list>
        <v-list-item @click.native="right = !right">
          <v-list-item-action>
            <v-icon light> mdi-repeat </v-icon>
          </v-list-item-action>
          <v-list-item-title>Switch drawer (click me)</v-list-item-title>
        </v-list-item>
      </v-list>
    </v-navigation-drawer>
    <!-- <v-footer :absolute="!fixed" app>
      <span>&copy; {{ new Date().getFullYear() }}</span>
    </v-footer> -->
  </v-app>
</template>

<script>
// import NavFooter from './NavFooter.vue'

export default {
  components: {
    // NavFooter,
  },
  data() {
    return {
      clipped: false,
      drawer: false,
      fixed: false,
      items: [
        // {
        //   icon: 'mdi-apps',
        //   title: 'Home',
        //   to: '/',
        // },
        {
          icon: 'mdi-account-multiple',
          title: 'Discussion(Summary)',
          to: '/discussion/list',
        },
        {
          icon: 'mdi-alert-octagon',
          title: 'Incident Handling',
          to: '/management-incident/list',
        },
        {
          icon: 'mdi-alert-outline',
          title: 'Issue',
          to: '/management-issue/list',
        },
        {
          icon: 'mdi-ambulance',
          title: 'Problem',
          to: '/management-problem/list',
        },
        {
          icon: 'mdi-key-change',
          title: 'Change',
          to: '/management-change/list',
        },
        {
          icon: 'mdi-import',
          title: 'Request',
          to: '/management-request/list',
        },
        {
          icon: 'mdi-magnify-plus',
          title: 'Capacity',
          to: '/management-capacity/list',
        },
        {
          icon: 'mdi-content-save-all',
          title: 'Backup',
          to: '/management-backup/list',
        },
        {
          icon: 'mdi-numeric-1-box-multiple-outline',
          title: 'Instance',
          to: '/inventory-instance/list',
        },
        {
          icon: 'mdi-numeric-2-box-multiple-outline',
          title: 'Kubernetes',
          to: '/inventory-kubernetes/list',
        },
        {
          icon: 'mdi-numeric-3-box-multiple-outline',
          title: 'Database',
          to: '/inventory-database/list',
        },
        {
          icon: 'mdi-numeric-4-box-multiple-outline',
          title: 'License',
          to: '/inventory-license/list',
        },
        {
          icon: 'mdi-lock-plus',
          title: 'Vulnerability(Security)',
          to: '/vulnerability/list',
        },
        {
          icon: 'mdi-wrench',
          title: 'Preventive(PM)',
          to: '/preventive/list',
        },
      ],
      miniVariant: false,
      right: true,
      rightDrawer: false,
      title: 'Lenz Portal',
    }
  },
  computed: {
    isLoggedIn: function () {
      // return this.$store.getters.isAuthenticated
      return null
    },
  },
  methods: {
    async logout() {
      await this.$store.dispatch('logOut')
      this.$router.push('/user/login')
    },
  },
}
</script>
