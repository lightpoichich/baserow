import RowCommentService from '@baserow_premium/services/row_comments/row_comments'
import _ from 'lodash'
import Vue from 'vue'

export const state = () => ({
  comments: [],
  seenComments: {},
  postingComment: false,
  loading: false,
  loaded: false,
  currentCount: 0,
  totalCount: 0,
  loadedRowId: false,
  loadedTableId: false,
})

export const mutations = {
  ADD_ROW_COMMENTS(state, comments) {
    comments.forEach((comment) => {
      const existingCommentLocation = state.seenComments[comment.id]
      const insertLocation = _.sortedIndexBy(
        state.comments,
        comment,
        (c) => -c.id
      )
      state.comments.splice(insertLocation, 0, comment)
      if (existingCommentLocation) {
        // We received an updated comment and inserted the new version above, now we
        // need to find the old version and delete it. It must be somewhere after the
        // new insert location as sortedIndexBy returns the lowest index which
        // preserves the sort order.
        const possibleDuplicateComment = state.comments[insertLocation + 1]
        if (possibleDuplicateComment.id === comment.id) {
          state.comments.splice(insertLocation, 1)
        }
      } else {
        Vue.set(state.seenComments, comment.id, true)
      }
    })
    state.currentCount = state.comments.length
  },
  REMOVE_ROW_COMMENT(state, comment) {
    const index = state.comments.findIndex((c) => c.id === comment)
    state.comments.splice(index, 1)
    Vue.unset(state.seenComments, comment.id)
  },
  RESET_ROW_COMMENTS(state) {
    state.comments = []
    state.seenComments = {}
  },
  SET_LOADING(state, loading) {
    state.loading = loading
  },
  SET_LOADED(state, loaded) {
    state.loaded = loaded
  },
  SET_LOADED_TABLE_AND_ROW(state, { tableId, rowId }) {
    state.loadedRowId = rowId
    state.loadedTableId = tableId
  },
  SET_POSTING_COMMENT(state, postingComment) {
    state.postingComment = postingComment
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
        rowId,
        {}
      )
      commit('RESET_ROW_COMMENTS')
      commit('ADD_ROW_COMMENTS', data.results)
      commit('SET_TOTAL_COUNT', data.count)
      commit('SET_LOADED', true)
    } finally {
      commit('SET_LOADING', false)
    }
  },
  async fetchNextSetOfComments(
    { dispatch, commit, getters, state },
    { tableId, rowId }
  ) {
    commit('SET_LOADING', true)
    try {
      // We have to use offset based paging here as new comments can be added by the
      // user or come in via realtime events.
      const { data } = await RowCommentService(this.$client).fetchAll(
        tableId,
        rowId,
        { offset: state.currentCount }
      )
      commit('ADD_ROW_COMMENTS', data.results)
      commit('SET_TOTAL_COUNT', data.count)
    } finally {
      commit('SET_LOADING', false)
    }
  },
  async postComment({ commit, state }, { tableId, rowId, comment }) {
    try {
      commit('SET_POSTING_COMMENT', true)
      const { data } = await RowCommentService(this.$client).create(
        tableId,
        rowId,
        comment
      )
      commit('ADD_ROW_COMMENTS', [data])
      commit('SET_TOTAL_COUNT', state.totalCount + 1)
    } finally {
      commit('SET_POSTING_COMMENT', false)
    }
  },
  forceAddRowComment({ commit }, { comment }) {
    commit('ADD_ROW_COMMENTS', [comment])
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
  getPostingComment(state) {
    return state.postingComment
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
