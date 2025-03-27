<template>
  <div class="merge-animation" :class="{ 'show': show }">
    <div class="merge-container">
      <!-- Левая карточка (предмет) -->
      <div class="merge-card left-card" :style="{ backgroundImage: `url(${itemImage})` }">
        <div class="card-content">
          <v-img
            :src="itemImage"
            cover
            class="merge-image"
          ></v-img>
        </div>
      </div>

      <!-- Правая карточка (животное) -->
      <div class="merge-card right-card" :style="{ backgroundImage: `url(${animalImage})` }">
        <div class="card-content">
          <v-img
            :src="animalImage"
            cover
            class="merge-image"
          ></v-img>
        </div>
      </div>

      <!-- Центральная точка слияния -->
      <div class="merge-point"></div>

      <!-- Результирующее изображение -->
      <div class="result-image" :class="{ 'show': showResult }">
        <v-img
          :src="resultImage"
          cover
          class="merge-image"
        ></v-img>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'MergeAnimation',
  props: {
    show: {
      type: Boolean,
      default: false
    },
    itemImage: {
      type: String,
      required: true
    },
    animalImage: {
      type: String,
      required: true
    },
    resultImage: {
      type: String,
      required: true
    }
  },
  data() {
    return {
      showResult: false
    }
  },
  watch: {
    show(newVal) {
      if (newVal) {
        // Запускаем анимацию
        setTimeout(() => {
          this.showResult = true;
        }, 1000); // Показываем результат после завершения анимации слияния
      } else {
        this.showResult = false;
      }
    }
  }
}
</script>

<style scoped>
.merge-animation {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(19, 17, 26, 0.95);
  z-index: 1000;
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0;
  visibility: hidden;
  transition: opacity 0.3s ease, visibility 0.3s ease;
}

.merge-animation.show {
  opacity: 1;
  visibility: visible;
}

.merge-container {
  position: relative;
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
}

.merge-card {
  position: absolute;
  width: 120px;
  height: 120px;
  border-radius: 16px;
  overflow: hidden;
  background-size: cover;
  background-position: center;
  box-shadow: 0 0 20px rgba(139, 92, 246, 0.3);
  transition: all 0.8s cubic-bezier(0.4, 0, 0.2, 1);
}

.left-card {
  left: 50%;
  top: 50%;
  transform: translate(-200px, -50%);
  z-index: 2;
}

.right-card {
  right: 50%;
  top: 50%;
  transform: translate(200px, -50%);
  z-index: 2;
}

.merge-animation.show .left-card {
  transform: translate(-60px, -50%);
}

.merge-animation.show .right-card {
  transform: translate(60px, -50%);
}

.card-content {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.merge-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.merge-point {
  position: absolute;
  width: 20px;
  height: 20px;
  background: #8B5CF6;
  border-radius: 50%;
  left: 50%;
  top: 50%;
  transform: translate(-50%, -50%);
  z-index: 3;
  opacity: 0;
  transition: all 0.3s ease;
}

.merge-animation.show .merge-point {
  opacity: 1;
  animation: pulse 1s ease infinite;
}

.result-image {
  position: absolute;
  width: 200px;
  height: 200px;
  border-radius: 16px;
  overflow: hidden;
  opacity: 0;
  transform: scale(0.8);
  transition: all 0.5s ease;
  z-index: 1;
}

.result-image.show {
  opacity: 1;
  transform: scale(1);
}

@keyframes pulse {
  0% {
    transform: translate(-50%, -50%) scale(1);
    box-shadow: 0 0 0 0 rgba(139, 92, 246, 0.4);
  }
  70% {
    transform: translate(-50%, -50%) scale(1.2);
    box-shadow: 0 0 0 20px rgba(139, 92, 246, 0);
  }
  100% {
    transform: translate(-50%, -50%) scale(1);
    box-shadow: 0 0 0 0 rgba(139, 92, 246, 0);
  }
}

@media (max-width: 600px) {
  .merge-card {
    width: 100px;
    height: 100px;
  }

  .merge-animation.show .left-card {
    transform: translate(-50px, -50%);
  }

  .merge-animation.show .right-card {
    transform: translate(50px, -50%);
  }

  .result-image {
    width: 160px;
    height: 160px;
  }
}

@media (max-width: 400px) {
  .merge-card {
    width: 80px;
    height: 80px;
  }

  .merge-animation.show .left-card {
    transform: translate(-40px, -50%);
  }

  .merge-animation.show .right-card {
    transform: translate(40px, -50%);
  }

  .result-image {
    width: 140px;
    height: 140px;
  }
}
</style> 