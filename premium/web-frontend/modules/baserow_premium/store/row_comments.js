import RowCommentService from '@baserow_premium/services/row_comments/row_comments'

export const state = () => ({
  comments: [],
  loading: false,
  loaded: false,
})

export const mutations = {
  ADD_ROW_COMMENT(state, comment) {
    state.comments.push(comment)
  },
  REMOVE_ROW_COMMENT(state, comment) {
    const index = state.comments.findIndex((c) => c.id === comment)
    state.comments.splice(index, 1)
  },
  REPLACE_ALL_ROW_COMMENTS(state, comments) {
    state.comments = comments
  },
  SET_LOADING(state, loading) {
    state.loading = loading
  },
  SET_LOADED(state, loaded) {
    state.loaded = loaded
  },
}

export const actions = {
  async fetchRowComments({ dispatch, commit, getters }, { tableId, rowId }) {
    commit('SET_LOADING', true)
    commit('SET_LOADED', false)
    try {
      const { data } = await RowCommentService(this.$client).fetchAll(
        tableId,
        rowId
      )
      commit('REPLACE_ALL_ROW_COMMENTS', data.results)
      commit('SET_LOADED', true)
    } finally {
      commit('SET_LOADING', false)
    }
  },
  async postComment({ commit }, { tableId, rowId, comment }) {
    const { data } = await RowCommentService(this.$client).create(
      tableId,
      rowId,
      comment
    )
    commit('ADD_ROW_COMMENT', data)
  },
  forceAddRowComment({ commit }, { comment }) {
    commit('ADD_ROW_COMMENT', {
      comment,
    })
  },
}

export const getters = {
  getRowComments(state) {
    return state.comments
  },
  getLoading(state) {
    return state.loading
  },
  getLoaded(state) {
    return state.loaded
  },
}

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations,
}
