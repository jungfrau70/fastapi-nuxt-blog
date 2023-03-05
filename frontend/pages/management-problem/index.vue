<template>
  <v-app>
    <v-card>
      <v-tabs>
        <v-tab to="/management-problem/list">리스트</v-tab>
        <v-tab to="/management-problem/graph">그래프</v-tab>
        <v-tab to="/management-problem/dashboard">대시보드</v-tab>
        <v-tab to="/management-problem/analyzer">분석기</v-tab>
      </v-tabs>
      <nuxt-child />
    </v-card>
  </v-app>
</template>
