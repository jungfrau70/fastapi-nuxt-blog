<template>
  <v-app>
    <v-card>
      <v-tabs>
        <v-tab to="/inventory-database/list">리스트</v-tab>
        <v-tab to="/inventory-database/graph">그래프</v-tab>
        <v-tab to="/inventory-database/dashboard">대시보드</v-tab>
        <v-tab to="/inventory-database/analyzer">분석기</v-tab>
      </v-tabs>
      <nuxt-child />
    </v-card>
    <v-card>
      <!-- HERE -->
      <iframe
        ref="formFrame"
        :src="url"
        width="100%"
        height="500"
        @load="afterLoad()"
      ></iframe>
      =
    </v-card>
  </v-app>
</template>


<script>
export default {
  data() {
    return {
      url: 'https://jupyterlite.github.io/demo/repl/index.html?kernel=python',
      editBoardDialog: '',
      title: 'JupyterLab',
    }
  },
  methods: {
    afterLoad() {
      // passing data to iframe
      window.onmessage = function (e) {
        // inside the iframe
        if (e.data === 'hello world') {
          alert('It works!')
        }
      }
    },
  },
}
</script>
