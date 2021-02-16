import ConfigService from '@baserow/modules/core/services/config'
import { clone } from '@baserow/modules/core/utils/object'

export const state = () => ({
  loaded: false,
  config: {},
})

export const mutations = {
  SET_CONFIG(state, values) {
    state.config = values
  },
  UPDATE_CONFIG(state, values) {
    state.config = Object.assign({}, state.config, values)
  },
  SET_VALUE(state, key, value) {
    state.config[key] = value
  },
  SET_LOADED(state, value) {
    state.loaded = value
  },
}

export const actions = {
  async load({ commit }) {
    const { data } = await ConfigService(this.$client).get()
    commit('SET_CONFIG', data)
    commit('SET_LOADED', true)
  },
  async update({ commit, getters }, values) {
    const oldValues = clone(getters.get)
    commit('UPDATE_CONFIG', values)

    try {
      await ConfigService(this.$client).update(values)
    } catch (e) {
      commit('SET_CONFIG', oldValues)
      throw e
    }
  },
}

export const getters = {
  isLoaded(state) {
    return state.loaded
  },
  get(state) {
    return state.config
  },
}

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations,
}
