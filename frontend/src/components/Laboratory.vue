<template>
  <div>
    <div class="laboratory-content">
      <link href="https://fonts.googleapis.com/css2?family=Press+Start+2P&display=swap" rel="stylesheet">
      <h1 class="laboratory-title">Laboratory</h1>
      
      <!-- Refresh Button -->
      <v-btn
        icon
        @click="resetSelection"
        class="refresh-btn"
      >
        <v-icon>mdi-refresh</v-icon>
      </v-btn>

      <div class="selection-cards" v-if="!generatedMeme">
        <div class="selection-card" :class="{ selected: selectedAnimal }" @click="openAnimalModal">
          <template v-if="!selectedAnimal">
            <div class="card-icon">🦁</div>
            <h2 class="card-title">Animal</h2>
          </template>
          <template v-else>
            <div class="selected-full">
              <div class="selected-icon">{{ getAnimalIcon(selectedAnimal) }}</div>
              <div class="selected-name">{{ selectedAnimal }}</div>
            </div>
          </template>
        </div>
        <div class="selection-card" :class="{ selected: selectedObject }" @click="openObjectModal">
          <template v-if="!selectedObject">
            <div class="card-icon">🔮</div>
            <h2 class="card-title">Object</h2>
          </template>
          <template v-else>
            <div class="selected-full">
              <div class="selected-icon">{{ getObjectIcon(selectedObject) }}</div>
              <div class="selected-name">{{ selectedObject }}</div>
            </div>
          </template>
        </div>
      </div>

      <!-- Loading Animation -->
      <div class="loading-container" v-if="isLoading">
        <div class="test-tube">
          <!-- <div class="test-tube-neck"></div> -->
          <div class="test-tube-body">
            <div class="liquid" :style="{ height: loadingProgress + '%' }"></div>
          </div>
        </div>
        <div class="loading-text">Generating...</div>
      </div>

      <!-- Generated Meme Display -->
      <div class="generated-meme-container" v-if="generatedMeme">
        <div class="meme-wrapper">
          <img 
            :src="generatedMeme.imageUrl" 
            alt="Generated Meme" 
            class="generated-meme"
            @click="showMemeModal = true"
          >
          <div class="meme-actions">
            <div class="action-buttons-row">
              <button class="action-button save-button" @click="saveMeme">
                <span class="button-icon">💾</span>
                <span class="button-text">Save</span>
              </button>
              <button class="action-button share-button" @click="shareMeme">
                <span class="button-icon">📤</span>
                <span class="button-text">Share</span>
              </button>
            </div>
            <button class="action-button mint-button" disabled>
              <span class="button-icon">🖼️</span>
              <span class="button-text">Mint NFT (Soon)</span>
            </button>
          </div>
        </div>
      </div>

      <div class="absurd-checkbox" v-if="!generatedMeme && !isLoading">
        <label class="checkbox-label" :class="{ active: addAbsurdElement }" style="pointer-events: none; opacity: 0.5;">
          <div class="potion-icon">🧪</div>
          <span class="checkbox-text" :class="{ active: addAbsurdElement }">Add absurd element?</span>
        </label>
      </div>

      <div class="generate-button-container" v-if="!generatedMeme && !isLoading">
        <div class="button-wrapper">
          <p v-if="!isConnected" class="wallet-connect-text">Connect your wallet first</p>
          <p v-else-if="!canGenerate" class="wallet-connect-text">{{ generationMessage }}</p>
          <button 
            class="generate-button"
            :class="{ 
              loading: isLoading,
              'unlock-button': !canGenerate && isConnected,
              'disabled': !isConnected || (!canGenerate && !isConnected)
            }"
            :disabled="!isConnected || isLoading || isUnlocking"
            @click="canGenerate ? generateMeme() : handleUnlockMore()"
          >
            <span class="button-text">{{ canGenerate ? 'MAKE MEME' : 'UNLOCK MORE' }}</span>
            <span v-if="isLoading" class="loading-spinner">⌛</span>
          </button>
        </div>
      </div>

      <!-- Animal Selection Modal -->
      <div class="modal" v-if="showAnimalModal">
        <div class="modal-content">
          <div class="modal-header">
            <h2>Select Animal</h2>
            <button class="close-button" @click="closeAnimalModal">×</button>
          </div>
          <div class="modal-body">
            <div class="selection-grid">
              <div 
                v-for="animal in animals" 
                :key="animal"
                class="selection-item"
                @click="selectAnimal(animal)"
              >
                <div class="item-icon">{{ getAnimalIcon(animal) }}</div>
                <div class="item-name">{{ animal }}</div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Object Selection Modal -->
      <div class="modal" v-if="showObjectModal">
        <div class="modal-content">
          <div class="modal-header">
            <h2>Select Object</h2>
            <button class="close-button" @click="closeObjectModal">×</button>
          </div>
          <div class="modal-body">
            <div class="selection-grid">
              <div 
                v-for="object in objects" 
                :key="object"
                class="selection-item"
                @click="selectObject(object)"
              >
                <div class="item-icon">{{ getObjectIcon(object) }}</div>
                <div class="item-name">{{ object }}</div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Модальное окно для увеличенного просмотра - теперь вне контейнера -->
    <div class="meme-modal" v-if="showMemeModal" @click="showMemeModal = false">
      <img :src="generatedMeme.imageUrl" alt="Generated Meme">
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import Cookies from 'js-cookie';
import { useWalletStore } from '@/stores/walletStore';
import { useGenerationStore } from '@/stores/generationStore';
import { computed } from 'vue';
import { unlockMore } from '@/utils/payment';
import { API_URL } from '@/config';

export default {
  name: 'Laboratory',
  data() {
    return {
      selectedAnimal: null,
      selectedObject: null,
      addAbsurdElement: false,
      showAnimalModal: false,
      showObjectModal: false,
      showMemeModal: false,
      animals: [
        'Monkey',
        'Cat',
        'Crocodile',
        'Pigeon',
        'Beaver',
        'Shark',
        'Elephant',
        'Frog',
        'Cow',
        'Penguin',
        'Tiger',
        'Eagle',
        'Hamster',
        'Giraffe',
        'Goose'
      ],
      objects: [
        'Cannabis',
        'Cactus',
        'Pineapple',
        'Burger',
        'PizzaSlice',
        'IceCreamCone',
        'Airplane',
        'Muscle',
        'CoffeeMug',
        'Banana',
        'Croissant',
        'SushiRoll',
        'Watermelon',
        'Coconut',
        'Donut'
      ],
      isLoading: false,
      generatedMeme: null,
      loadingProgress: 0,
      loadingInterval: null,
      isUnlocking: false
    };
  },
  computed: {
    canGenerate() {
      const walletAddress = Cookies.get('wallet_address');
      return this.selectedAnimal && this.selectedObject && walletAddress && this.generationStore.canGenerate;
    },
    generationMessage() {
      if (!this.isConnected) {
        return 'Connect your wallet first';
      }
      if (!this.generationStore.canGenerate) {
        return `Generation limit reached (${this.generationStore.usedGenerations}/${this.generationStore.limit})`;
      }
      return `Generations left: ${this.generationStore.limit - this.generationStore.usedGenerations}`;
    }
  },
  methods: {
    openAnimalModal() {
      this.showAnimalModal = true;
    },
    closeAnimalModal() {
      this.showAnimalModal = false;
    },
    openObjectModal() {
      this.showObjectModal = true;
    },
    closeObjectModal() {
      this.showObjectModal = false;
    },
    selectAnimal(animal) {
      this.selectedAnimal = animal;
      this.closeAnimalModal();
    },
    selectObject(object) {
      this.selectedObject = object;
      this.closeObjectModal();
    },
    getAnimalIcon(animal) {
      const icons = {
        'Monkey': '🐒',
        'Cat': '🐱',
        'Crocodile': '🐊',
        'Pigeon': '🕊️',
        'Beaver': '🦦',
        'Shark': '🦈',
        'Elephant': '🐘',
        'Frog': '🐸',
        'Cow': '🐮',
        'Penguin': '🐧',
        'Tiger': '🐯',
        'Eagle': '🦅',
        'Hamster': '🐹',
        'Giraffe': '🦒',
        'Goose': '🦢'
      };
      return icons[animal] || '❓';
    },
    getObjectIcon(object) {
      const icons = {
        'Cannabis': '🌿',
        'Cactus': '🌵',
        'Pineapple': '🍍',
        'Burger': '🍔',
        'PizzaSlice': '🍕',
        'IceCreamCone': '🍦',
        'Airplane': '✈️',
        'Muscle': '💪',
        'CoffeeMug': '☕',
        'Banana': '🍌',
        'Croissant': '🥐',
        'SushiRoll': '🍣',
        'Watermelon': '🍉',
        'Coconut': '🥥',
        'Donut': '🍩'
      };
      return icons[object] || '❓';
    },
    async generateMeme() {
      if (this.canGenerate && !this.isLoading) {
        try {
          const walletAddress = Cookies.get('wallet_address');
          await this.generationStore.useGeneration(walletAddress);
          
          this.isLoading = true;
          this.loadingProgress = 0;
          
          // Add merging classes
          const animalCard = document.querySelector('.selection-card:first-child');
          const objectCard = document.querySelector('.selection-card:nth-child(2)');
          if (animalCard && objectCard) {
            animalCard.classList.add('merging');
            objectCard.classList.add('merging');
          }

          // Wait for cards to disappear
          await new Promise(resolve => setTimeout(resolve, 2000));

          // Start loading animation with slower progress
          this.loadingInterval = setInterval(() => {
            if (this.loadingProgress < 100) {
              this.loadingProgress += 0.8;
            }
          }, 100);

          const response = await axios.post(`${API_URL}/generate-meme`, {
            animal: this.selectedAnimal,
            object: this.selectedObject
          });

          if (response.data && response.data.image_url) {
            const imageUrl = response.data.image_url;
            if (typeof imageUrl === 'string' && imageUrl.startsWith('http')) {
              this.generatedMeme = {
                imageUrl: imageUrl
              };
            } else {
              console.error('Invalid image URL format:', imageUrl);
            }
          } else {
            console.error('No image_url found in response');
          }
        } catch (error) {
          console.error('Error generating meme:', error);
          if (error.response) {
            console.error('Error response:', error.response.data);
          }
        } finally {
          clearInterval(this.loadingInterval);
          this.isLoading = false;
          this.loadingProgress = 0;
        }
      }
    },
    resetSelection() {
      this.selectedAnimal = null;
      this.selectedObject = null;
      this.addAbsurdElement = false;
      this.showAnimalModal = false;
      this.showObjectModal = false;
      this.showMemeModal = false;
      this.generatedMeme = null;
      this.isLoading = false;
      this.loadingProgress = 0;
    },
    saveMeme() {
      // Create temporary download link
      const link = document.createElement('a');
      link.href = this.generatedMeme.imageUrl;
      // Generate filename based on selected elements
      const fileName = `meme_${this.selectedAnimal?.toLowerCase()}_${this.selectedObject?.toLowerCase()}.jpg`;
      link.download = fileName;
      // Add temporary link to DOM
      document.body.appendChild(link);
      // Click temporary link to download
      link.click();
      // Remove temporary link from DOM
      document.body.removeChild(link);
    },
    shareMeme() {
      const shareUrl = `https://twitter.com/intent/tweet?url=${encodeURIComponent(this.generatedMeme.imageUrl)}&text=${encodeURIComponent('Check this out! @BrainRotLab')}`;
      window.open(shareUrl, '_blank');
    },
    async handleUnlockMore() {
      if (this.isUnlocking) return;
      this.isUnlocking = true;
      try {
        await unlockMore(this.generationStore);
      } catch (err) {
        console.error("Payment error:", err);
        alert("Failed to unlock generations.");
      } finally {
        this.isUnlocking = false;
      }
    }
  },
  setup() {
    const walletStore = useWalletStore();
    const generationStore = useGenerationStore();
    const isConnected = computed(() => walletStore.isConnected);
    
    return {
      isConnected,
      generationStore
    };
  }
};
</script>

<style scoped>

.laboratory-container::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: inherit;
  filter: blur(8px);
  z-index: -1;
}

.laboratory-content {
  position: relative;
  z-index: 1;
  backdrop-filter: blur(5px);
  border-radius: 20px;
  padding: 20px;
  border: 1px solid rgba(255, 255, 255, 0.2);
  width: 100%;
  min-height: calc(100vh - 200px);
  max-width: 1000px;
  margin: 0 auto;
  padding: 2rem 1rem;
  border-radius: 20px;
  margin-top: 1rem;
  position: relative;
  overflow: visible;
  background: rgba(0, 0, 0, 0.3);
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 20px;
}

.laboratory-title {
  font-family: 'Press Start 2P', monospace;
  font-size: 2.5rem;
  color: #00ff00;
  text-align: center;
  margin-bottom: 1rem;
  text-shadow: 
    -2px -2px 0 #000,
    2px -2px 0 #000,
    -2px 2px 0 #000,
    2px 2px 0 #000;
  letter-spacing: 1px;
  text-transform: uppercase;
  animation: glow 2s ease-in-out infinite alternate;
}

@keyframes glow {
  from {
    text-shadow: 
      0 0 5px #00ff00,
      0 0 10px #00ff00;
  }
  to {
    text-shadow: 
      0 0 15px #00ff00,
      0 0 30px #00ff00;
  }
}

.laboratory-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 2rem;
  padding: 1rem;
}

.laboratory-item {
  background: rgba(255, 255, 255, 0.05);
  border-radius: 15px;
  padding: 1.5rem;
  transition: transform 0.3s ease;
  border: 1px solid rgba(255, 0, 255, 0.2);
}

.laboratory-item:hover {
  transform: translateY(-5px);
  box-shadow: 0 0 20px rgba(255, 0, 255, 0.3);
}

.item-image {
  width: 100%;
  height: 200px;
  object-fit: cover;
  border-radius: 10px;
  margin-bottom: 1rem;
}

.item-title {
  color: #ff00ff;
  font-size: 1.5rem;
  margin-bottom: 0.5rem;
}

.item-description {
  color: #ffffff;
  font-size: 1rem;
  line-height: 1.5;
}

.selection-cards {
  display: flex;
  justify-content: center;
  gap: 6rem;
  margin-top: 2rem;
  padding: 0 1rem;
  position: relative;
}

.selection-card {
  background: rgba(255, 255, 255, 0.05);
  backdrop-filter: blur(10px);
  border-radius: 15px;
  padding: 2rem;
  width: 300px;
  height: 300px;
  text-align: center;
  cursor: pointer;
  transition: all 0.3s ease;
  border: 1px solid rgba(255, 0, 255, 0.2);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  position: relative;
  transform-origin: center;
  box-shadow: 0 0 20px rgba(255, 0, 255, 0.2);
}

/* Анимация слияния */
.selection-card.merging {
  animation: mergeAnimation 1.5s ease-in-out forwards;
  position: relative;
  overflow: hidden;
  filter: blur(0);
}

@keyframes mergeAnimation {
  0% {
    filter: blur(0) contrast(100%);
    transform: scale(1);
    opacity: 1;
  }
  20% {
    filter: blur(1px) contrast(150%);
    transform: scale(1.05);
    opacity: 0.9;
  }
  40% {
    filter: blur(2px) contrast(200%);
    transform: scale(0.95);
    opacity: 0.8;
  }
  60% {
    filter: blur(3px) contrast(250%);
    transform: scale(1.02);
    opacity: 0.7;
  }
  80% {
    filter: blur(4px) contrast(300%);
    transform: scale(0.98);
    opacity: 0.6;
  }
  100% {
    filter: blur(5px) contrast(400%);
    transform: scale(0);
    opacity: 0;
  }
}

.selection-card.merging::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: radial-gradient(circle at center, transparent 0%, rgba(255, 0, 255, 0.3) 100%);
  animation: glowEffect 1.5s ease-in-out forwards;
  z-index: 1;
  filter: inherit;
}

@keyframes glowEffect {
  0% {
    background: radial-gradient(circle at center, transparent 0%, rgba(255, 0, 255, 0.3) 100%);
    transform: scale(1);
  }
  50% {
    background: radial-gradient(circle at center, transparent 0%, rgba(255, 0, 255, 0.5) 100%);
    transform: scale(1.2);
  }
  100% {
    background: radial-gradient(circle at center, transparent 0%, rgba(255, 0, 255, 0.7) 100%);
    transform: scale(1.5);
  }
}

/* Добавляем эффект втягивания в центр */
.laboratory-content::after {
  content: '';
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 0;
  height: 0;
  background: radial-gradient(circle, rgba(255, 0, 255, 0.8) 0%, transparent 70%);
  animation: centerAbsorption 1.5s ease-in-out forwards;
  z-index: 2;
  pointer-events: none;
  filter: blur(2px);
}

@keyframes centerAbsorption {
  0% {
    width: 0;
    height: 0;
    opacity: 0;
    filter: blur(0);
  }
  50% {
    width: 200px;
    height: 200px;
    opacity: 0.8;
    filter: blur(4px);
  }
  100% {
    width: 0;
    height: 0;
    opacity: 0;
    filter: blur(8px);
  }
}

.selection-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 0 40px rgba(255, 0, 255, 0.4);
  border-color: rgba(255, 0, 255, 0.5);
}

/* Добавляем стили для выбранной карточки */
.selection-card.selected {
  background: rgba(0, 255, 0, 0.05);
  border-color: rgba(0, 255, 0, 0.4);
  box-shadow: 0 0 40px rgba(0, 255, 0, 0.3);
}

.selection-card.selected:hover {
  background: rgba(0, 255, 0, 0.1);
  border-color: rgba(0, 255, 0, 0.6);
  box-shadow: 0 0 50px rgba(0, 255, 0, 0.4);
}

/* Стили для карточки с предметом */
.selection-card:nth-child(2).selected {
  background: rgba(0, 102, 255, 0.05);
  border-color: rgba(0, 102, 255, 0.4);
  box-shadow: 0 0 40px rgba(0, 102, 255, 0.3);
}

.selection-card:nth-child(2).selected:hover {
  background: rgba(0, 102, 255, 0.1);
  border-color: rgba(0, 102, 255, 0.6);
  box-shadow: 0 0 50px rgba(0, 102, 255, 0.4);
}

.card-icon {
  font-size: 4rem;
  margin-bottom: 1.5rem;
  filter: drop-shadow(0 0 15px rgba(255, 0, 255, 0.6));
}

.card-title {
  color: #ff00ff;
  font-size: 1.8rem;
  margin-bottom: 1rem;
  text-shadow: 0 0 15px rgba(255, 0, 255, 0.6);
}

.card-description {
  color: #ffffff;
  font-size: 1.1rem;
  margin-bottom: 1.5rem;
  opacity: 0.8;
}

.selected-full {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 1rem;
  width: 100%;
  height: 100%;
}

.selected-full .selected-icon {
  font-size: 6rem;
  filter: drop-shadow(0 0 20px rgba(0, 255, 0, 0.7));
}

.selected-full .selected-name {
  font-size: 2rem;
  color: #00ff00;
  text-shadow: 0 0 10px rgba(0, 255, 0, 0.5);
  text-align: center;
  word-break: break-word;
  padding: 0 1rem;
  display: none;
}

.selection-card:hover .selected-full .selected-icon {
  transform: scale(1.1);
  filter: drop-shadow(0 0 15px rgba(0, 255, 0, 0.7));
}

.selection-card:hover .selected-full .selected-name {
  transform: scale(1.05);
  text-shadow: 0 0 15px rgba(0, 255, 0, 0.7);
}

/* Обновляем стили для выбранного предмета */
.selection-card:nth-child(2) .selected-full .selected-icon {
  font-size: 6rem;
  filter: drop-shadow(0 0 20px rgba(0, 102, 255, 0.7));
}

.selection-card:nth-child(2) .selected-full .selected-name {
  color: #0066ff;
  text-shadow: 0 0 10px rgba(0, 102, 255, 0.5);
  display: none;
}

.selection-card:nth-child(2):hover .selected-full .selected-icon {
  filter: drop-shadow(0 0 15px rgba(0, 102, 255, 0.7));
}

.selection-card:nth-child(2):hover .selected-full .selected-name {
  text-shadow: 0 0 15px rgba(0, 102, 255, 0.7);
}

.absurd-checkbox {
  margin-top: 2rem;
  text-align: center;
  display: flex;
  justify-content: center;
}

.checkbox-label {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  cursor: pointer;
  padding: 0.5rem 1rem;
  border-radius: 8px;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 0, 255, 0.2);
  transition: all 0.3s ease;
  max-width: 300px;
  width: 100%;
}

.checkbox-label:hover {
  background: rgba(255, 0, 255, 0.1);
  border-color: rgba(255, 0, 255, 0.4);
  transform: translateY(-2px);
}

.checkbox-label:active {
  transform: scale(0.95);
}

.potion-icon {
  font-size: 1.5rem;
  transition: all 0.3s ease;
}

.checkbox-text {
  color: #ffffff;
  font-size: 1.1rem;
  user-select: none;
  transition: all 0.3s ease;
}

.checkbox-text.active {
  color: #00ff00;
  text-shadow: 0 0 10px rgba(0, 255, 0, 0.5);
}

.checkbox-label:hover .potion-icon {
  transform: scale(1.2);
  filter: drop-shadow(0 0 5px rgba(255, 0, 255, 0.5));
}

.checkbox-label:hover .checkbox-text {
  color: #00ff00;
  text-shadow: 0 0 10px rgba(0, 255, 0, 0.3);
}

/* Стили для чекбокса */
.checkbox-label.active {
  background: rgba(255, 0, 255, 0.1);
  border-color: rgba(255, 0, 255, 0.4);
  box-shadow: 0 0 15px rgba(255, 0, 255, 0.3);
}

.checkbox-label.active .potion-icon {
  filter: drop-shadow(0 0 8px rgba(255, 0, 255, 0.6));
  transform: scale(1.1);
}

.checkbox-label.active .checkbox-text {
  color: #ff00ff;
  text-shadow: 0 0 10px rgba(255, 0, 255, 0.5);
}

.modal {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.7);
  backdrop-filter: blur(5px);
  border-radius: 20px;
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-content {
  background: rgba(15, 15, 15, 0.8);
  border-radius: 20px;
  padding: 2rem;
  width: 90%;
  max-width: 800px;
  max-height: 80vh;
  overflow-y: auto;
  border: 1px solid rgba(255, 0, 255, 0.3);
  box-shadow: 0 0 30px rgba(255, 0, 255, 0.2);
  position: relative;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
}

.modal-header h2 {
  color: #00ff00;
  font-size: 2rem;
  margin: 0;
  text-shadow: 0 0 10px rgba(0, 255, 0, 0.5);
}

.close-button {
  background: none;
  border: none;
  color: #ff00ff;
  font-size: 2rem;
  cursor: pointer;
  padding: 0.5rem;
  transition: all 0.3s ease;
}

.close-button:hover {
  color: #00ff00;
  transform: scale(1.2);
}

.modal-body {
  max-height: calc(80vh - 100px);
  overflow-y: auto;
  padding-right: 10px;
}

.modal-body::-webkit-scrollbar {
  width: 8px;
}

.modal-body::-webkit-scrollbar-track {
  background: rgba(255, 255, 255, 0.1);
  border-radius: 4px;
}

.modal-body::-webkit-scrollbar-thumb {
  background: rgba(255, 0, 255, 0.5);
  border-radius: 4px;
}

.modal-body::-webkit-scrollbar-thumb:hover {
  background: rgba(255, 0, 255, 0.7);
}

.selection-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(120px, 1fr));
  gap: 1rem;
  padding: 0.5rem;
}

.selection-item {
  background: rgba(255, 255, 255, 0.05);
  border-radius: 12px;
  padding: 1rem;
  text-align: center;
  cursor: pointer;
  transition: all 0.3s ease;
  border: 1px solid rgba(255, 0, 255, 0.2);
  min-height: 100px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}

.item-icon {
  font-size: 2rem;
  margin-bottom: 0.5rem;
}

.item-name {
  color: #ffffff;
  font-size: 1rem;
  word-break: break-word;
}

.button-wrapper {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  width: 100%;
}

.generate-button-container {
  margin-top: 1rem;
  display: flex;
  justify-content: center;
  align-items: center;
  width: 100%;
}

.generate-button {
  font-family: 'Press Start 2P', monospace;
  font-size: 24px;
  font-weight: 600;
  background-color: #00FF66;
  color: white;
  border: 4px solid #00cc55;
  padding: 20px 30px;
  text-shadow: 
    -2px -2px 0 #000,
    2px -2px 0 #000,
    -2px 2px 0 #000,
    2px 2px 0 #000;
  box-shadow: 0 0 15px #00FF66, 0 0 30px rgba(0, 255, 102, 0.5);
  cursor: pointer;
  transition: all 0.3s ease;
  letter-spacing: 1px;
  text-transform: uppercase;
  border-radius: 8px;
  background: linear-gradient(45deg, #00FF66, #00cc55);
  animation: glow 2s ease-in-out infinite alternate;
  display: flex;
  align-items: center;
  gap: 1rem;
  line-height: 1.5;
  position: relative;
}

.generate-button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  background: linear-gradient(45deg, #666666, #999999);
  box-shadow: none;
  animation: none;
}

.generate-button:not(:disabled):hover {
  transform: scale(1.05);
  box-shadow: 0 0 25px #00FF66, 0 0 50px rgba(0, 255, 102, 0.7);
  color: white;
  text-shadow: 
    -2px -2px 0 #000,
    2px -2px 0 #000,
    -2px 2px 0 #000,
    2px 2px 0 #000;
  background: linear-gradient(45deg, #00FF66, #00cc55, #00FF66);
  animation: glow 1s ease-in-out infinite alternate;
}

.generate-button:not(:disabled):active {
  transform: scale(0.95);
  box-shadow: 0 0 10px #00FF66, 0 0 20px rgba(0, 255, 102, 0.3);
}

.generate-button.loading::after {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  border-radius: 8px;
  display: flex;
  justify-content: center;
  align-items: center;
  color: white;
  font-size: 1.5rem;
}

.generate-button.loading .button-text {
  opacity: 0;
}

.button-icon {
  font-size: 2rem;
  filter: drop-shadow(0 0 5px rgba(255, 64, 129, 0.8));
}

.button-text {
  text-shadow: 
    -2px -2px 0 #000,
    2px -2px 0 #000,
    -2px 2px 0 #000,
    2px 2px 0 #000;
  letter-spacing: 2px;
  color: white;
}

.loading-spinner {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  font-size: 2rem;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from { transform: translate(-50%, -50%) rotate(0deg); }
  to { transform: translate(-50%, -50%) rotate(360deg); }
}

.generated-meme-container {
  margin-top: 2rem;
  display: flex;
  justify-content: center;
  width: 100%;
  padding: 0 1rem;
  opacity: 0;
  animation: fadeInResult 1s ease-in-out forwards;
  animation-delay: 1s;
}

@keyframes fadeInResult {
  0% {
    opacity: 0;
    transform: scale(0.8) rotateY(0deg);
  }
  50% {
    opacity: 1;
    transform: scale(1) rotateY(360deg);
  }
  100% {
    opacity: 1;
    transform: scale(1) rotateY(0deg);
  }
}

.meme-wrapper {
  background: rgba(255, 255, 255, 0.05);
  border-radius: 15px;
  padding: 1rem;
  border: 1px solid rgba(0, 102, 255, 0.2);
  max-width: 400px;
  width: 100%;
  box-shadow: 0 0 30px rgba(0, 102, 255, 0.2);
  transform-style: preserve-3d;
  perspective: 1000px;
}

.generated-meme {
  width: 100%;
  border-radius: 10px;
  margin-bottom: 0.5rem;
  box-shadow: 0 0 20px rgba(0, 102, 255, 0.3);
  aspect-ratio: 1;
  object-fit: cover;
  cursor: pointer;
  transition: all 0.3s ease;
  transform-style: preserve-3d;
}

.generated-meme:hover {
  box-shadow: 0 0 30px rgba(0, 102, 255, 0.5);
  transform: scale(1.02);
  filter: brightness(1.1);
}

.meme-actions {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  margin-top: 1rem;
  width: 100%;
}

.action-buttons-row {
  display: flex;
  gap: 0.5rem;
  width: 100%;
}

.action-button {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  padding: 0.8rem;
  border-radius: 8px;
  border: none;
  cursor: pointer;
  transition: all 0.3s ease;
  font-family: 'Press Start 2P', monospace;
  font-size: 0.8rem;
  flex: 1;
}

.save-button {
  background: linear-gradient(45deg, #00ff00, #00cc00);
  color: white;
  box-shadow: 0 0 15px rgba(0, 255, 0, 0.3);
}

.save-button:hover {
  background: linear-gradient(45deg, #00cc00, #00ff00);
  box-shadow: 0 0 20px rgba(0, 255, 0, 0.5);
  transform: translateY(-2px);
}

.share-button {
  background: linear-gradient(45deg, #0066ff, #001b6b);
  color: white;
  box-shadow: 0 0 15px rgba(0, 102, 255, 0.3);
}

.share-button:hover {
  background: linear-gradient(45deg, #0033cc, #0066ff);
  box-shadow: 0 0 20px rgba(0, 102, 255, 0.5);
  transform: translateY(-2px);
}

.mint-button {
  background: linear-gradient(45deg, #ff00ff, #cc00cc);
  color: white;
  box-shadow: 0 0 15px rgba(255, 0, 255, 0.3);
  opacity: 0.7;
  cursor: not-allowed;
}

.mint-button:hover {
  background: linear-gradient(45deg, #cc00cc, #ff00ff);
  box-shadow: 0 0 20px rgba(255, 0, 255, 0.5);
}

.button-icon {
  font-size: 1.2rem;
}

.button-text {
  text-shadow: 
    -1px -1px 0 #000,
    1px -1px 0 #000,
    -1px 1px 0 #000,
    1px 1px 0 #000;
}

.refresh-btn {
  position: absolute;
  top: 1rem;
  right: 1rem;
  background: none;
  border: none;
  width: 60px;
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.3s ease;
  color: #ff00ff;
  font-size: 2rem;
}

.refresh-btn:hover {
  transform: rotate(180deg);
  color: #ff66ff;
}

.refresh-icon {
  transition: transform 0.3s ease;
  text-shadow: 0 0 10px rgba(255, 0, 255, 0.5);
}

.refresh-btn:hover .refresh-icon {
  transform: rotate(180deg);
  text-shadow: 0 0 20px rgba(255, 0, 255, 0.8);
}

/* Модальное окно для увеличенного просмотра */
.meme-modal {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.301);
  backdrop-filter: blur(20px);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 9999;
  cursor: pointer;
  animation: modalFadeIn 0.3s ease;
  pointer-events: auto;
}

.meme-modal img {
  max-width: 90%;
  max-height: 90vh;
  border-radius: 20px;
  box-shadow: 0 0 50px rgba(0, 102, 255, 0.4);
  animation: fadeIn 0.3s ease;
  object-fit: contain;
  border: 2px solid rgba(0, 102, 255, 0.3);
  pointer-events: none;
}

.meme-modal::before {
  content: '×';
  position: fixed;
  top: 2rem;
  right: 2rem;
  color: #ff00ff;
  font-size: 2.5rem;
  cursor: pointer;
  transition: all 0.3s ease;
  text-shadow: 0 0 15px rgba(255, 0, 255, 0.5);
  z-index: 10000;
  background: rgba(0, 0, 0, 0.5);
  width: 50px;
  height: 50px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  border: 1px solid rgba(255, 0, 255, 0.3);
  pointer-events: auto;
}

.meme-modal::before:hover {
  color: #00ff00;
  transform: scale(1.2);
  background: rgba(0, 0, 0, 0.7);
  border-color: rgba(0, 255, 0, 0.5);
}

@keyframes modalFadeIn {
  from { 
    opacity: 0; 
    backdrop-filter: blur(0);
  }
  to { 
    opacity: 1; 
    backdrop-filter: blur(20px);
  }
}

@keyframes fadeIn {
  from { 
    opacity: 0; 
    transform: scale(0.95); 
  }
  to { 
    opacity: 1; 
    transform: scale(1); 
  }
}

/* Медиа-запрос для планшетов */
@media (max-width: 768px) {
  .laboratory-content {
    padding: 10px 0;
    min-height: calc(100vh - 240px);
  }

  .selection-cards {
    width: 100%;
    padding: 0 10px;
  }

  .selection-card {
    width: 100%;
    margin-bottom: 10px;
  }

  .absurd-checkbox {
    width: 100%;
    padding: 0 10px;
  }

  .generate-button-container {
    width: 100%;
    padding: 0 10px;
  }

  .generated-meme-container {
    width: 100%;
    padding: 0 10px;
  }

  .modal-content {
    width: 100%;
    margin: 0;
    border-radius: 0;
  }

  .selection-grid {
    grid-template-columns: repeat(2, 1fr);
    gap: 8px;
    padding: 8px;
  }

  .card-icon {
    font-size: 3.5rem;
    margin-bottom: 1rem;
  }

  .selected-full .selected-icon {
    font-size: 5rem;
  }

  .generate-button {
    font-size: 18px;
    padding: 15px 20px;
    width: 80%;
    max-width: 400px;
    display: flex;
    justify-content: center;
    align-items: center;
    text-align: center;
  }

  .generate-button .button-text {
    text-align: center;
    width: 100%;
  }

  .meme-wrapper {
    max-width: 90%;
  }

  .laboratory-title {
    font-size: 2.5rem;
  }

  .checkbox-label {
    padding: 0.8rem 1.2rem;
    font-size: 0.9rem;
    width: 100%;
    display: flex;
    justify-content: center;
    align-items: center;
  }

  .potion-icon {
    font-size: 1.8rem;
  }

  .action-button {
    padding: 0.8rem;
    font-size: 0.8rem;
  }

  .button-icon {
    font-size: 1.2rem;
  }

  .refresh-btn {
    width: 50px;
    height: 50px;
    font-size: 1.8rem;
  }
}

/* Медиа-запрос для мобильных устройств */
@media (max-width: 500px) {
  .laboratory-content {
    min-height: auto;
    padding: 0.5rem 0;
    margin: 0;
    overflow: visible;
  }

  .selection-cards {
    gap: 1.5rem;
    padding: 0 0.5rem;
    flex-direction: column;
    align-items: center;
    width: 100%;
    margin-bottom: 1.5rem;
  }

  .selection-card {
    width: 90%;
    max-width: 400px;
    height: 200px;
    padding: 1.5rem;
  }

  .card-icon {
    font-size: 4rem;
    margin-bottom: 1rem;
  }

  .selected-full .selected-icon {
    font-size: 4.5rem;
  }

  .generate-button {
    width: 100%;
    font-size: 18px;
    padding: 15px 20px;
  }

  .generated-meme-container {
    margin: 1.5rem 0;
    width: 90%;
    max-width: 400px;
  }

  .meme-wrapper {
    width: 100%;
  }

  .laboratory-title {
    font-size: 1.6rem;
    padding-top: 20px;
    margin-bottom: 1rem;
  }

  .generate-button-container {
    margin: 1.5rem 0;
    width: 90%;
    max-width: 400px;
  }

  .checkbox-label {
    padding: 0.8rem 1.2rem;
    font-size: 0.9rem;
    width: 100%;
    display: flex;
    justify-content: center;
    align-items: center;
  }

  .potion-icon {
    font-size: 1.8rem;
  }

  .action-button {
    padding: 0.8rem;
    font-size: 0.8rem;
  }

  .button-icon {
    font-size: 1.2rem;
  }

  .modal-content {
    width: 95%;
    padding: 1rem;
  }

  .selection-grid {
    grid-template-columns: repeat(auto-fill, minmax(100px, 1fr));
  }

  .refresh-btn {
    width: 40px;
    height: 40px;
    font-size: 1.5rem;
    top: 0.5rem;
    right: 0.5rem;
  }
}

.loading-container {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 2rem;
  opacity: 0;
  animation: fadeIn 1s ease forwards;
  animation-delay: 2s;
  z-index: 10;
}

.test-tube {
  position: relative;
  width: 120px;
  height: 360px;
  display: flex;
  flex-direction: column;
  align-items: center;
  filter: drop-shadow(0 0 20px rgba(255, 0, 255, 0.5));
}

.test-tube-body {
  width: 100px;
  height: 250px;
  background: rgba(255, 255, 255, 0.05);
  border: 2px solid rgba(255, 0, 255, 0.5);
  border-top: none;
  border-radius: 0 0 20px 20px;
  position: relative;
  overflow: hidden;
}

.liquid {
  position: absolute;
  bottom: 0;
  width: 100%;
  background: linear-gradient(to top, 
    rgba(13, 160, 0, 0.8),
    rgba(0, 255, 0, 0.8)
  );
  transition: height 0.1s ease;
  border-radius: 0 0 18px 18px;
}

.test-tube-bottom {
  width: 100px;
  height: 20px;
  background: rgba(255, 255, 255, 0.1);
  border: 2px solid rgba(255, 0, 255, 0.5);
  border-top: none;
  border-radius: 0 0 20px 20px;
  margin-top: -2px;
}

.loading-text {
  color: #00ff00;
  font-family: 'Press Start 2P', monospace;
  font-size: 1.2rem;
  text-shadow: 0 0 10px rgba(0, 255, 0, 0.5);
  animation: pulse 1.5s ease-in-out infinite;
}

@keyframes pulse {
  0% { opacity: 0.5; }
  50% { opacity: 1; }
  100% { opacity: 0.5; }
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

.wallet-connect-text {
  font-family: 'Press Start 2P', monospace;
  color: #00ff00;
  font-size: 0.8rem;
  margin-bottom: 1rem;
  text-shadow: 0 0 10px rgba(0, 255, 0, 0.5);
  letter-spacing: 1px;
  animation: blink 1.5s ease-in-out infinite;
}

@keyframes blink {
  0% { opacity: 1; }
  50% { opacity: 0.3; }
  100% { opacity: 1; }
}

.generate-button.unlock-button {
  background: linear-gradient(45deg, #ff00ff, #cc00cc);
  border-color: #cc00cc;
  box-shadow: 0 0 15px #ff00ff, 0 0 30px rgba(255, 0, 255, 0.5);
}

.generate-button.unlock-button:hover {
  background: linear-gradient(45deg, #cc00cc, #ff00ff);
  box-shadow: 0 0 25px #ff00ff, 0 0 50px rgba(255, 0, 255, 0.7);
}

.generate-button.unlock-button:disabled {
  background: linear-gradient(45deg, #666666, #999999);
  border-color: #666666;
  box-shadow: none;
}

.generate-button.disabled {
  opacity: 0.5;
  cursor: not-allowed;
}
</style> 