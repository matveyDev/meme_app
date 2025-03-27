<template>
  <div>
    <v-btn
      :color="isConnected ? 'success' : '#8B5CF6'"
      class="wallet-connect-btn"
      elevation="2"
      @click="toggleWallet"
    >
      <v-icon start class="mr-2">{{ isConnected ? 'mdi-wallet' : 'mdi-wallet-outline' }}</v-icon>
      <span v-if="isConnected" class="wallet-address">{{ truncatedAddress }}</span>
      <span v-else>Connect</span>
    </v-btn>

    <v-dialog v-model="showDialog" max-width="400">
      <v-card class="wallet-dialog">
        <v-card-title class="gradient-text">Select Wallet</v-card-title>
        <v-card-text>
          <v-list class="wallet-list">
            <v-list-item
              v-for="wallet in availableWallets"
              :key="wallet.name"
              @click="connectWallet(wallet)"
              class="wallet-item"
            >
              <v-list-item-title class="d-flex align-center">
                <img :src="wallet.imageUrl" :alt="wallet.name" class="wallet-icon mr-3">
                {{ wallet.name }}
              </v-list-item-title>
            </v-list-item>
          </v-list>
        </v-card-text>
      </v-card>
    </v-dialog>
  </div>
</template>

<script>
export default {
  name: 'TonWallet',
  data() {
    return {
      isConnected: false,
      showDialog: false,
      walletAddress: '',
      availableWallets: [
        {
          name: 'Tonkeeper',
          imageUrl: 'https://tonkeeper.com/assets/tonkeeper-logo.png',
          url: 'https://app.tonkeeper.com/ton-connect'
        },
        {
          name: 'OpenMask',
          imageUrl: 'https://raw.githubusercontent.com/OpenProduct/openmask-extension/main/public/openmask-logo-128.png',
          url: 'https://openmask.app/'
        }
      ]
    }
  },
  computed: {
    truncatedAddress() {
      if (!this.walletAddress) return ''
      return this.walletAddress.slice(0, 6) + '...' + this.walletAddress.slice(-4)
    }
  },
  created() {
    // Проверяем сохраненное состояние при загрузке
    const savedState = localStorage.getItem('walletState')
    if (savedState) {
      const { isConnected, address } = JSON.parse(savedState)
      this.isConnected = isConnected
      this.walletAddress = address
    }
  },
  methods: {
    toggleWallet() {
      if (this.isConnected) {
        this.disconnectWallet()
      } else {
        this.showDialog = true
      }
    },
    connectWallet(wallet) {
      // Симулируем подключение кошелька (в реальном приложении здесь будет логика TON Connect)
      this.isConnected = true
      this.walletAddress = '0x' + Math.random().toString(16).slice(2, 12)
      this.showDialog = false
      
      // Сохраняем состояние в localStorage
      localStorage.setItem('walletState', JSON.stringify({
        isConnected: true,
        address: this.walletAddress
      }))
      
      this.$emit('wallet-connected', this.walletAddress)
      window.open(wallet.url, '_blank')
    },
    disconnectWallet() {
      this.isConnected = false
      this.walletAddress = ''
      
      // Очищаем сохраненное состояние
      localStorage.removeItem('walletState')
      this.$emit('wallet-disconnected')
    }
  }
}
</script>

<style scoped>
.wallet-connect-btn {
  border-radius: 12px !important;
  font-weight: 600 !important;
  text-transform: none !important;
  letter-spacing: 0.5px !important;
  height: 40px !important;
  padding: 0 16px !important;
  background: linear-gradient(135deg, rgba(139, 92, 246, 0.1) 0%, rgba(109, 40, 217, 0.1) 100%) !important;
  border: 1px solid rgba(139, 92, 246, 0.3) !important;
  backdrop-filter: blur(10px) !important;
  color: white !important;
}

.wallet-connect-btn:hover {
  background: linear-gradient(135deg, rgba(139, 92, 246, 0.2) 0%, rgba(109, 40, 217, 0.2) 100%) !important;
  border-color: rgba(139, 92, 246, 0.5) !important;
}

.wallet-address {
  max-width: 120px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.wallet-dialog {
  background: rgba(19, 17, 26, 0.95) !important;
  border: 1px solid rgba(139, 92, 246, 0.2) !important;
  backdrop-filter: blur(10px);
  color: white !important;
}

.wallet-list {
  background: transparent !important;
  padding: 8px !important;
  color: white !important;
}

.wallet-item {
  border-radius: 12px !important;
  margin-bottom: 8px !important;
  background: rgba(30, 27, 36, 0.8) !important;
  border: 1px solid rgba(139, 92, 246, 0.2) !important;
  transition: all 0.3s ease !important;
  color: white !important;
}

.wallet-item:hover {
  background: rgba(139, 92, 246, 0.1) !important;
  border-color: rgba(139, 92, 246, 0.4) !important;
}

.wallet-icon {
  width: 24px;
  height: 24px;
  object-fit: contain;
}

.gradient-text {
  background: linear-gradient(135deg, #8B5CF6 0%, #6D28D9 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  font-weight: 700;
}
</style> 