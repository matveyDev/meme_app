import { defineStore } from 'pinia';
import { ref, computed } from 'vue';

export const useWalletStore = defineStore('wallet', () => {
  const walletAddress = ref(null);
  const walletType = ref(null); // 'phantom' or 'solflare'

  const isConnected = computed(() => !!walletAddress.value);

  function setWalletAddress(address) {
    walletAddress.value = address;
  }

  function setWalletType(type) {
    walletType.value = type;
  }

  function clearWallet() {
    walletAddress.value = null;
    walletType.value = null;
  }

  return {
    walletAddress,
    walletType,
    isConnected,
    setWalletAddress,
    setWalletType,
    clearWallet,
  };
});
