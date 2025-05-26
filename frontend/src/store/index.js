import { createStore } from 'vuex'

export default createStore({
  state: {
    token: localStorage.getItem('access_token') || ''
  },
  mutations: {
    setToken(state, token) {
      state.token = token
      localStorage.setItem('access_token', token)
    },
    clearToken(state) {
      state.token = ''
      localStorage.removeItem('access_token')
    }
  }
})