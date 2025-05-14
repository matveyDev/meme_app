<template>
  <div class="ln-header">
    <div class="ln-header-center">
      <div class="desktop-elements">
        <div class="token-info">
          <a aria-current="page" href="/" class="is-active is-exact-active ln-header-center-logo">
            <img class="img-responsive" src="@/assets/coin.jpg" alt="Token">
          </a>
          <p>BrainRotCoin</p>
        </div>
      </div>
      <div class="mobile-elements">
        <div class="token-info">
          <a aria-current="page" href="/" class="is-active is-exact-active ln-header-center-logo">
            <img class="img-responsive" src="@/assets/coin.jpg" alt="Token">
          </a>
          <p>BrainRotCoin</p>
        </div>
        <button class="connect-wallet-btn" @click="openWalletDialog">
          <span class="wallet-icon">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M21 12V7H5a2 2 0 0 0 0 4h14v1"></path>
              <path d="M3 5v14a2 2 0 0 0 2 2h16v-5"></path>
              <path d="M18 12a2 2 0 0 0 0 4h4v-4Z"></path>
            </svg>
          </span>
          <span class="wallet-text">{{ walletAddress ? shortenAddress(walletAddress) : 'Connect' }}</span>
        </button>
      </div>
      <div class="ln-header-contract" @click="copyContractAddress">
        <div class="ln-header-contract-address">
          <p>Contract Address</p>
          <span>{{ contractAddress }}</span>
        </div>
        <div class="icon" :data-copied="isCopied">
          <svg v-if="!isCopied" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <rect x="2" y="2" width="20" height="20" rx="2.18" ry="2.18"></rect>
            <line x1="7" y1="2" x2="7" y2="22"></line>
            <line x1="17" y1="2" x2="17" y2="22"></line>
            <line x1="2" y1="12" x2="22" y2="12"></line>
            <line x1="2" y1="7" x2="7" y2="7"></line>
            <line x1="2" y1="17" x2="7" y2="17"></line>
            <line x1="17" y1="17" x2="22" y2="17"></line>
            <line x1="17" y1="7" x2="22" y2="7"></line>
          </svg>
          <svg v-else xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round">
            <polyline points="20 6 9 17 4 12"></polyline>
          </svg>
        </div>
      </div>
      <button class="connect-wallet-btn desktop-connect-btn" @click="openWalletDialog">
        <span class="wallet-icon">
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M21 12V7H5a2 2 0 0 0 0 4h14v1"></path>
            <path d="M3 5v14a2 2 0 0 0 2 2h16v-5"></path>
            <path d="M18 12a2 2 0 0 0 0 4h4v-4Z"></path>
          </svg>
        </span>
        <span class="wallet-text">{{ walletAddress ? shortenAddress(walletAddress) : 'Connect' }}</span>
      </button>
    </div>
  </div>
</template>

<script>
import { ref, onUnmounted } from 'vue';

export default {
  name: 'AppHeader',
  props: {
    walletAddress: {
      type: String,
      default: null
    }
  },
  emits: ['open-wallet-dialog'],
  setup(props, { emit }) {
    const isCopied = ref(false);
    const copyTimeout = ref(null);
    const contractAddress = ref('SOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOON');

    const openWalletDialog = () => {
      emit('open-wallet-dialog');
    };

    const shortenAddress = (address) => {
      if (!address) return '';
      return `${address.slice(0, 4)}...${address.slice(-4)}`;
    };

    const copyContractAddress = async () => {
      try {
        if (!navigator.clipboard) {
          throw new Error('Clipboard API not available in this browser or context');
        }
        await navigator.clipboard.writeText(contractAddress.value);
        
        isCopied.value = true;
        
        if (copyTimeout.value) {
          clearTimeout(copyTimeout.value);
        }
        
        copyTimeout.value = setTimeout(() => {
          isCopied.value = false;
        }, 2000);
      } catch (error) {
        console.error('Failed to copy contract address:', error);
        // Fallback method for copying text
        try {
          const textArea = document.createElement('textarea');
          textArea.value = contractAddress.value;
          textArea.style.position = 'fixed';
          textArea.style.left = '-999999px';
          textArea.style.top = '-999999px';
          document.body.appendChild(textArea);
          textArea.focus();
          textArea.select();
          const successful = document.execCommand('copy');
          if (successful) {
            isCopied.value = true;
            if (copyTimeout.value) {
              clearTimeout(copyTimeout.value);
            }
            copyTimeout.value = setTimeout(() => {
              isCopied.value = false;
            }, 2000);
          }
          document.body.removeChild(textArea);
        } catch (fallbackError) {
          console.error('Fallback copy method also failed:', fallbackError);
        }
      }
    };

    onUnmounted(() => {
      if (copyTimeout.value) {
        clearTimeout(copyTimeout.value);
      }
    });

    return {
      openWalletDialog,
      shortenAddress,
      copyContractAddress,
      isCopied,
      contractAddress
    };
  }
};
</script>

<style scoped>
.ln-header {
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 1rem 2rem;
  background: rgba(19, 17, 26, 0.4);
  border-bottom: 1px solid rgba(0, 255, 102, 0.1);
  backdrop-filter: blur(10px);
  width: 100%;
  max-width: 1200px;
  margin: 0 auto;
  height: auto;
  min-height: 80px;
  position: relative;
  overflow: hidden;
  box-shadow: 
    0 0 60px rgba(0, 255, 102, 0.2),
    0 0 40px rgba(0, 204, 85, 0.1),
    inset 0 0 20px rgba(0, 255, 102, 0.1);
}

.ln-header::before {
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
  animation: headerGlow 8s ease-in-out infinite;
}

.ln-header-center {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: space-between;
  gap: 2rem;
  position: relative;
  z-index: 1;
  width: 100%;
}

.desktop-elements {
  display: flex;
  align-items: center;
  gap: 2rem;
}

.token-info {
  display: flex;
  align-items: center;
  gap: 1rem;
  position: relative;
}

.ln-header-center-logo img {
  width: 64px;
  height: 64px;
  filter: drop-shadow(0 0 5px #00FF66) drop-shadow(0 0 10px rgba(0, 255, 102, 0.3));
  border-radius: 12px;
  object-fit: cover;
  animation: tokenGlow 2s ease-in-out infinite alternate;
  transition: all 0.3s ease;
}


@keyframes tokenGlow {
  from {
    filter: drop-shadow(0 0 2px #00FF66) drop-shadow(0 0 10px rgba(0, 255, 102, 0.3));
  }
  to {
    filter: drop-shadow(0 0 10px #00FF66) drop-shadow(0 0 15px rgba(0, 255, 102, 0.4));
  }
}

.ln-header-center p {
  color: #ffffff;
  margin: 0;
  font-weight: 600;
  font-size: 1.5rem;
  text-shadow: 0 0 10px #00FF66, 0 0 20px rgba(0, 255, 102, 0.5);
}

.connect-wallet-btn {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  background: rgba(0, 255, 102, 0.2);
  border: 2px solid rgba(0, 255, 102, 0.5);
  border-radius: 8px;
  padding: 0.75rem 1.5rem;
  color: #ffffff;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
  box-shadow: 0 0 10px rgba(0, 255, 102, 0.2);
}

.connect-wallet-btn:hover {
  background: rgba(0, 255, 102, 0.3);
  border-color: rgba(0, 255, 102, 0.7);
  box-shadow: 0 0 15px rgba(0, 255, 102, 0.4);
  transform: translateY(-1px);
}

.connect-wallet-btn:active {
  transform: translateY(0);
  box-shadow: 0 0 8px rgba(0, 255, 102, 0.3);
}

.connect-wallet-btn::after {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: radial-gradient(circle at center, rgba(0, 255, 102, 0.3) 0%, transparent 70%);
  opacity: 0;
  transition: opacity 0.3s ease;
}

.connect-wallet-btn:hover::after {
  opacity: 0.5;
}

.wallet-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 28px;
  height: 28px;
  color: #00FF66;
  filter: drop-shadow(0 0 5px rgba(0, 255, 102, 0.5));
}

.wallet-icon svg {
  width: 100%;
  height: 100%;
  stroke: currentColor;
}

.wallet-text {
  font-size: 1.1rem;
  text-shadow: 0 0 5px rgba(0, 255, 102, 0.3);
}

.ln-header-contract {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  background: rgba(0, 255, 102, 0.1);
  padding: 0.5rem 1rem;
  border-radius: 8px;
  border: 1px solid rgba(0, 255, 102, 0.2);
  cursor: pointer;
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
  margin: 0 auto;
  white-space: nowrap;
}

.ln-header-contract:hover {
  background: rgba(0, 255, 102, 0.1);
  border-color: rgba(0, 255, 102, 0.5);
  box-shadow: 0 0 15px rgba(0, 255, 102, 0.3);
}

.ln-header-contract:active {
  transform: scale(0.98);
}

.ln-header-contract::after {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: radial-gradient(circle at center, rgba(0, 255, 102, 0.2) 0%, transparent 70%);
  opacity: 0;
  transition: opacity 0.3s ease;
}

.ln-header-contract:hover::after {
  opacity: 0.5;
}

.ln-header-contract-address {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
  white-space: nowrap;
}

.ln-header-contract-address p {
  color: #ffffff;
  margin: 0;
  font-size: 0.875rem;
  white-space: nowrap;
  text-shadow: 0 0 5px rgba(0, 255, 102, 0.3);
}

.ln-header-contract-address span {
  color: #ffffff;
  font-family: monospace;
  font-size: 0.875rem;
  white-space: nowrap;
  text-shadow: 0 0 5px rgba(0, 255, 102, 0.3);
}

.ln-header-contract .icon {
  width: 20px;
  height: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: rgba(255, 255, 255, 0.6);
  transition: all 0.3s ease;
}

.ln-header-contract:hover .icon {
  color: rgba(255, 255, 255, 0.8);
}

.ln-header-contract .icon svg {
  stroke: currentColor;
  transition: all 0.3s ease;
}

.ln-header-contract .icon[data-copied="true"] svg {
  stroke: #00FF66;
  stroke-width: 3;
  filter: drop-shadow(0 0 10px #00FF66) drop-shadow(0 0 20px rgba(0, 255, 102, 0.7));
  animation: checkmarkGlow 0.5s ease-in-out;
}

@keyframes checkmarkGlow {
  0% {
    filter: drop-shadow(0 0 0 #00FF66) drop-shadow(0 0 0 rgba(0, 255, 102, 0.7));
  }
  50% {
    filter: drop-shadow(0 0 15px #00FF66) drop-shadow(0 0 30px rgba(0, 255, 102, 0.9));
  }
  100% {
    filter: drop-shadow(0 0 10px #00FF66) drop-shadow(0 0 20px rgba(0, 255, 102, 0.7));
  }
}

@keyframes headerGlow {
  0% {
    opacity: 0.5;
  }
  50% {
    opacity: 1;
  }
  100% {
    opacity: 0.5;
  }
}

.mobile-elements {
  display: none;
}

.desktop-connect-btn {
  display: none;
}

@media (min-width: 769px) and (max-width: 863px) {
  .ln-header {
    width: 100%;
    padding: 1rem;
    border-radius: 0;
  }

  .ln-header-center {
    gap: 1rem;
  }

  .desktop-elements {
    gap: 1rem;
  }

  .ln-header-center-logo img {
    width: 48px;
    height: 48px;
  }

  .ln-header-center p {
    font-size: 1.2rem;
  }

  .connect-wallet-btn {
    padding: 0.5rem 1rem;
  }

  .wallet-text {
    font-size: 1rem;
  }

  .ln-header-contract {
    padding: 0.5rem 0.75rem;
  }

  .ln-header-contract-address p {
    font-size: 0.8rem;
  }

  .ln-header-contract-address span {
    font-size: 0.8rem;
  }
}

@media (min-width: 864px) and (max-width: 920px) {
  .ln-header {
    width: 100%;
    padding: 1.25rem;
    border-radius: 0;
  }

  .ln-header-center {
    gap: 1.5rem;
  }

  .desktop-elements {
    gap: 1.5rem;
  }

  .ln-header-center-logo img {
    width: 56px;
    height: 56px;
  }

  .ln-header-center p {
    font-size: 1.4rem;
  }

  .connect-wallet-btn {
    padding: 0.75rem 1.25rem;
  }

  .wallet-text {
    font-size: 1.1rem;
  }

  .ln-header-contract {
    padding: 0.75rem 1rem;
  }

  .ln-header-contract-address p {
    font-size: 0.9rem;
  }

  .ln-header-contract-address span {
    font-size: 0.9rem;
  }
}

@media (min-width: 769px) {
  .ln-header {
    width: fit-content;
    border-radius: 0 0 16px 16px;
  }

  .desktop-connect-btn {
    display: flex;
  }
}

@media (max-width: 768px) {
  .ln-header {
    padding: 1.25rem 0.75rem 0.75rem;
    min-height: 11rem;
    max-width: none;
  }

  .ln-header-center {
    flex-direction: column;
    gap: 0.5rem;
  }

  .desktop-elements {
    display: none;
  }

  .mobile-elements {
    display: flex;
    width: 100%;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 0.75rem;
  }

  .mobile-elements .token-info {
    display: flex;
    align-items: center;
    gap: 0.75rem;
  }

  .mobile-elements .connect-wallet-btn {
    display: flex;
    padding: 0.5rem 1rem;
  }

  .mobile-elements .ln-header-center-logo img {
    width: 56px;
    height: 56px;
    border-radius: 12px;
  }

  .mobile-elements p {
    font-size: 1.3rem;
    letter-spacing: -0.5px;
  }

  .mobile-elements .wallet-icon {
    width: 24px;
    height: 24px;
  }

  .mobile-elements .wallet-text {
    font-size: 1rem;
    font-weight: 500;
  }

  .ln-header-contract {
    width: 100%;
    justify-content: center;
    padding: 0.5rem 1rem;
  }

  .ln-header-contract-address p {
    font-size: 0.9rem;
  }

  .ln-header-contract-address span {
    font-size: 0.9rem;
  }

  .ln-header-contract .icon {
    width: 20px;
    height: 20px;
  }
}

.connect-button {
  background: rgba(0, 255, 0, 0.1);
  border: 1px solid rgba(0, 255, 0, 0.3);
  color: #00ff00;
  padding: 0.5rem 1rem;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.9rem;
}

.connect-button:hover {
  background: rgba(0, 255, 0, 0.2);
  box-shadow: 0 0 15px rgba(0, 255, 0, 0.3);
}

@media (max-width: 405px) {
  .connect-wallet-btn {
    padding: 0.5rem;
    width: 60px;
    height: 60px;
    justify-content: center;
  }

  .connect-wallet-btn .wallet-text {
    display: none;
  }

  .connect-wallet-btn .wallet-icon {
    width: 32px;
    height: 32px;
    margin: 0;
  }

  .ln-header-contract {
    padding: 0.4rem 0.6rem;
    gap: 0.3rem;
  }

  .ln-header-contract-address p {
    font-size: 0.75rem;
  }

  .ln-header-contract-address span {
    font-size: 0.9rem;
    letter-spacing: -0.5px;
  }

  .ln-header-contract .icon {
    display: none;
  }
}
</style> 