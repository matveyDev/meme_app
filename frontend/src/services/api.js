import axios from 'axios';

const API_URL = 'http://127.0.0.1:8000/api';

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/json'
  },
  withCredentials: false
});

export const mixService = {
  async getMixes() {
    try {
      const response = await api.get('/mixeds/');
      return response.data;
    } catch (error) {
      console.error('Error fetching mixes:', error);
      throw error;
    }
  },

  async updateMix(id, data) {
    try {
      const response = await api.put(`/mixeds/${id}`, data);
      return response.data;
    } catch (error) {
      console.error('Error updating mix:', error);
      throw error;
    }
  }
};

export default api; 