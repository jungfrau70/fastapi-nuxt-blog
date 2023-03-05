<template>
  <v-app>
    <KubernetesList />
  </v-app>
</template>

<script>
import KubernetesList from '../../components/KubernetesList.vue'
export default {
  components: {
    KubernetesList,
  },
}
</script>
