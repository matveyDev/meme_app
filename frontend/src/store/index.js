import { createStore } from 'vuex'
import { API_URL } from '@/config'

export default createStore({
  state: {
    mixeds: [],
    users: [],
    currentUser: null
  },
  mutations: {
    SET_MIXEDS(state, mixeds) {
      state.mixeds = mixeds
    },
    SET_USERS(state, users) {
      state.users = users
    },
    setCurrentUser(state, user) {
      state.currentUser = user
    }
  },
  actions: {
    async fetchMixeds({ commit }) {
      try {
        const response = await fetch(`${API_URL}/api/mixeds/`)
        const data = await response.json()
        commit('SET_MIXEDS', data)
      } catch (error) {
        console.error('Error fetching mixeds:', error)
      }
    },
    async fetchUsers({ commit }) {
      try {
        const response = await fetch(`${API_URL}/api/users/`)
        const data = await response.json()
        commit('SET_USERS', data)
      } catch (error) {
        console.error('Error fetching users:', error)
      }
    }
  }
}) 