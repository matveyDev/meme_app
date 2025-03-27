<template>
  <v-dialog :value="show" @input="$emit('update:show', $event)" max-width="500px">
    <v-card class="vote-dialog">
      <v-card-title class="dialog-title">
        {{ mix?.name }}
        <v-btn
          icon
          class="close-btn"
          @click="close"
        >
          <v-icon color="#8B5CF6">mdi-close</v-icon>
        </v-btn>
      </v-card-title>
      <v-card-text>
        <div class="vote-preview">
          <img :src="mix?.image" :alt="mix?.name" class="vote-image">
        </div>
        <v-text-field
          v-model="points"
          label="Points"
          type="number"
          :rules="[v => !!v || 'Points are required']"
          class="mt-4 vote-input"
          color="#8B5CF6"
          dark
        ></v-text-field>
      </v-card-text>
      <v-card-actions class="vote-actions">
        <v-spacer></v-spacer>
        <v-btn
          class="cancel-btn"
          text
          @click="close"
        >
          Cancel
        </v-btn>
        <v-btn
          class="submit-btn"
          :loading="loading"
          :disabled="!points"
          @click="submit"
        >
          Submit Vote
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
export default {
  name: 'VoteDialog',
  props: {
    show: {
      type: Boolean,
      required: true
    },
    mix: {
      type: Object,
      required: true
    },
    loading: {
      type: Boolean,
      default: false
    }
  },
  data() {
    return {
      points: ''
    }
  },
  methods: {
    close() {
      this.$emit('update:show', false);
      this.points = '';
    },
    submit() {
      this.$emit('submit', this.points);
      this.points = '';
    }
  }
}
</script>

<style scoped>
.vote-dialog {
  background: #1E1B24;
  color: white;
  border: 1px solid rgba(139, 92, 246, 0.3);
  box-shadow: 0 0 20px rgba(139, 92, 246, 0.2);
}

.dialog-title {
  position: relative;
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 24px;
  font-weight: 700;
  color: white;
  padding: 16px 24px;
  background: linear-gradient(135deg, #8B5CF6 0%, #6D28D9 100%);
  text-align: center;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
}

.close-btn {
  position: absolute;
  right: 8px;
  top: 50%;
  transform: translateY(-50%);
  transition: all 0.3s ease;
}

.close-btn:hover {
  transform: translateY(-50%) scale(1.1);
  background-color: rgba(255, 255, 255, 0.1);
}

.close-btn .v-icon {
  font-size: 24px;
}

.vote-preview {
  width: 100%;
  aspect-ratio: 1;
  border-radius: 8px;
  overflow: hidden;
  margin-top: 16px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
  border: 1px solid rgba(139, 92, 246, 0.2);
}

.vote-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.vote-input {
  margin-top: 24px !important;
}

.vote-input :deep(.v-label) {
  color: rgba(255, 255, 255, 0.9) !important;
}

.vote-input :deep(.v-input__slot) {
  border-color: rgba(139, 92, 246, 0.3) !important;
}

.vote-input :deep(.v-input__slot:hover) {
  border-color: rgba(139, 92, 246, 0.5) !important;
}

.vote-actions {
  padding: 16px 24px;
  background: rgba(139, 92, 246, 0.05);
  border-top: 1px solid rgba(139, 92, 246, 0.2);
}

.cancel-btn {
  color: rgba(255, 255, 255, 0.8) !important;
  font-weight: 500;
  margin-right: 12px;
  text-transform: none;
  letter-spacing: 0.5px;
}

.cancel-btn:hover {
  color: white !important;
  background: rgba(255, 255, 255, 0.1);
}

.submit-btn {
  background: linear-gradient(45deg, #8B5CF6, #9333EA) !important;
  color: white !important;
  font-weight: 600;
  padding: 0 24px !important;
  height: 40px;
  text-transform: none;
  letter-spacing: 0.5px;
  border: none;
  box-shadow: 0 4px 10px rgba(139, 92, 246, 0.3);
}

.submit-btn:hover {
  background: linear-gradient(45deg, #9333EA, #8B5CF6) !important;
  box-shadow: 0 4px 15px rgba(139, 92, 246, 0.4);
  transform: translateY(-1px);
}

.submit-btn:disabled {
  background: rgba(139, 92, 246, 0.3) !important;
  color: rgba(255, 255, 255, 0.5) !important;
  box-shadow: none;
}

@media (max-width: 600px) {
  .vote-preview {
    aspect-ratio: 1;
  }

  .vote-dialog .dialog-title {
    font-size: 1.3rem;
    padding: 16px;
  }

  .vote-actions {
    padding: 12px 16px;
  }

  .submit-btn {
    padding: 0 16px !important;
    height: 36px;
  }
}
</style> 