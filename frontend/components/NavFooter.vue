<template>
  <v-footer padless>
    <v-row justify="center" no-gutters>
      <template>
        <v-btn 
              v-for="(item, i) in items"
              :key="i"
              :to="item.to"
              router
              exact
              color="white" text rounded class="my-1"

            >
              <v-list-item-action>
                <v-icon>{{ item.icon }}</v-icon>
              </v-list-item-action>
              <!-- <v-list-item-content>
                <v-list-item-title ma-0 pa-0 auto>{{
                  item.title
                }}</v-list-item-title>
              </v-list-item-content> -->
        </v-btn>
      </template></v-row
    ></v-footer
  >
</template>

<script>
export default {
  data() {
    return {
      items: [
        {
          icon: 'mdi-apps',
          title: 'Home',
          to: '/',
        },
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
    }
  },
}
</script>