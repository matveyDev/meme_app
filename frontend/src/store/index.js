import { createStore } from 'vuex'

export default createStore({
  state: {
    memes: [],
    users: [],
    currentUser: null
  },
  mutations: {
    setMemes(state, memes) {
      state.memes = memes
    },
    setUsers(state, users) {
      state.users = users
    },
    setCurrentUser(state, user) {
      state.currentUser = user
    }
  },
  actions: {
    async fetchMemes({ commit }) {
      try {
        const response = await fetch('http://localhost:8000/api/mixeds/')
        const data = await response.json()
        commit('setMemes', data)
      } catch (error) {
        console.error('Error fetching memes:', error)
      }
    },
    async fetchUsers({ commit }) {
      try {
        const response = await fetch('http://localhost:8000/api/users/')
        const data = await response.json()
        commit('setUsers', data)
      } catch (error) {
        console.error('Error fetching users:', error)
      }
    }
  }
}) 