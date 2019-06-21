import AuthService from '@/services/authService.js'
import { client } from '@/services/client.js'

export const state = () => ({
  user: null
})

export const mutations = {
  SET_USER_DATA(state, data) {
    state.user = data
    localStorage.setItem('user', JSON.stringify(data))
    client.defaults.headers.common.Authorization = `JWT ${data.token}`
  },
  CLEAR_USER_DATA(state) {
    state.user = null
    localStorage.removeItem('user')
    client.defaults.headers.common.pop('Authorization')
  }
}

export const actions = {
  login({ commit, dispatch }, { email, password }) {
    return AuthService.login(email, password).then(({ data }) => {
      commit('SET_USER_DATA', data)
      dispatch('startRefreshTimeout')
    })
  },
  refresh({ commit, state, dispatch }) {
    return AuthService.refresh(state.user.token)
      .then(({ data }) => {
        commit('SET_USER_DATA', data)
        dispatch('startRefreshTimeout')
      })
      .catch(() => {
        // The token could not be refreshed, this means the token is no longer
        // valid and the user not logged in anymore.
        commit('CLEAR_USER_DATA')
      })
  },
  /**
   * Because the token expires within a configurable time, we need to keep
   * refreshing the token before that happens.
   */
  startRefreshTimeout({ dispatch }) {
    clearTimeout(this.refreshTimeout)
    this.refreshTimeout = setTimeout(() => {
      dispatch('refresh')
    }, (process.env.JWTTokenExpire - 2) * 1000)
  }
}

export const getters = {
  loggedIn(state) {
    return !!state.user
  }
}
