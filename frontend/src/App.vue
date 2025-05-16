<template>
  <v-app>
    <div class="app">
      <AppHeader 
        :wallet-address="walletAddress"
        @open-wallet-dialog="openWalletDialog" 
      />
      <v-main class="main-content">
        <div class="content-wrapper">
          <router-view />
        </div>
      </v-main>
      <AppFooter />
      <WalletDialog
        v-model:isOpen="isWalletDialogOpen"
        v-model:walletAddress="walletAddress"
      />
    </div>
  </v-app>
</template>

<script>
import { ref } from 'vue';
import AppHeader from './components/AppHeader.vue';
import AppFooter from './components/Footer.vue';
import WalletDialog from './components/WalletDialog.vue';

export default {
  name: 'App',
  components: {
    AppHeader,
    AppFooter,
    WalletDialog
  },
  setup() {
    const isWalletDialogOpen = ref(false);
    const walletAddress = ref(null);

    const openWalletDialog = () => {
      isWalletDialogOpen.value = true;
    };

    return {
      isWalletDialogOpen,
      walletAddress,
      openWalletDialog
    };
  }
};
</script>

<style>
.app {
  min-height: 100vh;
  background-image: linear-gradient(rgba(0, 0, 0, 0.048), rgba(0, 0, 0, 0.425)), url('@/assets/background.webp');
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
  color: white;
  display: flex;
  flex-direction: column;
}

.v-application {
  background: transparent !important;
}

.main-content {
  flex: 1 0 auto;
  padding-top: 0 !important;
  display: flex;
  flex-direction: column;
}

.content-wrapper {
  flex: 1;
  display: flex;
  flex-direction: column;
  min-height: calc(100vh - 200px);
  /* padding: 20px; */
}

@media (max-width: 768px) {
  .app {
    min-height: 100vh;
  }
  
  .content-wrapper {
    min-height: calc(100vh - 240px);
    padding: 10px 0px;
  }
}
</style> 