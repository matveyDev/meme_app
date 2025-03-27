<template>
  <div class="leaderboard-item" @click="$emit('click')">
    <div class="rank" :class="{'top-rank': index < 3}">
      <span class="rank-number">#{{ index + 1 }}</span>
      <v-icon v-if="index === 0" color="#FFD700" class="rank-icon">mdi-crown</v-icon>
      <v-icon v-else-if="index === 1" color="#C0C0C0" class="rank-icon">mdi-crown</v-icon>
      <v-icon v-else-if="index === 2" color="#CD7F32" class="rank-icon">mdi-crown</v-icon>
    </div>
    <div class="meme-info">
      <div class="image-container">
        <img 
          :src="mix.image" 
          :alt="mix.name"
          class="meme-thumbnail"
          @error="handleImageError"
        >
      </div>
      <div class="meme-details">
        <h3>{{ mix.name }}</h3>
        <div class="points">
          <span class="points-value">{{ Math.round(mix.points) }}</span>
          <span class="points-label">points</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'LeaderboardItem',
  props: {
    mix: {
      type: Object,
      required: true
    },
    index: {
      type: Number,
      required: true
    },
    fallbackImage: {
      type: String,
      default: 'path/to/fallback/image.jpg'
    }
  },
  methods: {
    handleImageError(e) {
      e.target.src = this.fallbackImage;
    }
  }
}
</script>

<style scoped>
.leaderboard-item {
  display: flex;
  align-items: center;
  padding: 16px;
  border-bottom: 1px solid rgba(139, 92, 246, 0.2);
  transition: transform 0.2s ease, background-color 0.2s ease;
  cursor: pointer;
}

.leaderboard-item:hover {
  background-color: rgba(139, 92, 246, 0.1);
  transform: translateX(4px);
}

.leaderboard-item:last-child {
  border-bottom: none;
}

.rank {
  display: flex;
  flex-direction: column;
  align-items: center;
  font-size: 1.5rem;
  font-weight: 600;
  color: #8B5CF6;
  width: 60px;
  text-align: center;
}

.rank-number {
  margin-bottom: 4px;
}

.rank-icon {
  font-size: 1.2rem;
}

.rank.top-rank {
  font-size: 1.8rem;
  text-shadow: 0 0 10px rgba(245, 158, 11, 0.3);
}

.rank.top-rank .rank-icon {
  font-size: 1.4rem;
  margin-top: 4px;
}

.meme-info {
  display: flex;
  align-items: center;
  flex: 1;
}

.image-container {
  position: relative;
  width: 80px;
  height: 80px;
  margin-right: 16px;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.meme-thumbnail {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.3s ease;
}

.image-container:hover .meme-thumbnail {
  transform: scale(1.1);
}

.meme-details {
  flex: 1;
}

.meme-details h3 {
  font-size: 1.2rem;
  margin: 0 0 8px 0;
  color: white;
  font-weight: 600;
}

.points {
  display: flex;
  align-items: baseline;
  gap: 4px;
}

.points-value {
  font-size: 1.2rem;
  font-weight: 600;
  color: #8B5CF6;
}

.points-label {
  font-size: 0.9rem;
  color: rgba(255, 255, 255, 0.6);
}

@media (max-width: 600px) {
  .rank {
    font-size: 1.2rem;
    width: 40px;
  }

  .rank.top-rank {
    font-size: 1.4rem;
  }

  .image-container {
    width: 60px;
    height: 60px;
    margin-right: 12px;
  }

  .meme-details h3 {
    font-size: 1rem;
    margin-bottom: 4px;
  }

  .points-value {
    font-size: 1rem;
  }

  .points-label {
    font-size: 0.8rem;
  }

  .rank-icon {
    font-size: 1rem;
  }

  .rank.top-rank .rank-icon {
    font-size: 1.2rem;
  }
}
</style> 