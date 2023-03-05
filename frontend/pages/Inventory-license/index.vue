<template>
  <v-app>
    <v-card>
      <v-tabs>
        <v-tab to="/inventory-license/list">리스트</v-tab>
        <v-tab to="/inventory-license/graph">그래프</v-tab>
        <v-tab to="/inventory-license/dashboard">대시보드</v-tab>
        <v-tab to="/inventory-license/analyzer">분석기</v-tab>
      </v-tabs>
      <nuxt-child />
    </v-card>
  </v-app>
</template>
