<template>
  <v-app>
    <v-card>
      <v-tabs>
        <v-tab to="/preventive/list">리스트</v-tab>
        <v-tab to="/preventive/graph">그래프</v-tab>
        <v-tab to="/preventive/dashboard">대시보드</v-tab>
        <v-tab to="/preventive/analyzer">분석기</v-tab>
      </v-tabs>
      <nuxt-child />
    </v-card>
  </v-app>
</template>
