<template>
  <div v-if="isOpen" class="wallet-dialog-overlay" @click="closeDialog">
    <div class="wallet-dialog" @click.stop>
      <div class="wallet-dialog-header">
        <h3>Wallet Connection</h3>
        <button class="close-button" @click="closeDialog">
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <line x1="18" y1="6" x2="6" y2="18"></line>
            <line x1="6" y1="6" x2="18" y2="18"></line>
          </svg>
        </button>
      </div>
      
      <div class="wallet-dialog-content">
        <div v-if="walletAddress" class="connected-wallet">
          <div class="wallet-info">
            <span class="wallet-icon">
              <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M21 12V7H5a2 2 0 0 0 0 4h14v1"></path>
                <path d="M3 5v14a2 2 0 0 0 2 2h16v-5"></path>
                <path d="M18 12a2 2 0 0 0 0 4h4v-4Z"></path>
              </svg>
            </span>
            <div class="address-info">
              <p>Connected Wallet</p>
              <span class="wallet-address">{{ shortenAddress(walletAddress) }}</span>
            </div>
          </div>
          <button class="disconnect-button" @click="disconnectWallet">
            Disconnect
          </button>
        </div>
        
        <div v-else class="connect-options">
          <button class="connect-button" @click="connectWallet('phantom')">
            <span class="wallet-icon">👻</span>
            Phantom Wallet
          </button>
          <button class="connect-button solflare" @click="connectWallet('solflare')">
            <span class="wallet-icon">⚡</span>
            Solflare Wallet
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { PhantomWalletAdapter } from '@solana/wallet-adapter-phantom';
import { SolflareWalletAdapter } from '@solana/wallet-adapter-solflare';
import Cookies from 'js-cookie';
import { useWalletStore } from '@/stores/walletStore';
import { useGenerationStore } from '@/stores/generationStore';

export default {
  name: 'WalletDialog',
  props: {
    isOpen: {
      type: Boolean,
      required: true
    },
    walletAddress: {
      type: String,
      default: null
    }
  },
  emits: ['update:isOpen', 'update:walletAddress'],
  setup(props, { emit }) {
    const walletStore = useWalletStore();
    const generationStore = useGenerationStore();

    const onWalletConnected = async (address) => {
      walletStore.setWalletAddress(address);
      if (address) {
        await generationStore.checkGenerationLimit(address);
      }
    };

    const checkWalletConnection = async () => {
      try {
        const savedAddress = Cookies.get('wallet_address');
        const savedWalletType = Cookies.get('wallet_type');
        
        if (savedAddress && savedWalletType) {
          let isConnected = false;
          
          if (savedWalletType === 'phantom' && window.solana && window.solana.isPhantom) {
            const phantom = new PhantomWalletAdapter();
            isConnected = await phantom.connected;
          } else if (savedWalletType === 'solflare' && window.solflare) {
            const solflare = new SolflareWalletAdapter();
            isConnected = await solflare.connected;
          }
          
          if (isConnected) {
            walletStore.setWalletType(savedWalletType);
            emit('update:walletAddress', savedAddress);
            await onWalletConnected(savedAddress);
          } else {
            Cookies.remove('wallet_address');
            Cookies.remove('wallet_type');
            walletStore.clearWallet();
            emit('update:walletAddress', null);
            await onWalletConnected(null);
          }
        }
      } catch (error) {
        console.error('Error checking wallet connection:', error);
        Cookies.remove('wallet_address');
        Cookies.remove('wallet_type');
        walletStore.clearWallet();
        emit('update:walletAddress', null);
        await onWalletConnected(null);
      }
    };

    const connectWallet = async (walletType) => {
      try {
        const isMobile = /iPhone|iPad|iPod|Android/i.test(navigator.userAgent);

        if (isMobile) {
          const deepLink = walletType === 'phantom'
            ? 'https://phantom.app/ul/browse/https://brainrotlab.io'
            : 'https://solflare.com/ul/browse/https://brainrotlab.io';
          window.location.href = deepLink;
          return;
        }

        if (walletType === 'phantom') {
          const provider = window.solana;

          if (!provider?.isPhantom) {
            window.open('https://phantom.app/', '_blank');
            return;
          }

          try {
            const response = await provider.connect();

            if (!response?.publicKey) {
              throw new Error('No public key returned');
            }

            const message = new TextEncoder().encode("Verify ownership");
            const signed = await provider.signMessage(message, "utf8");

            if (!signed || !signed.signature) {
              throw new Error("User did not sign message — wallet probably locked");
            }

            const address = response.publicKey.toString();
            Cookies.set('wallet_address', address);
            Cookies.set('wallet_type', walletType);
            walletStore.setWalletType(walletType);
            emit('update:walletAddress', address);
            emit('update:isOpen', false);
            await onWalletConnected(address);

          } catch (err) {
            console.error("Phantom connection failed:", err);
            Cookies.remove('wallet_address');
            Cookies.remove('wallet_type');
            walletStore.clearWallet();
            emit('update:walletAddress', null);
            await onWalletConnected(null);
          }
        } else if (walletType === 'solflare') {
          if (!window.solflare) {
            window.open('https://solflare.com/', '_blank');
            return;
          }

          const wallet = new SolflareWalletAdapter();
          await wallet.connect();

          const address = wallet.publicKey.toString();
          Cookies.set('wallet_address', address);
          Cookies.set('wallet_type', walletType);
          walletStore.setWalletType(walletType);
          emit('update:walletAddress', address);
          await onWalletConnected(address);
          emit('update:isOpen', false);
        }
      } catch (error) {
        console.error('Error connecting wallet:', error);
        Cookies.remove('wallet_address');
        Cookies.remove('wallet_type');
        walletStore.clearWallet();
        emit('update:walletAddress', null);
        await onWalletConnected(null);
      }
    };

    const disconnectWallet = async () => {
      try {
        const walletType = Cookies.get('wallet_type');
        let wallet;
        
        if (walletType === 'phantom') {
          wallet = new PhantomWalletAdapter();
        } else if (walletType === 'solflare') {
          wallet = new SolflareWalletAdapter();
        }
        
        if (wallet) {
          await wallet.disconnect();
        }
        
        Cookies.remove('wallet_address');
        Cookies.remove('wallet_type');
        walletStore.clearWallet();
        emit('update:walletAddress', null);
        await onWalletConnected(null);
      } catch (error) {
        console.error('Error disconnecting wallet:', error);
      }
    };

    const closeDialog = () => {
      emit('update:isOpen', false);
    };

    const shortenAddress = (address) => {
      if (!address) return '';
      return `${address.slice(0, 4)}...${address.slice(-4)}`;
    };

    // Check connection when component initializes
    checkWalletConnection();

    return {
      connectWallet,
      disconnectWallet,
      closeDialog,
      shortenAddress,
      generationStore
    };
  }
};
</script>

<style scoped>
.wallet-dialog-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.7);
  backdrop-filter: blur(5px);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.wallet-dialog {
  background: rgba(19, 17, 26, 0.95);
  border: 1px solid rgba(0, 255, 102, 0.2);
  border-radius: 16px;
  padding: 1.5rem;
  width: 100%;
  max-width: 400px;
  box-shadow: 
    0 0 30px rgba(0, 255, 102, 0.2),
    0 0 20px rgba(0, 204, 85, 0.1);
  position: relative;
  overflow: hidden;
}

.wallet-dialog::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: 
    radial-gradient(circle at 20% 20%, rgba(0, 255, 102, 0.15) 0%, transparent 40%),
    radial-gradient(circle at 80% 80%, rgba(0, 204, 85, 0.15) 0%, transparent 40%);
  z-index: 0;
  pointer-events: none;
}

.wallet-dialog-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
  position: relative;
  z-index: 1;
}

.wallet-dialog-header h3 {
  color: #ffffff;
  margin: 0;
  font-size: 1.5rem;
  text-shadow: 0 0 10px rgba(0, 255, 102, 0.5);
}

.close-button {
  background: none;
  border: none;
  color: rgba(255, 255, 255, 0.6);
  cursor: pointer;
  padding: 0.5rem;
  transition: all 0.3s ease;
}

.close-button:hover {
  color: #ffffff;
  transform: rotate(90deg);
}

.wallet-dialog-content {
  position: relative;
  z-index: 1;
}

.connected-wallet {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.wallet-info {
  display: flex;
  align-items: center;
  gap: 1rem;
  background: rgba(0, 255, 102, 0.1);
  padding: 1rem;
  border-radius: 12px;
  border: 1px solid rgba(0, 255, 102, 0.2);
}

.wallet-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
  font-size: 24px;
  filter: drop-shadow(0 0 5px rgba(123, 97, 255, 0.5));
}

.address-info {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.address-info p {
  color: rgba(255, 255, 255, 0.8);
  margin: 0;
  font-size: 0.9rem;
}

.wallet-address {
  color: #ffffff;
  font-family: monospace;
  font-size: 1rem;
  text-shadow: 0 0 5px rgba(0, 255, 102, 0.3);
}

.disconnect-button {
  background: rgba(255, 0, 0, 0.2);
  border: 1px solid rgba(255, 0, 0, 0.5);
  color: #ff4444;
  padding: 0.75rem;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s ease;
  font-weight: 600;
}

.disconnect-button:hover {
  background: rgba(255, 0, 0, 0.3);
  box-shadow: 0 0 15px rgba(255, 0, 0, 0.3);
}

.connect-options {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.connect-button {
  display: flex;
  align-items: center;
  gap: 1rem;
  background: rgba(123, 97, 255, 0.1);
  border: 1px solid rgba(123, 97, 255, 0.3);
  color: #7b61ff;
  padding: 1rem;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s ease;
  font-weight: 600;
  width: 100%;
}

.connect-button:hover {
  background: rgba(123, 97, 255, 0.2);
  box-shadow: 0 0 15px rgba(123, 97, 255, 0.3);
}

.connect-button.solflare {
  background: rgba(255, 204, 0, 0.1);
  border: 1px solid rgba(255, 204, 0, 0.3);
  color: #ffcc00;
}

.connect-button.solflare:hover {
  background: rgba(255, 204, 0, 0.2);
  box-shadow: 0 0 15px rgba(255, 204, 0, 0.3);
}

.connect-button.solflare .wallet-icon {
  filter: drop-shadow(0 0 5px rgba(255, 204, 0, 0.5));
}

@media (max-width: 480px) {
  .wallet-dialog {
    margin: 1rem;
    padding: 1.5rem;
    border-radius: 16px;
    min-height: auto;
    max-width: 90%;
    max-height: 90vh;
    overflow-y: auto;
  }
  
  .wallet-dialog-header {
    margin-bottom: 1.5rem;
  }
  
  .wallet-dialog-header h3 {
    font-size: 1.25rem;
  }
  
  .wallet-info {
    padding: 1rem;
    flex-direction: row;
    align-items: center;
    gap: 1rem;
  }
  
  .wallet-icon {
    width: 32px;
    height: 32px;
    font-size: 20px;
  }
  
  .wallet-address {
    font-size: 0.9rem;
    word-break: break-all;
  }

  .connect-button,
  .disconnect-button {
    width: 100%;
    padding: 0.75rem;
    font-size: 0.9rem;
  }

  .close-button {
    padding: 0.5rem;
  }
}
</style> 