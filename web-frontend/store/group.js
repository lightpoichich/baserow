import GroupService from '@/services/group'

export const state = () => ({
  loaded: false,
  loading: false,
  items: []
})

export const mutations = {
  SET_LOADED(state, loaded) {
    state.loaded = loaded
  },
  SET_LOADING(state, loading) {
    state.loading = loading
  },
  SET_ITEMS(state, items) {
    state.items = items
  }
}

export const actions = {
  loadAll({ state, dispatch }) {
    if (!state.loaded && !state.loading) {
      dispatch('fetchAll')
    }
  },
  fetchAll({ commit }) {
    commit('SET_LOADING', true)

    return GroupService.fetchAll()
      .then(({ data }) => {
        commit('SET_LOADED', false)
        commit('SET_ITEMS', data)
      })
      .catch(() => {
        commit('SET_ITEMS', [])
      })
      .then(() => {
        commit('SET_LOADING', false)
      })
  }
}

export const getters = {
  isLoaded(state) {
    return state.loaded
  },
  isLoading(state) {
    return state.loading
  }
}
