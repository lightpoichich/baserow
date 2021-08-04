import RowCommentService from '@baserow_premium/services/row_comments/row_comments'
import _ from 'lodash'
import moment from 'moment'

export const state = () => ({
  comments: [],
  postingComment: false,
  loading: false,
  loaded: false,
  currentCount: 0,
  totalCount: 0,
  loadedRowId: false,
  loadedTableId: false,
})

export const mutations = {
  /**
   * Adds a list of comments to the existing comments, ensuring that the end result of
   * comments is an ordered list of comments descending by ID with no duplicate
   * comments. If a comment with the same id as an existing comment is provided in the
   * list the existing comment will be replaced by the new one.
   *
   * We want to handle duplicates here as comments received as realtime events could
   * potentially be also loaded in via a normal backend api fetch call.
   */
  ADD_ROW_COMMENTS(state, comments) {
    comments.forEach((newComment) => {
      const existingIndex = state.comments.findIndex(
        (c) => c.id === newComment.id
      )
      if (existingIndex >= 0) {
        // Prevent duplicates by just replacing them inline
        state.comments.splice(existingIndex, 0, newComment)
      } else {
        state.comments.push(newComment)
      }
    })
    state.currentCount = state.comments.length
  },
  RESET_ROW_COMMENTS(state) {
    state.comments = []
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
  /**
   * Fetches the initial row comments to display for a given table and row. Resets any
   * existing comments entirely.
   */
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
      commit('SET_LOADED_TABLE_AND_ROW', { tableId, rowId })
      commit('SET_LOADED', true)
    } finally {
      commit('SET_LOADING', false)
    }
  },
  /**
   * Fetches the next 10 comments from the server and adds them to the comments list.
   */
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
  /**
   * Posts a new comment to the server and updates the comments list once the server
   * responds with it's id and other related comment data.
   */
  async postComment({ commit, state, dispatch }, { tableId, rowId, comment }) {
    try {
      commit('SET_POSTING_COMMENT', true)
      const { data } = await RowCommentService(this.$client).create(
        tableId,
        rowId,
        comment
      )
      dispatch('forceCreate', { rowComment: data })
      return data
    } finally {
      commit('SET_POSTING_COMMENT', false)
    }
  },
  async forceCreate(context, { rowComment }) {
    const { commit, state } = context
    if (
      state.loadedTableId === rowComment.table &&
      state.loadedRowId === rowComment.row_id
    ) {
      commit('ADD_ROW_COMMENTS', [rowComment])
      commit('SET_TOTAL_COUNT', state.totalCount + 1)
    }
    // A new comment has been forcibly created so we need to let all views know that
    // the row comment count metadata should be incremented atomically.
    for (const viewType of Object.values(this.$registry.getAll('view'))) {
      await viewType.rowMetadataUpdated(
        { store: this },
        rowComment.table,
        rowComment.row_id,
        'row_comment_count',
        (count) => (count ? count + 1 : 1),
        'page/'
      )
    }
  },
}

export const getters = {
  getSortedRowComments(state) {
    return _.sortBy(state.comments, (c) => -moment.utc(c.created_on))
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
