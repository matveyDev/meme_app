<template>
  <v-app>
    <app-header class="app-header" />
    <v-main>
      <v-container fluid class="pa-0">
        <router-view></router-view>
      </v-container>
    </v-main>
  </v-app>
</template>

<script>
import AppHeader from '@/components/AppHeader.vue'

export default {
  name: 'App',
  components: {
    AppHeader
  }
}
</script>

<style>
.v-application {
  background: #121212;
  color: white;
}

.v-main {
  padding-top: 0 !important;
}

.app-header {
  width: 100%;
  z-index: 100;
}

.main-container {
  padding-top: 120px !important;
}

@media (max-width: 768px) {
  .main-container {
    padding-top: 160px !important;
  }
}
</style> 