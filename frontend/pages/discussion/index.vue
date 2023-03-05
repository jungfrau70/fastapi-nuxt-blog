<template>
  <v-app height="100%">
    <v-card class="flexcard" height="100%">
      <v-tabs>
        <v-tab to="/discussion/list">리스트</v-tab>
        <v-tab to="/discussion/graph">그래프</v-tab>
        <v-tab to="/discussion/dashboard">대시보드</v-tab>
        <v-tab to="/discussion/analyzer">분석기</v-tab>
      </v-tabs>
      <nuxt-child height="100%"></nuxt-child>
    </v-card>
  </v-app>
</template>
