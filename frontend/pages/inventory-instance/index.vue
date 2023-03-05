<template>
  <v-app>
    <v-card>
      <v-tabs>
        <v-tab to="/inventory-instance/list">리스트</v-tab>
        <v-tab to="/inventory-instance/graph">그래프</v-tab>
        <v-tab to="/inventory-instance/dashboard">대시보드</v-tab>
        <v-tab to="/inventory-instance/analyzer">분석기</v-tab>
      </v-tabs>
      <nuxt-child />
    </v-card>
  </v-app>
</template>
