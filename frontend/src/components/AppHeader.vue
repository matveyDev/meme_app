<template>
  <div class="ln-header">
    <div class="ln-header-center">
      <div class="desktop-elements">
        <div class="token-info">
          <a aria-current="page" href="/" class="is-active is-exact-active ln-header-center-logo">
            <img class="img-responsive" src="https://media.istockphoto.com/id/1367033004/ru/%D0%B2%D0%B5%D0%BA%D1%82%D0%BE%D1%80%D0%BD%D0%B0%D1%8F/%D0%BC%D0%BE%D0%B7%D0%B3-%D0%BD%D0%B0%D1%80%D0%B8%D1%81%D0%BE%D0%B2%D0%B0%D0%BD-%D0%BE%D1%82-%D1%80%D1%83%D0%BA%D0%B8-2.jpg?s=612x612&w=0&k=20&c=dy2ZDIoa4vv4qvAFmt41C7XNJuQ09t63tI2pdQH4Vjo=" alt="Token">
          </a>
          <p>BrainRotCoin</p>
        </div>
      </div>
      <div class="mobile-elements">
        <div class="token-info">
          <a aria-current="page" href="/" class="is-active is-exact-active ln-header-center-logo">
            <img class="img-responsive" src="https://media.istockphoto.com/id/1367033004/ru/%D0%B2%D0%B5%D0%BA%D1%82%D0%BE%D1%80%D0%BD%D0%B0%D1%8F/%D0%BC%D0%BE%D0%B7%D0%B3-%D0%BD%D0%B0%D1%80%D0%B8%D1%81%D0%BE%D0%B2%D0%B0%D0%BD-%D0%BE%D1%82-%D1%80%D1%83%D0%BA%D0%B8-2.jpg?s=612x612&w=0&k=20&c=dy2ZDIoa4vv4qvAFmt41C7XNJuQ09t63tI2pdQH4Vjo=" alt="Token">
          </a>
          <p>BrainRotCoin</p>
        </div>
        <button class="connect-wallet-btn" @click="connectWallet">
          <span class="wallet-icon">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M21 12V7H5a2 2 0 0 0 0 4h14v1"></path>
              <path d="M3 5v14a2 2 0 0 0 2 2h16v-5"></path>
              <path d="M18 12a2 2 0 0 0 0 4h4v-4Z"></path>
            </svg>
          </span>
          <span class="wallet-text">{{ isConnected ? 'Connected' : 'Connect' }}</span>
        </button>
      </div>
      <div class="ln-header-contract" @click="copyAddress">
        <div class="ln-header-contract-address">
          <p>Contract Address</p>
          <span>{{ contractAddress }}</span>
        </div>
        <div class="icon">
          <svg v-if="!copied" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <rect x="2" y="2" width="20" height="20" rx="2.18" ry="2.18"></rect>
            <line x1="7" y1="2" x2="7" y2="22"></line>
            <line x1="17" y1="2" x2="17" y2="22"></line>
            <line x1="2" y1="12" x2="22" y2="12"></line>
            <line x1="2" y1="7" x2="7" y2="7"></line>
            <line x1="2" y1="17" x2="7" y2="17"></line>
            <line x1="17" y1="17" x2="22" y2="17"></line>
            <line x1="17" y1="7" x2="22" y2="7"></line>
          </svg>
          <svg v-else xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <polyline points="20 6 9 17 4 12"></polyline>
          </svg>
        </div>
      </div>
      <button class="connect-wallet-btn desktop-connect-btn" @click="connectWallet">
        <span class="wallet-icon">
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M21 12V7H5a2 2 0 0 0 0 4h14v1"></path>
            <path d="M3 5v14a2 2 0 0 0 2 2h16v-5"></path>
            <path d="M18 12a2 2 0 0 0 0 4h4v-4Z"></path>
          </svg>
        </span>
        <span class="wallet-text">{{ isConnected ? 'Connected' : 'Connect' }}</span>
      </button>
    </div>
  </div>
</template>

<script>
export default {
  name: 'AppHeader',
  data() {
    return {
      contractAddress: 'SOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOON',
      copied: false,
      isConnected: false
    }
  },
  methods: {
    async copyAddress() {
      try {
        await navigator.clipboard.writeText(this.contractAddress);
        this.copied = true;
        setTimeout(() => {
          this.copied = false;
        }, 2000);
      } catch (err) {
        console.error('Failed to copy text: ', err);
      }
    },
    async connectWallet() {
      try {
        if (window.ton) {
          const accounts = await window.ton.send('ton_requestAccounts');
          if (accounts && accounts.length > 0) {
            this.isConnected = true;
            this.$emit('wallet-connected', accounts[0]);
          }
        } else {
          alert('Please install Tonkeeper or another TON wallet');
        }
      } catch (error) {
        console.error('Failed to connect wallet:', error);
        alert('Failed to connect wallet. Please try again.');
      }
    }
  }
}
</script>

<style scoped>
.ln-header {
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 1rem 2rem;
  background: rgba(19, 17, 26, 0.4);
  border-bottom: 1px solid rgba(139, 92, 246, 0.1);
  backdrop-filter: blur(10px);
  width: 100%;
  max-width: 1200px;
  margin: 0 auto;
  height: auto;
  min-height: 80px;
  position: relative;
  overflow: hidden;
  box-shadow: 
    0 0 60px rgba(139, 92, 246, 0.2),
    0 0 40px rgba(109, 40, 217, 0.1),
    inset 0 0 20px rgba(139, 92, 246, 0.1);
}

.ln-header::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: 
    radial-gradient(circle at 20% 20%, rgba(139, 92, 246, 0.15) 0%, transparent 40%),
    radial-gradient(circle at 80% 80%, rgba(109, 40, 217, 0.15) 0%, transparent 40%);
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
}

.ln-header-center-logo img {
  width: 64px;
  height: 64px;
  filter: drop-shadow(0 0 10px rgba(139, 92, 246, 0.3));
  border-radius: 12px;
  object-fit: cover;
}

.ln-header-center p {
  color: white;
  margin: 0;
  font-weight: 600;
  font-size: 1.5rem;
  text-shadow: 0 0 10px rgba(139, 92, 246, 0.3);
}

.connect-wallet-btn {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  background: rgba(139, 92, 246, 0.2);
  border: 1px solid rgba(139, 92, 246, 0.3);
  border-radius: 8px;
  padding: 0.75rem 1.5rem;
  color: white;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.ln-header-contract {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  background: rgba(139, 92, 246, 0.1);
  padding: 0.5rem 1rem;
  border-radius: 8px;
  border: 1px solid rgba(139, 92, 246, 0.2);
  cursor: pointer;
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
  margin: 0 auto;
  white-space: nowrap;
}

.ln-header-contract:hover {
  background: rgba(139, 92, 246, 0.15);
  border-color: rgba(139, 92, 246, 0.3);
  transform: translateY(-1px);
}

.ln-header-contract:active {
  transform: translateY(0);
}

.ln-header-contract::after {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: radial-gradient(circle at center, rgba(139, 92, 246, 0.2) 0%, transparent 70%);
  opacity: 0;
  transition: opacity 0.3s ease;
}

.ln-header-contract:hover::after {
  opacity: 1;
}

.ln-header-contract-address {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
  white-space: nowrap;
}

.ln-header-contract-address p {
  color: rgba(255, 255, 255, 0.6);
  margin: 0;
  font-size: 0.875rem;
  white-space: nowrap;
}

.ln-header-contract-address span {
  color: white;
  font-family: monospace;
  font-size: 0.875rem;
  white-space: nowrap;
}

.ln-header-contract .icon {
  width: 20px;
  height: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: rgba(255, 255, 255, 0.6);
  transition: color 0.3s ease;
}

.ln-header-contract:hover .icon {
  color: rgba(255, 255, 255, 0.8);
}

@keyframes headerGlow {
  0% {
    opacity: 0.5;
    transform: scale(1);
  }
  50% {
    opacity: 0.8;
    transform: scale(1.05);
  }
  100% {
    opacity: 0.5;
    transform: scale(1);
  }
}

.wallet-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 28px;
  height: 28px;
}

.wallet-icon svg {
  width: 100%;
  height: 100%;
  stroke: currentColor;
}

.wallet-text {
  font-size: 1.1rem;
}

.mobile-elements {
  display: none;
}

.desktop-connect-btn {
  display: none;
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
    min-height: auto;
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
</style> 