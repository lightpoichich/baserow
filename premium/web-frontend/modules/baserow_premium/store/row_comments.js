import RowCommentService from '@baserow_premium/services/row_comments/row_comments'

export const state = () => ({
  comments: [],
  loading: false,
  loaded: false,
  currentCount: 0,
  totalCount: 0,
  currentPage: 1,
  loadedRowId: false,
  loadedTableId: false,
})

export const mutations = {
  ADD_ROW_COMMENT(state, comment) {
    state.comments.unshift(comment)
  },
  REMOVE_ROW_COMMENT(state, comment) {
    const index = state.comments.findIndex((c) => c.id === comment)
    state.comments.splice(index, 1)
  },
  REPLACE_ALL_ROW_COMMENTS(state, comments) {
    state.comments = comments
  },
  APPEND_ROW_COMMENTS(state, comments) {
    state.comments = state.comments.concat(comments)
  },
  SET_LOADING(state, loading) {
    state.loading = loading
  },
  SET_LOADED(state, loaded) {
    state.loaded = loaded
  },
  SET_CURRENT_COUNT(state, currentCount) {
    state.currentCount = currentCount
  },
  SET_CURRENT_PAGE(state, currentPage) {
    state.currentPage = currentPage
  },
  SET_TOTAL_COUNT(state, totalCount) {
    state.totalCount = totalCount
  },
}

export const actions = {
  async fetchRowComments(
    { dispatch, commit, getters, state },
    { tableId, rowId }
  ) {
    commit('SET_LOADING', true)
    commit('SET_LOADED', false)
    try {
      const { data } = await RowCommentService(this.$client).fetchAll(
        tableId,
        rowId
      )
      commit('REPLACE_ALL_ROW_COMMENTS', data.results)
      commit('SET_TOTAL_COUNT', data.count)
      commit('SET_CURRENT_COUNT', state.comments.length)
      commit('SET_LOADED', true)
      commit('SET_CURRENT_PAGE', 1)
    } finally {
      commit('SET_LOADING', false)
    }
  },
  async fetchPage({ dispatch, commit, getters, state }, { tableId, rowId }) {
    commit('SET_LOADING', true)
    try {
      const nextPage = state.page + 1
      const { data } = await RowCommentService(this.$client).fetchAll(
        tableId,
        rowId,
        nextPage
      )
      commit('APPEND_ROW_COMMENTS', data.results)
      commit('SET_TOTAL_COUNT', data.count)
      commit('SET_CURRENT_COUNT', state.comments.length)
      commit('SET_CURRENT_PAGE', nextPage)
    } finally {
      commit('SET_LOADING', false)
    }
  },
  async postComment({ commit, state }, { tableId, rowId, comment }) {
    const { data } = await RowCommentService(this.$client).create(
      tableId,
      rowId,
      comment
    )
    commit('ADD_ROW_COMMENT', data)
    commit('SET_TOTAL_COUNT', state.totalCount + 1)
    commit('SET_CURRENT_COUNT', state.currentCount + 1)
    commit('SET_CURRENT_PAGE', Math.floor(state.currentCount / 100) + 1)
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
  getCurrentCount(state) {
    return state.currentCount
  },
  getTotalCount(state) {
    return state.totalCount
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
