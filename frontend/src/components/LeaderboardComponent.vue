<template>
  <div class="leaderboard-container">
    <div class="leaderboard-content">
      <div v-if="loading" class="loading">
        <v-progress-circular indeterminate color="primary"></v-progress-circular>
        <span class="ml-3">Loading mixes...</span>
      </div>
      <div v-else-if="error" class="error">
        <v-icon color="error" class="mr-2">mdi-alert-circle</v-icon>
        {{ error }}
      </div>
      <div v-else-if="topMixes.length === 0" class="no-mixes">
        <v-icon color="grey" size="36" class="mb-2">mdi-emoticon-sad</v-icon>
        <p>No mixes found</p>
      </div>
      <div v-else>
        <leaderboard-item
          v-for="(mix, index) in topMixes"
          :key="mix.id"
          :mix="mix"
          :index="index"
          :fallback-image="fallbackImage"
          @click="openVoteDialog(mix)"
        />
      </div>
    </div>

    <vote-dialog
      v-model:show="showVoteDialog"
      :mix="selectedMix"
      :loading="voting"
      @submit="submitVote"
    />
  </div>
</template>

<script>
import { mixService } from '@/services/api';
import LeaderboardItem from './LeaderboardItem.vue';
import VoteDialog from './VoteDialog.vue';

export default {
  name: 'LeaderboardComponent',
  components: {
    LeaderboardItem,
    VoteDialog
  },
  data() {
    return {
      topMixes: [],
      loading: false,
      error: null,
      fallbackImage: 'path/to/fallback/image.jpg',
      showVoteDialog: false,
      selectedMix: null,
      voting: false
    }
  },
  methods: {
    openVoteDialog(mix) {
      this.selectedMix = mix;
      this.showVoteDialog = true;
    },
    closeVoteDialog() {
      this.showVoteDialog = false;
      this.selectedMix = null;
    },
    async submitVote(points) {
      if (!this.selectedMix || !points) return;

      this.voting = true;
      try {
        if (!this.selectedMix.name || !this.selectedMix.image || 
            !this.selectedMix.spice_id || !this.selectedMix.animal_slug_id || 
            !this.selectedMix.user_id) {
          throw new Error('Missing required fields in selected mix');
        }
        
        const updateData = {
          name: this.selectedMix.name,
          image: this.selectedMix.image,
          points: parseFloat(this.selectedMix.points) + parseFloat(points),
          spice_id: this.selectedMix.spice_id,
          animal_slug_id: this.selectedMix.animal_slug_id,
          user_id: this.selectedMix.user_id
        };

        await mixService.updateMix(this.selectedMix.id, updateData);

        // Обновляем данные в списке
        const index = this.topMixes.findIndex(m => m.id === this.selectedMix.id);
        if (index !== -1) {
          this.topMixes[index].points = parseFloat(this.topMixes[index].points) + parseFloat(points);
          // Пересортируем список
          this.topMixes.sort((a, b) => b.points - a.points);
        }

        this.$emit('vote-success', {
          message: `Successfully voted for ${this.selectedMix.name}!`,
          points: points
        });

        this.closeVoteDialog();
      } catch (error) {
        console.error('Error submitting vote:', error);
        this.error = 'Failed to submit vote. Please try again.';
      } finally {
        this.voting = false;
      }
    },
    async fetchTopMixes() {
      this.loading = true;
      this.error = null;
      
      try {
        const data = await mixService.getMixes();
        
        if (!Array.isArray(data)) {
          throw new Error('Invalid data format received from server');
        }

        this.topMixes = data
          .filter(mix => mix && mix.name && mix.spice_id && mix.animal_slug_id && mix.user_id)
          .sort((a, b) => b.points - a.points)
          .map(mix => ({
            id: mix.id,
            name: mix.name,
            image: mix.image || '',
            points: parseFloat(mix.points) || 0,
            spice_id: mix.spice_id,
            animal_slug_id: mix.animal_slug_id,
            user_id: mix.user_id
          }));
      } catch (error) {
        console.error('Error fetching top mixes:', error);
        this.error = error.message;
      } finally {
        this.loading = false;
      }
    }
  },
  async mounted() {
    await this.fetchTopMixes();
  }
}
</script>

<style scoped>
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
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
}

.no-mixes {
  padding: 32px;
  text-align: center;
  color: rgba(255, 255, 255, 0.6);
  font-size: 1.1rem;
}

.loading, .error {
  padding: 32px;
  text-align: center;
  font-size: 1.1rem;
}

.loading {
  color: rgba(255, 255, 255, 0.6);
}

.error {
  color: #EF4444;
}

@media (max-width: 600px) {
  .leaderboard-container {
    padding: 12px;
  }
}
</style> 