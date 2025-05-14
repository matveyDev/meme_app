import { defineStore } from 'pinia';
import axios from 'axios';
import { API_URL } from '@/config';

export const useGenerationStore = defineStore('generation', {
  state: () => ({
    canGenerate: false,
    usedGenerations: 0,
    limit: 0,
    isLoading: false,
    error: null
  }),

  actions: {
    async checkGenerationLimit(walletAddress) {
      try {
        this.isLoading = true;
        this.error = null;
        const response = await axios.post(`${API_URL}/can-generate`, {
          walletAddress
        });
        
        this.canGenerate = response.data.canGenerate;
        this.usedGenerations = response.data.usedGenerations;
        this.limit = response.data.limit;
      } catch (error) {
        console.error('Error checking generation limit:', error);
        this.error = error.response?.data?.detail || 'Failed to check generation limit';
      } finally {
        this.isLoading = false;
      }
    },

    async useGeneration(walletAddress) {
      try {
        this.isLoading = true;
        this.error = null;
        const response = await axios.post(`${API_URL}/use-generation`, {
          walletAddress
        });
        
        this.canGenerate = response.data.canGenerate;
        this.usedGenerations = response.data.usedGenerations;
        this.limit = response.data.limit;
      } catch (error) {
        console.error('Error using generation:', error);
        this.error = error.response?.data?.detail || 'Failed to use generation';
        throw error;
      } finally {
        this.isLoading = false;
      }
    }
  }
}); 