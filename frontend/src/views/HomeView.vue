<template>
  <div class="home">
    <div class="crypto-background"></div>
    <div class="crypto-background-overlay"></div>

    <!-- Добавляем компонент анимации -->
    <MergeAnimation
      :show="showMergeAnimation"
      :item-image="getSelectedItemImage"
      :animal-image="getSelectedAnimalImage"
      :result-image="generatedImage"
      @animation-complete="onAnimationComplete"
    />

    <v-container class="fill-height d-flex flex-column position-relative">
      <v-row justify="center">
        <v-col cols="12" md="11" lg="12" xl="12">
          <div class="page-switcher">
            <v-btn
              class="page-btn"
              :class="{ 'active': currentPage === 'generator' }"
              @click="currentPage = 'generator'"
            >
              <v-icon start class="mr-2">mdi-image-plus</v-icon>
              <span class="btn-text">Generator</span>
            </v-btn>
            <v-btn
              class="page-btn"
              :class="{ 'active': currentPage === 'leaderboard' }"
              @click="currentPage = 'leaderboard'"
            >
              <v-icon start class="mr-2">mdi-trophy</v-icon>
              <span class="btn-text">Leaderboard</span>
            </v-btn>
          </div>
        </v-col>
      </v-row>

      <v-row v-if="currentPage === 'generator'" justify="center">
        <v-col cols="12" md="11" lg="12" xl="12">
          <div class="content-wrapper">
            <div class="content-background"></div>
            <div class="content-glow-1"></div>
            <div class="content-glow-2"></div>
            
            <div class="content-inner">
              <v-row justify="center" class="mb-8">
                <v-col cols="12">
                  <h2 class="text-h3 text-center gradient-text">BrainRot Generator</h2>
                </v-col>
              </v-row>

              <v-row justify="center" class="selection-row">
                <!-- Карточка выбранного предмета -->
                <v-col cols="12" md="5" lg="5" xl="5">
                  <div class="selection-title gradient-text mb-4">Select Item</div>
                  <v-card
                    class="selection-card"
                    elevation="2"
                    @click="showItemDialog = true"
                  >
                    <div v-if="selectedItem" class="selection-content">
                      <v-img
                        :src="getSelectedItemImage"
                        :aspect-ratio="1"
                        cover
                        class="selection-image"
                      ></v-img>
                    </div>
                    <div v-else class="empty-selection">
                      <v-icon size="48" color="rgba(139, 92, 246, 0.5)" class="mb-2">mdi-plus-circle-outline</v-icon>
                      <div class="empty-text">Select</div>
                    </div>
                  </v-card>
                </v-col>

                <!-- Разделитель -->
                <v-col cols="12" md="2" lg="2" xl="2" class="d-flex justify-center align-center position-relative">
                  <div class="separator"></div>
                  <div class="plus-sign">+</div>
                </v-col>

                <!-- Карточка выбранного животного -->
                <v-col cols="12" md="5" lg="5" xl="5">
                  <div class="selection-title gradient-text mb-4">Select Animal</div>
                  <v-card
                    class="selection-card"
                    elevation="2"
                    @click="showAnimalDialog = true"
                  >
                    <div v-if="selectedAnimal" class="selection-content">
                      <v-img
                        :src="getSelectedAnimalImage"
                        :aspect-ratio="1"
                        cover
                        class="selection-image"
                      ></v-img>
                    </div>
                    <div v-else class="empty-selection">
                      <v-icon size="48" color="rgba(139, 92, 246, 0.5)" class="mb-2">mdi-plus-circle-outline</v-icon>
                      <div class="empty-text">Select</div>
                    </div>
                  </v-card>
                </v-col>
              </v-row>

              <v-row justify="center" class="mt-12 mb-8">
                <v-col cols="12" class="text-center d-flex justify-center">
                  <v-btn
                    color="#8B5CF6"
                    :loading="loading"
                    class="generate-btn"
                    elevation="4"
                    height="64"
                    @click="generateMeme"
                  >
                    <v-icon start class="mr-2">mdi-image-plus</v-icon>
                    Generate Meme
                  </v-btn>
                </v-col>
              </v-row>

              <v-row v-if="generatedImage" justify="center" class="mt-8">
                <v-col cols="12" md="8">
                  <v-card class="result-card">
                    <v-img
                      :src="generatedImage"
                      max-height="500"
                      contain
                      class="generated-image"
                      @click="showFullscreenImage = true"
                      style="cursor: pointer;"
                    ></v-img>
                    <v-card-actions class="pa-4">
                      <v-btn
                        color="#8B5CF6"
                        block
                        class="save-btn"
                        elevation="2"
                        @click="saveImage"
                        :loading="loading"
                        :disabled="!generatedImage"
                      >
                        <v-icon start class="mr-2">mdi-content-save</v-icon>
                        Save Meme
                      </v-btn>
                    </v-card-actions>
                  </v-card>
                </v-col>
              </v-row>
            </div>
          </div>
        </v-col>
      </v-row>

      <v-row v-if="currentPage === 'leaderboard'" justify="center">
        <v-col cols="12" md="11" lg="12" xl="12">
          <div class="content-wrapper">
            <div class="content-background"></div>
            <div class="content-glow-1"></div>
            <div class="content-glow-2"></div>
            
            <div class="content-inner">
              <v-row justify="center" class="mb-8">
                <v-col cols="12">
                  <h2 class="text-h3 text-center gradient-text">Leaderboard</h2>
                </v-col>
              </v-row>

              <LeaderboardComponent />
            </div>
          </div>
        </v-col>
      </v-row>
    </v-container>

    <!-- Диалог выбора предмета -->
    <v-dialog
      v-model="showItemDialog"
      max-width="600"
      class="selection-dialog"
      content-class="dialog-content-wrapper"
    >
      <v-card class="dialog-card">
        <v-card-title class="dialog-title gradient-text text-center">Select Item</v-card-title>
        <v-card-text class="dialog-content">
          <v-row class="ma-0">
            <v-col v-for="item in itemsData" :key="item.name" cols="6" sm="6" md="4" class="pa-2">
              <v-card
                class="dialog-item-card"
                :class="{ 'selected': selectedItem === item.name }"
                @click="selectItem(item)"
                elevation="2"
              >
                <v-img
                  :src="item.image"
                  :aspect-ratio="1"
                  cover
                  class="dialog-item-image"
                ></v-img>
              </v-card>
            </v-col>
          </v-row>
        </v-card-text>
      </v-card>
    </v-dialog>

    <!-- Диалог выбора животного -->
    <v-dialog
      v-model="showAnimalDialog"
      max-width="600"
      class="selection-dialog"
      content-class="dialog-content-wrapper"
    >
      <v-card class="dialog-card">
        <v-card-title class="dialog-title gradient-text text-center">Select Animal</v-card-title>
        <v-card-text class="dialog-content">
          <v-row class="ma-0">
            <v-col v-for="animal in animalsData" :key="animal.name" cols="6" sm="6" md="4" class="pa-2">
              <v-card
                class="dialog-item-card"
                :class="{ 'selected': selectedAnimal === animal.name }"
                @click="selectAnimal(animal)"
                elevation="2"
              >
                <v-img
                  :src="animal.image"
                  :aspect-ratio="1"
                  cover
                  class="dialog-item-image"
                ></v-img>
              </v-card>
            </v-col>
          </v-row>
        </v-card-text>
      </v-card>
    </v-dialog>

    <!-- Диалог голосования -->
    <v-dialog
      v-model="showVoteDialog"
      max-width="600"
      class="vote-dialog"
      content-class="dialog-content-wrapper"
    >
      <v-card class="dialog-card">
        <v-card-title class="dialog-title gradient-text text-center">Vote for Meme</v-card-title>
        <v-card-text class="dialog-content">
          <div class="vote-meme-preview">
            <v-img
              :src="selectedMeme?.image"
              width="300"
              height="300"
              cover
              class="vote-meme-image"
            ></v-img>
            <div class="vote-meme-info">
              <h3 class="vote-meme-title">{{ selectedMeme?.title }}</h3>
            </div>
            <div class="custom-vote-input">
              <v-text-field
                v-model="customVotePoints"
                type="number"
                label="Enter points"
                variant="outlined"
                density="comfortable"
                hide-details
                class="custom-vote-field"
                :rules="[v => v > 0 || 'Points must be greater than 0']"
              >
              </v-text-field>
            </div>
            <div class="dialog-actions">
              <v-btn
                color="rgba(139, 92, 246, 0.2)"
                class="cancel-btn"
                @click="closeVoteDialog"
              >
                Cancel
              </v-btn>
              <v-btn
                color="#8B5CF6"
                class="submit-btn"
                :disabled="!customVotePoints"
                @click="submitVote"
              >
                Submit Vote
              </v-btn>
            </div>
          </div>
        </v-card-text>
      </v-card>
    </v-dialog>

    <!-- Диалог для просмотра изображения -->
    <v-dialog
      v-model="showFullscreenImage"
      fullscreen
      class="fullscreen-dialog"
      transition="dialog-bottom-transition"
    >
      <v-card class="fullscreen-card">
        <v-toolbar dark color="rgba(19, 17, 26, 0.95)">
          <v-btn
            icon
            @click="showFullscreenImage = false"
          >
            <v-icon>mdi-close</v-icon>
          </v-btn>
          <v-toolbar-title>Preview</v-toolbar-title>
          <v-spacer></v-spacer>
          <v-btn
            icon
            @click="saveImage"
            :disabled="!generatedImage"
          >
            <v-icon>mdi-download</v-icon>
          </v-btn>
        </v-toolbar>
        <div class="fullscreen-image-container">
          <v-img
            :src="generatedImage"
            contain
            height="100%"
            class="fullscreen-image"
          ></v-img>
        </div>
      </v-card>
    </v-dialog>
  </div>
</template>

<script>
import LeaderboardComponent from '@/components/LeaderboardComponent.vue';
import MergeAnimation from '@/components/MergeAnimation.vue';

export default {
  name: 'HomeView',
  components: {
    LeaderboardComponent,
    MergeAnimation
  },
  data() {
    return {
      currentPage: 'generator',
      selectedItem: null,
      selectedAnimal: null,
      showItemDialog: false,
      showAnimalDialog: false,
      showVoteDialog: false,
      selectedMeme: null,
      customVotePoints: '',
      showMergeAnimation: false,
      loading: false,
      generatedImage: null,
      showFullscreenImage: false,
      itemsData: [
        {
          name: 'банан',
          image: 'https://images.unsplash.com/photo-1571771894821-ce9b6c11b08e?w=500&auto=format'
        },
        {
          name: 'кокос',
          image: 'https://images.unsplash.com/photo-1580984969071-a8da5656c2fb?w=500&auto=format'
        },
        {
          name: 'самолет',
          image: 'https://images.unsplash.com/photo-1436491865332-7a61a109cc05?w=500&auto=format'
        }
      ],
      animalsData: [
        {
          name: 'крокодил',
          image: 'https://images.unsplash.com/photo-1597143720583-3970660d6cd8?w=500&auto=format'
        },
        {
          name: 'обезьяна',
          image: 'https://images.unsplash.com/photo-1540573133985-87b6da6d54a9?w=500&auto=format'
        },
        {
          name: 'бобёр',
          image: 'https://images.unsplash.com/photo-1589860170912-6b83cf6f8809?w=500&auto=format'
        }
      ],
    }
  },
  computed: {
    getSelectedItemImage() {
      const item = this.itemsData.find(i => i.name === this.selectedItem)
      return item ? item.image : ''
    },
    getSelectedAnimalImage() {
      const animal = this.animalsData.find(a => a.name === this.selectedAnimal)
      return animal ? animal.image : ''
    }
  },
  methods: {
    selectItem(item) {
      this.selectedItem = item.name
      this.showItemDialog = false
    },
    selectAnimal(animal) {
      this.selectedAnimal = animal.name
      this.showAnimalDialog = false
    },
    async generateMeme() {
      if (!this.selectedItem || !this.selectedAnimal) {
        // Добавить уведомление пользователю
        return;
      }

      this.loading = true;
      this.generatedImage = null; // Сбрасываем предыдущий результат

      try {
        // Показываем анимацию слияния
        this.showMergeAnimation = true;

        // Отправляем запрос на создание мема
        const response = await fetch('http://localhost:8000/api/generate_image/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            prompt: `Create a high-quality, detailed meme image combining ${this.selectedItem} and ${this.selectedAnimal}. The image should be surreal, absurd, and entertaining, with vibrant colors and professional composition. The style should be similar to BombordiroCrocodilo and Bombini Goosini memes, featuring a clean, modern look with a touch of surrealism. The result should be a high-quality, detailed image that looks like a professional meme from the BombordiroCrocodilo series.`
          })
        });

        if (!response.ok) {
          throw new Error('Failed to generate meme');
        }

        const data = await response.json();
        this.generatedImage = data.image_url;
        
        // Через 2 секунды скрываем анимацию
        setTimeout(() => {
          this.showMergeAnimation = false;
          this.loading = false;
        }, 2000);
      } catch (error) {
        console.error('Error generating meme:', error);
        this.loading = false;
        this.showMergeAnimation = false;
      }
    },
    onAnimationComplete() {
      this.showMergeAnimation = false;
    },
    saveImage() {
      if (!this.generatedImage) return;
      
      // Создаем временную ссылку для скачивания
      const link = document.createElement('a');
      link.href = this.generatedImage;
      link.download = `meme-${Date.now()}.png`;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
    },
    openVoteDialog(meme) {
      this.selectedMeme = meme;
      this.customVotePoints = '';
      this.showVoteDialog = true;
    },
    closeVoteDialog() {
      this.showVoteDialog = false;
      this.selectedMeme = null;
      this.customVotePoints = '';
    },
    submitVote() {
      if (!this.selectedMeme) return;
      
      const points = parseInt(this.customVotePoints);
      if (!points || points <= 0) return;
      
      // Временное обновление очков для демонстрации
      this.selectedMeme.points += points;
      
      this.closeVoteDialog();
      this.customVotePoints = null;
    },
  }
}
</script>

<style>
/* Глобальные стили для фона */
html, body {
  min-height: 100vh;
  margin: 0;
  padding: 0;
  background: #13111A;
  overflow-x: hidden;
}

#app {
  min-height: 100vh;
  background: transparent;
  overflow-x: hidden;
}
</style>

<style scoped>
.home {
  width: 100%;
  color: white;
  display: flex;
  flex-direction: column;
  position: relative;
  overflow: hidden;
}

.crypto-background {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: 
    linear-gradient(125deg, rgba(139, 92, 246, 0.15) 0%, rgba(30, 27, 36, 0) 30%),
    linear-gradient(260deg, rgba(109, 40, 217, 0.15) 10%, rgba(19, 17, 26, 0) 40%),
    linear-gradient(315deg, rgba(76, 29, 149, 0.18) 15%, rgba(19, 17, 26, 0) 35%),
    linear-gradient(to bottom, #13111A 0%, #1E1B24 50%, #13111A 100%);
  z-index: 0;
  pointer-events: none;
  animation: gradientShift 15s ease infinite;
}

.crypto-background::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: 
    radial-gradient(circle at 20% 20%, rgba(139, 92, 246, 0.15) 0%, transparent 40%),
    radial-gradient(circle at 80% 80%, rgba(109, 40, 217, 0.15) 0%, transparent 40%),
    radial-gradient(circle at 50% 50%, rgba(76, 29, 149, 0.12) 0%, transparent 60%);
  z-index: 1;
  pointer-events: none;
  animation: glowPulse 8s ease-in-out infinite;
}

.crypto-background::after {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: 
    radial-gradient(2px 2px at 20% 30%, rgba(139, 92, 246, 0.7) 50%, transparent 50%),
    radial-gradient(2px 2px at 40% 70%, rgba(109, 40, 217, 0.6) 50%, transparent 50%),
    radial-gradient(2px 2px at 60% 20%, rgba(139, 92, 246, 0.7) 50%, transparent 50%),
    radial-gradient(2px 2px at 80% 50%, rgba(76, 29, 149, 0.6) 50%, transparent 50%);
  background-size: 250px 250px;
  z-index: 2;
  opacity: 0.4;
  pointer-events: none;
  animation: starFloat 60s linear infinite;
}

.content-wrapper {
  position: relative;
  padding: 32px;
  border-radius: 32px;
  background: rgba(19, 17, 26, 0.75);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(139, 92, 246, 0.2);
  overflow: hidden;
  width: 100%;
  max-width: 2400px;
  margin: 0 auto;
  box-sizing: border-box;
  box-shadow: 
    0 0 60px rgba(139, 92, 246, 0.1),
    inset 0 0 40px rgba(109, 40, 217, 0.05);
}

.content-background {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: 
    radial-gradient(circle at 0% 0%, rgba(139, 92, 246, 0.08) 0%, transparent 50%),
    radial-gradient(circle at 100% 100%, rgba(109, 40, 217, 0.08) 0%, transparent 50%);
  opacity: 0.8;
  z-index: 0;
  pointer-events: none;
}

.content-glow-1 {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: radial-gradient(circle at 30% 30%, rgba(139, 92, 246, 0.12) 0%, transparent 60%);
  filter: blur(40px);
  z-index: 1;
  pointer-events: none;
  opacity: 0.6;
  animation: glow1Move 15s ease-in-out infinite;
}

.content-glow-2 {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: radial-gradient(circle at 70% 70%, rgba(109, 40, 217, 0.12) 0%, transparent 60%);
  filter: blur(40px);
  z-index: 1;
  pointer-events: none;
  opacity: 0.6;
  animation: glow2Move 12s ease-in-out infinite;
}

.content-inner {
  position: relative;
  z-index: 2;
  width: 100%;
}

.position-relative {
  position: relative;
  z-index: 2;
  width: 100%;
}

.v-container {
  width: 100% !important;
  max-width: 100% !important;
  padding: 16px !important;
  margin: 0 !important;
  box-sizing: border-box !important;
  overflow: hidden;
}

.selection-title {
  font-size: 1.5rem;
  font-weight: 600;
  text-align: center;
  text-shadow: 0 0 20px rgba(139, 92, 246, 0.5);
  margin-bottom: 2rem !important;
}

.selection-card {
  background: rgba(30, 27, 36, 0.9) !important;
  border: 2px solid rgba(139, 92, 246, 0.2) !important;
  border-radius: 24px !important;
  overflow: hidden;
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
  cursor: pointer;
  width: 100%;
  margin-bottom: 1rem;
  aspect-ratio: 1/1;
  max-height: 1000px;
  display: flex;
  flex-direction: column;
  box-shadow: 0 8px 32px rgba(19, 17, 26, 0.3);
}

.selection-content {
  height: 100%;
  display: flex;
  flex-direction: column;
  background: rgba(19, 17, 26, 0.8);
}

.selection-image {
  flex: 1;
  width: 100%;
  height: 100% !important;
  background: rgba(19, 17, 26, 0.8);
  object-fit: cover;
}

.separator {
  width: 2px;
  height: 200px;
  background: linear-gradient(180deg, rgba(139, 92, 246, 0.3) 0%, rgba(139, 92, 246, 0) 100%);
  margin: 0 3rem;
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
}

.gradient-text {
  background: linear-gradient(135deg, #8B5CF6 0%, #6D28D9 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  font-weight: 700;
}

.generate-btn {
  width: 100% !important;
  max-width: 300px !important;
  height: 56px !important;
  font-size: 1.1rem !important;
  margin: 0 !important;
  border-radius: 16px !important;
}

.result-card {
  background: rgba(30, 27, 36, 0.8) !important;
  border-radius: 24px !important;
  border: 1px solid rgba(139, 92, 246, 0.2) !important;
  overflow: hidden;
  backdrop-filter: blur(10px);
  width: 100%;
  max-width: 2400px;
  margin: 0 auto;
  animation: memeAppear 0.6s cubic-bezier(0.34, 1.56, 0.64, 1);
  transform-origin: center;
}

@keyframes memeAppear {
  0% {
    opacity: 0;
    transform: scale(0.8) translateY(20px);
  }
  100% {
    opacity: 1;
    transform: scale(1) translateY(0);
  }
}

.generated-image {
  border-bottom: 1px solid rgba(139, 92, 246, 0.2);
  background: rgba(19, 17, 26, 0.8);
  width: 100%;
  height: auto;
  max-height: 800px;
  object-fit: contain;
  display: block;
  transition: transform 0.3s ease, box-shadow 0.3s ease !important;
  cursor: pointer !important;
  animation: imageAppear 0.8s cubic-bezier(0.34, 1.56, 0.64, 1);
  transform-origin: center;
}

@keyframes imageAppear {
  0% {
    opacity: 0;
    transform: scale(0.9);
  }
  50% {
    opacity: 0.5;
    transform: scale(0.95);
  }
  100% {
    opacity: 1;
    transform: scale(1);
  }
}

.save-btn {
  border-radius: 12px !important;
  font-weight: 700 !important;
  text-transform: none !important;
  height: 48px !important;
  background: linear-gradient(135deg, #8B5CF6 0%, #6D28D9 100%) !important;
  box-shadow: 
    0 0 30px rgba(139, 92, 246, 0.4),
    0 0 0 1px rgba(139, 92, 246, 0.3) !important;
  width: 100%;
  max-width: 300px;
  margin: 0 auto !important;
  opacity: 1 !important;
  cursor: pointer !important;
  transition: all 0.3s ease !important;
  position: relative;
  overflow: hidden !important;
  letter-spacing: 0.5px !important;
}

.save-btn .v-btn__content {
  color: #FFFFFF !important;
  font-size: 1.1rem !important;
  font-weight: 700 !important;
  letter-spacing: 0.5px !important;
  opacity: 1 !important;
}

.save-btn .v-icon {
  color: #FFFFFF !important;
  opacity: 1 !important;
}

.save-btn:hover {
  transform: translateY(-2px) !important;
  box-shadow: 
    0 0 40px rgba(139, 92, 246, 0.5),
    0 0 0 1px rgba(139, 92, 246, 0.4) !important;
}

.save-btn:active {
  transform: translateY(0) !important;
  box-shadow: 
    0 0 20px rgba(139, 92, 246, 0.3),
    0 0 0 1px rgba(139, 92, 246, 0.3) !important;
}

.save-btn:disabled {
  opacity: 0.7 !important;
  cursor: not-allowed !important;
  background: linear-gradient(135deg, #6B7280, #4B5563) !important;
  box-shadow: none !important;
}

.save-btn:disabled .v-btn__content,
.save-btn:disabled .v-icon {
  opacity: 0.7 !important;
  color: rgba(255, 255, 255, 0.7) !important;
}

.selection-row {
  margin: 0 !important;
  width: 100%;
}

.empty-selection {
  height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  background: rgba(19, 17, 26, 0.8);
  padding: 20px;
}

.empty-text {
  color: rgba(255, 255, 255, 0.7);
  font-size: 1.1rem;
  margin-top: 12px;
  font-weight: 500;
}

.selection-dialog {
  display: flex;
  align-items: center;
  justify-content: center;
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
}

:deep(.v-overlay__content) {
  align-items: center;
  display: flex;
  justify-content: center;
  width: 100%;
  height: 100%;
}

.dialog-content-wrapper {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 100%;
  height: 100%;
}

.dialog-card {
  background: rgba(19, 17, 26, 0.95) !important;
  border: 1px solid rgba(139, 92, 246, 0.2);
  border-radius: 24px !important;
  overflow: hidden;
  margin: 0;
  max-height: 90vh;
  width: 90vw;
  max-width: 600px !important;
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
}

.dialog-title {
  font-size: 1.5rem !important;
  padding: 24px !important;
  border-bottom: 1px solid rgba(139, 92, 246, 0.2);
  text-align: center !important;
  width: 100%;
}

.dialog-content {
  padding: 24px !important;
  background: rgba(19, 17, 26, 0.8);
  display: flex;
  justify-content: center;
  align-items: flex-start;
  width: 100%;
}

.dialog-content .v-row {
  width: 100%;
  margin: 0 !important;
}

.dialog-item-card {
  background: rgba(30, 27, 36, 0.8) !important;
  border: 2px solid rgba(139, 92, 246, 0.2) !important;
  border-radius: 16px !important;
  overflow: hidden;
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
  cursor: pointer;
  aspect-ratio: 1/1;
  width: 100%;
  box-shadow: 0 4px 24px rgba(19, 17, 26, 0.2);
}

.dialog-item-image {
  width: 100%;
  height: 100% !important;
  object-fit: cover;
  background: rgba(19, 17, 26, 0.8);
}

.dialog-item-card:hover {
  transform: translateY(-4px) scale(1.02);
  border-color: rgba(139, 92, 246, 0.6) !important;
  box-shadow: 
    0 12px 36px rgba(139, 92, 246, 0.3),
    0 0 0 1px rgba(139, 92, 246, 0.3);
}

.dialog-item-card.selected {
  border-color: #8B5CF6 !important;
  box-shadow: 
    0 0 40px rgba(139, 92, 246, 0.4),
    0 0 0 2px rgba(139, 92, 246, 0.6) !important;
}

.dialog-item-title {
  font-size: 1rem !important;
  padding: 12px !important;
  text-align: center;
  color: white !important;
  background: linear-gradient(180deg, rgba(30, 27, 36, 0.8) 0%, rgba(19, 17, 26, 0.8) 100%);
}

.plus-sign {
  position: absolute;
  font-size: 3rem;
  font-weight: 600;
  color: rgba(139, 92, 246, 0.7);
  text-shadow: 0 0 20px rgba(139, 92, 246, 0.5);
  display: none;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  z-index: 2;
}

@media (min-width: 1920px) {
  .content-wrapper {
    padding: 40px;
    max-width: 2800px;
  }

  .content-inner {
    padding: 0;
  }

  .mb-8 {
    margin-bottom: 1.5rem !important;
  }

  .mt-12 {
    margin-top: 1.5rem !important;
  }

  .plus-sign {
    display: block;
    font-size: 5rem;
  }

  .selection-title {
    font-size: 2.5rem;
    margin-bottom: 2.5rem !important;
    white-space: nowrap;
  }

  .selection-card {
    aspect-ratio: 1/1;
    max-height: 1200px;
    min-height: 300px;
  }

  .generate-btn {
    max-width: 400px !important;
    height: 72px !important;
    font-size: 1.3rem !important;
  }

  .empty-selection .v-icon {
    font-size: 64px !important;
    height: 64px !important;
    width: 64px !important;
  }

  .empty-text {
    font-size: 1.4rem;
    margin-top: 16px;
  }
}

@media (min-width: 1280px) and (max-width: 1919px) {
  .content-wrapper {
    padding: 32px;
    max-width: 2400px;
  }

  .content-inner {
    padding: 0;
  }

  .mb-8 {
    margin-bottom: 1.25rem !important;
  }

  .mt-12 {
    margin-top: 1.25rem !important;
  }

  .plus-sign {
    display: block;
    font-size: 4rem;
  }

  .selection-title {
    font-size: 2rem;
    margin-bottom: 2rem !important;
    white-space: nowrap;
  }

  .selection-card {
    aspect-ratio: 1/1;
    max-height: 1000px;
    min-height: 300px;
  }

  .generate-btn {
    max-width: 350px !important;
    height: 64px !important;
    font-size: 1.2rem !important;
  }

  .empty-selection .v-icon {
    font-size: 56px !important;
    height: 56px !important;
    width: 56px !important;
  }

  .empty-text {
    font-size: 1.3rem;
    margin-top: 14px;
  }
}

@media (max-width: 960px) {
  .v-container {
    padding: 12px !important;
  }

  .content-wrapper {
    padding: 24px;
    border-radius: 20px;
    max-width: 100%;
    box-shadow: 
      0 0 30px rgba(139, 92, 246, 0.08),
      inset 0 0 20px rgba(109, 40, 217, 0.03);
  }

  .selection-card {
    aspect-ratio: auto;
    height: 280px;
    max-height: 280px;
    margin-bottom: 16px;
  }

  .empty-selection {
    height: 280px;
  }

  .separator {
    width: 100%;
    height: 2px;
    margin: 8px 0;
  }

  .selection-row {
    margin: 0 !important;
    gap: 0 !important;
  }

  .plus-sign {
    display: none;
  }
}

@media (max-width: 600px) {
  .home {
    overflow: hidden;
  }

  .v-container {
    padding: 1rem;
  }

  .content-wrapper {
    padding: 1rem;
    max-width: 100%;
  }

  .home-title {
    font-size: 2rem;
    margin-bottom: 1.5rem;
  }

  .home-subtitle {
    font-size: 1rem;
    margin-bottom: 2rem;
  }

  .action-buttons {
    flex-direction: column;
    gap: 1rem;
    margin-top: 2rem;
  }

  .action-button {
    width: 100%;
    height: 48px;
    font-size: 1rem;
  }

  .action-button .v-icon {
    font-size: 1.5rem;
    margin-right: 0.5rem;
  }

  .leaderboard-container {
    margin-top: 2rem;
  }

  .selection-card {
    height: 240px;
    max-height: 240px;
    margin-bottom: 12px;
  }

  .empty-selection {
    height: 240px;
    padding: 16px;
  }

  .selection-title {
    font-size: 1.25rem;
    margin-bottom: 12px !important;
  }

  .separator {
    margin: 4px 0;
  }

  .plus-sign {
    display: none;
  }
}

@media (max-width: 400px) {
  .v-container {
    padding: 4px !important;
  }

  .content-wrapper {
    padding: 12px;
    border-radius: 12px;
    max-width: 100%;
  }

  .content-inner .mb-8 {
    margin-bottom: 0.75rem !important;
    margin-top: 0.5rem !important;
  }

  .selection-card {
    height: 200px;
  }

  .empty-selection {
    height: 200px;
    padding: 12px;
  }

  .empty-text {
    font-size: 0.9rem;
    margin-top: 6px;
  }

  .generate-btn {
    height: 44px !important;
    font-size: 0.9rem !important;
  }

  .dialog-card {
    width: calc(100vw - 24px);
    max-height: calc(100vh - 24px);
  }

  .plus-sign {
    display: none;
  }
}

/* Фиксы для Safari */
@supports (-webkit-touch-callout: none) {
  .home {
    min-height: -webkit-fill-available;
  }

  .v-container {
    min-height: -webkit-fill-available;
  }
}

@keyframes gradientShift {
  0% {
    background-position: 0% 50%;
  }
  50% {
    background-position: 100% 50%;
  }
  100% {
    background-position: 0% 50%;
  }
}

@keyframes glowPulse {
  0% {
    opacity: 0.6;
    transform: scale(1);
  }
  50% {
    opacity: 0.8;
    transform: scale(1.05);
  }
  100% {
    opacity: 0.6;
    transform: scale(1);
  }
}

@keyframes starFloat {
  0% {
    background-position: 0 0;
  }
  100% {
    background-position: 500px 500px;
  }
}

@keyframes wrapperGlow {
  0% {
    box-shadow: 
      0 0 60px rgba(139, 92, 246, 0.1),
      inset 0 0 40px rgba(109, 40, 217, 0.05);
  }
  50% {
    box-shadow: 
      0 0 70px rgba(139, 92, 246, 0.15),
      inset 0 0 50px rgba(109, 40, 217, 0.08);
  }
  100% {
    box-shadow: 
      0 0 60px rgba(139, 92, 246, 0.1),
      inset 0 0 40px rgba(109, 40, 217, 0.05);
  }
}

@keyframes glow1Move {
  0% {
    transform: translate(0, 0);
  }
  50% {
    transform: translate(10%, 10%);
  }
  100% {
    transform: translate(0, 0);
  }
}

@keyframes glow2Move {
  0% {
    transform: translate(0, 0);
  }
  50% {
    transform: translate(-10%, -10%);
  }
  100% {
    transform: translate(0, 0);
  }
}

.selection-card:hover {
  transform: translateY(-8px);
  border-color: rgba(139, 92, 246, 0.4) !important;
  box-shadow: 
    0 16px 48px rgba(139, 92, 246, 0.2),
    0 0 0 1px rgba(139, 92, 246, 0.2);
}

@keyframes mobilePulse {
  0% {
    opacity: 0.3;
    transform: scale(1);
  }
  50% {
    opacity: 0.4;
    transform: scale(1.1);
  }
  100% {
    opacity: 0.3;
    transform: scale(1);
  }
}

.page-switcher {
  display: flex;
  justify-content: center;
  gap: 16px;
}

.page-btn {
  background: rgba(19, 17, 26, 0.75) !important;
  border: 1px solid rgba(139, 92, 246, 0.2) !important;
  border-radius: 16px !important;
  color: rgba(255, 255, 255, 0.7) !important;
  font-weight: 500 !important;
  text-transform: none !important;
  padding: 16px 32px !important;
  transition: all 0.3s ease !important;
  backdrop-filter: blur(10px);
  display: flex !important;
  align-items: center !important;
  justify-content: center !important;
  min-width: 200px !important;
  font-size: 1.1rem !important;
}

.page-btn:hover {
  background: rgba(30, 27, 36, 0.9) !important;
  border-color: rgba(139, 92, 246, 0.4) !important;
  color: rgba(255, 255, 255, 0.9) !important;
  transform: translateY(-2px);
}

.page-btn.active {
  background: linear-gradient(135deg, #8B5CF6 0%, #6D28D9 100%) !important;
  border-color: transparent !important;
  color: white !important;
  box-shadow: 0 0 20px rgba(139, 92, 246, 0.3) !important;
}

.btn-text {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 100%;
}

@media (min-width: 1920px) {
  .page-switcher {
    margin: 0;
  }
}

@media (min-width: 1280px) and (max-width: 1919px) {
  .page-switcher {
    margin: 0;
  }
}

@media (max-width: 600px) {
  .page-switcher {
    gap: 12px;
    margin: 2rem 0 1rem 0;
  }

  .page-btn {
    padding: 12px 24px !important;
    font-size: 1rem !important;
    min-width: 160px !important;
  }
}

@media (max-width: 400px) {
  .page-switcher {
    gap: 8px;
    margin: 1.5rem 0 1rem 0;
  }

  .page-btn {
    padding: 10px 20px !important;
    font-size: 0.95rem !important;
    min-width: 140px !important;
  }
}

.leaderboard-container {
  width: 100%;
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}

.leaderboard-content {
  background: rgba(30, 27, 36, 0.9);
  border-radius: 16px;
  border: 1px solid rgba(139, 92, 246, 0.3);
  overflow: hidden;
}

.leaderboard-item {
  display: flex;
  align-items: center;
  padding: 16px;
  border-bottom: 1px solid rgba(139, 92, 246, 0.2);
}

.leaderboard-item:last-child {
  border-bottom: none;
}

.rank {
  font-size: 1.5rem;
  font-weight: 600;
  color: #8B5CF6;
  width: 60px;
  text-align: center;
}

.meme-info {
  display: flex;
  align-items: center;
  flex: 1;
}

.meme-thumbnail {
  width: 80px;
  height: 80px;
  border-radius: 8px;
  object-fit: cover;
  margin-right: 16px;
}

.meme-details {
  flex: 1;
}

.meme-details h3 {
  font-size: 1.2rem;
  margin: 0 0 8px 0;
  color: white;
}

.points {
  font-size: 1rem;
  color: rgba(255, 255, 255, 0.8);
}

@media (max-width: 600px) {
  .leaderboard-container {
    padding: 12px;
  }

  .rank {
    font-size: 1.2rem;
    width: 40px;
  }

  .meme-thumbnail {
    width: 60px;
    height: 60px;
    margin-right: 12px;
  }

  .meme-details h3 {
    font-size: 1rem;
    margin-bottom: 4px;
  }

  .points {
    font-size: 0.9rem;
  }
}

.vote-dialog .dialog-card {
  max-width: 600px !important;
  background: rgba(19, 17, 26, 0.98) !important;
  border: 1px solid rgba(139, 92, 246, 0.3) !important;
  box-shadow: 
    0 0 40px rgba(139, 92, 246, 0.2),
    inset 0 0 30px rgba(109, 40, 217, 0.1) !important;
}

.vote-meme-preview {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 24px;
  padding: 0 24px;
  width: 100%;
  box-sizing: border-box;
}

.vote-meme-image {
  border-radius: 24px;
  border: 3px solid rgba(139, 92, 246, 0.3);
  box-shadow: 
    0 8px 32px rgba(139, 92, 246, 0.2),
    0 0 0 1px rgba(139, 92, 246, 0.2);
}

.vote-meme-info {
  text-align: center;
}

.vote-meme-title {
  font-size: 2rem;
  font-weight: 700;
  color: white;
  margin-bottom: 8px;
  text-shadow: 0 0 20px rgba(139, 92, 246, 0.3);
}

.custom-vote-input {
  width: 100%;
  max-width: 250px;
}

.custom-vote-field {
  background: rgba(30, 27, 36, 0.9);
  border-radius: 16px;
  overflow: visible;
}

:deep(.custom-vote-field .v-field) {
  color: white !important;
  background: transparent !important;
  border-color: rgba(139, 92, 246, 0.3) !important;
  font-size: 1.1rem !important;
  padding: 12px !important;
}

:deep(.custom-vote-field .v-field:hover) {
  border-color: rgba(139, 92, 246, 0.5) !important;
}

:deep(.custom-vote-field .v-field--focused) {
  border-color: #8B5CF6 !important;
  box-shadow: 0 0 20px rgba(139, 92, 246, 0.2) !important;
}

:deep(.custom-vote-field .v-label) {
  color: rgba(255, 255, 255, 0.8) !important;
  font-size: 1rem !important;
  font-weight: 500 !important;
  transform-origin: left !important;
  white-space: nowrap !important;
  background: transparent !important;
  padding: 0 4px !important;
}

:deep(.custom-vote-field .v-field--focused .v-label) {
  color: #8B5CF6 !important;
  transform: translateY(-18px) scale(0.75) !important;
  background: rgba(30, 27, 36, 0.9) !important;
}

.dialog-actions {
  width: 100%;
  display: flex;
  gap: 16px;
  justify-content: center;
  background: transparent;
  border-top: none;
  padding: 0 !important;
}

.cancel-btn {
  border-radius: 16px !important;
  font-weight: 600 !important;
  text-transform: none !important;
  height: 48px !important;
  font-size: 1.1rem !important;
  background: rgba(139, 92, 246, 0.2) !important;
  border: 1px solid rgba(139, 92, 246, 0.3) !important;
  color: rgba(255, 255, 255, 0.9) !important;
  transition: all 0.3s ease !important;
}

.cancel-btn:hover {
  background: rgba(139, 92, 246, 0.3) !important;
  border-color: rgba(139, 92, 246, 0.5) !important;
  transform: translateY(-2px);
}

.submit-btn {
  border-radius: 16px !important;
  font-weight: 600 !important;
  text-transform: none !important;
  height: 48px !important;
  font-size: 1.1rem !important;
  background: linear-gradient(135deg, #8B5CF6 0%, #6D28D9 100%) !important;
  box-shadow: 
    0 0 30px rgba(139, 92, 246, 0.4),
    0 0 0 1px rgba(139, 92, 246, 0.3) !important;
  transition: all 0.3s ease !important;
  color: white !important;
  text-shadow: 0 0 10px rgba(255, 255, 255, 0.3) !important;
}

.submit-btn:hover {
  transform: translateY(-2px);
  box-shadow: 
    0 0 40px rgba(139, 92, 246, 0.5),
    0 0 0 1px rgba(139, 92, 246, 0.4) !important;
}

.submit-btn:disabled {
  background: rgba(139, 92, 246, 0.2) !important;
  box-shadow: none !important;
  border-color: rgba(139, 92, 246, 0.2) !important;
}

@media (max-width: 600px) {
  .vote-meme-preview {
    padding: 0 16px;
    gap: 16px;
  }

  .vote-meme-image {
    width: 240px !important;
    height: 240px !important;
  }

  .vote-meme-title {
    font-size: 1.5rem;
  }

  .custom-vote-input {
    width: 100%;
    padding: 0;
    margin: 0;
    margin-bottom: 24px;
  }

  .dialog-actions {
    justify-content: center;
    max-width: 100%;
  }

  .cancel-btn,
  .submit-btn {
    height: 44px !important;
    font-size: 1rem !important;
    flex: 1;
    max-width: 160px;
  }
}

@media (max-width: 400px) {
  .vote-meme-preview {
    padding: 0 12px;
    gap: 12px;
  }

  .vote-meme-image {
    width: 200px !important;
    height: 200px !important;
  }

  .vote-meme-title {
    font-size: 1.25rem;
  }

  .custom-vote-input {
    width: 100%;
    padding: 0;
    margin: 0;
    margin-bottom: 20px;
  }

  .dialog-actions {
    gap: 8px;
    padding: 0 !important;
  }

  .cancel-btn,
  .submit-btn {
    height: 40px !important;
    font-size: 0.95rem !important;
    flex: 1;
    max-width: 140px;
  }
}

.leaderboard-table tbody tr {
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.leaderboard-table tbody tr:hover {
  background-color: rgba(139, 92, 246, 0.05);
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.fullscreen-dialog {
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(19, 17, 26, 0.95) !important;
  overflow: hidden !important;
}

.fullscreen-card {
  width: calc(100% - 32px) !important;
  height: auto !important;
  max-width: min(500px, 100vw - 32px) !important;
  aspect-ratio: 1/1;
  margin: 16px;
  border-radius: 24px !important;
  border: 1px solid rgba(139, 92, 246, 0.2);
  box-shadow: 
    0 0 40px rgba(19, 17, 26, 0.5),
    0 0 0 1px rgba(139, 92, 246, 0.3);
  position: relative;
  transform: none !important;
  background: rgba(19, 17, 26, 0.95) !important;
  overflow: hidden !important;
}

.fullscreen-image-container {
  padding: 0;
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  z-index: 1;
}

.fullscreen-image {
  width: 100% !important;
  height: 100% !important;
  max-width: 100% !important;
  max-height: 100% !important;
  border-radius: 24px;
  object-fit: contain !important;
}

:deep(.v-toolbar) {
  position: absolute !important;
  top: 0;
  left: 0;
  right: 0;
  z-index: 10;
  background: linear-gradient(to bottom, rgba(19, 17, 26, 0.95), transparent) !important;
  border-radius: 24px 24px 0 0;
  backdrop-filter: blur(10px);
  height: 56px !important;
  padding: 0 8px !important;
  display: flex !important;
  align-items: center !important;
  justify-content: space-between !important;
}

:deep(.v-toolbar-title) {
  display: none !important;
}

:deep(.v-toolbar .v-btn) {
  color: #FFFFFF !important;
  opacity: 1 !important;
  transition: all 0.3s ease;
  width: 40px !important;
  height: 40px !important;
  min-width: 40px !important;
  margin: 8px !important;
  background: rgba(139, 92, 246, 0.2) !important;
  border: 1px solid rgba(139, 92, 246, 0.3) !important;
  padding: 0 !important;
  display: flex !important;
  align-items: center !important;
  justify-content: center !important;
}

:deep(.v-toolbar .v-btn:hover) {
  opacity: 1 !important;
  transform: scale(1.1);
  background: rgba(139, 92, 246, 0.3) !important;
  border-color: rgba(139, 92, 246, 0.4) !important;
}

:deep(.v-toolbar .v-btn:active) {
  transform: scale(0.95);
}

:deep(.v-toolbar .v-icon) {
  font-size: 24px;
  color: #FFFFFF !important;
  opacity: 1 !important;
}

:deep(.v-overlay__content) {
  width: 100% !important;
  height: 100% !important;
  max-height: 100vh !important;
  max-width: 100vw !important;
  position: fixed !important;
  top: 0 !important;
  left: 0 !important;
  margin: 0 !important;
  padding: 0 !important;
  display: flex !important;
  align-items: center !important;
  justify-content: center !important;
  overflow: hidden !important;
}

:deep(.v-dialog--fullscreen) {
  background: rgba(19, 17, 26, 0.95) !important;
}

:deep(.v-dialog--fullscreen > .v-card) {
  min-height: unset !important;
  height: auto !important;
  position: relative !important;
  margin: 16px !important;
  border-radius: 24px !important;
  background: rgba(19, 17, 26, 0.95) !important;
}

@media (max-width: 400px) {
  .fullscreen-card {
    width: calc(100% - 24px) !important;
    margin: 12px;
  }

  :deep(.v-toolbar) {
    height: 48px !important;
    padding: 0 4px !important;
  }

  :deep(.v-toolbar .v-btn) {
    width: 36px !important;
    height: 36px !important;
    min-width: 36px !important;
    margin: 6px !important;
  }

  :deep(.v-toolbar .v-icon) {
    font-size: 20px;
  }
}
</style> 