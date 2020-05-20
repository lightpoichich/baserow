import Vue from 'vue'
import axios from 'axios'
import _ from 'lodash'

import GridService from '@baserow/modules/database/services/view/grid'
import RowService from '@baserow/modules/database/services/row'

export function populateRow(row) {
  row._ = {
    loading: false,
    hover: false,
  }
  return row
}

export const state = () => ({
  loading: false,
  loaded: false,
  // The last used grid id.
  lastGridId: -1,
  // Contains the custom field options per view. Things like the field width are
  // stored here.
  fieldOptions: {},
  // Contains the buffered rows that we keep in memory. Depending on the
  // scrollOffset rows will be added or removed from this buffer. Most of the times,
  // it will contain 3 times the bufferRequestSize in rows.
  rows: [],
  // The total amount of rows in the table.
  count: 0,
  // The height of a single row.
  rowHeight: 33,
  // The distance to the top in pixels the visible rows should have.
  rowsTop: 0,
  // The amount of rows that must be visible above and under the middle row.
  rowPadding: 16,
  // The amount of rows that will be requested per request.
  bufferRequestSize: 40,
  // The start index of the buffer in the whole table.
  bufferStartIndex: 0,
  // The limit of the buffer measured from the start index in the whole table.
  bufferLimit: 0,
  // The start index of the visible rows of the rows in the buffer.
  rowsStartIndex: 0,
  // The end index of the visible rows of the rows buffer.
  rowsEndIndex: 0,
  // The last scrollTop when the visibleByScrollTop was called.
  scrollTop: 0,
  // The last windowHeight when the visibleByScrollTop was called.
  windowHeight: 0,
})

export const mutations = {
  SET_LOADING(state, value) {
    state.loading = value
  },
  SET_LOADED(state, value) {
    state.loaded = value
  },
  SET_LAST_GRID_ID(state, gridId) {
    state.lastGridId = gridId
  },
  SET_SCROLL_TOP(state, { scrollTop, windowHeight }) {
    state.scrollTop = scrollTop
    state.windowHeight = windowHeight
  },
  CLEAR_ROWS(state) {
    state.rows = []
    state.rowsTop = 0
    state.bufferStartIndex = 0
    state.bufferEndIndex = 0
    state.bufferLimit = 0
    state.rowsStartIndex = 0
    state.rowsEndIndex = 0
    state.scrollTop = 0
  },
  /**
   * It will add and remove rows to the state based on the provided values. For example
   * if prependToRows is a positive number that amount of the provided rows will be
   * added to the state. If that number is negative that amoun will be removed from
   * the state. Same goes for the appendToRows, only then it will be appended.
   */
  ADD_ROWS(
    state,
    { rows, prependToRows, appendToRows, count, bufferStartIndex, bufferLimit }
  ) {
    state.count = count
    state.bufferStartIndex = bufferStartIndex
    state.bufferLimit = bufferLimit

    if (prependToRows > 0) {
      state.rows = [...rows.slice(0, prependToRows), ...state.rows]
    }
    if (appendToRows > 0) {
      state.rows.push(...rows.slice(0, appendToRows))
    }

    if (prependToRows < 0) {
      state.rows = state.rows.splice(Math.abs(prependToRows))
    }
    if (appendToRows < 0) {
      state.rows = state.rows.splice(
        0,
        state.rows.length - Math.abs(appendToRows)
      )
    }
  },
  SET_ROWS_INDEX(state, { startIndex, endIndex, top }) {
    state.rowsStartIndex = startIndex
    state.rowsEndIndex = endIndex
    state.rowsTop = top
  },
  DELETE_ROW(state, id) {
    const index = state.rows.findIndex((item) => item.id === id)
    state.count--
    if (index !== -1) {
      state.bufferLimit--
      state.rows.splice(index, 1)
    }
  },
  FINALIZE_ROW(state, { index, id }) {
    state.rows[index].id = id
    state.rows[index]._.loading = false
  },
  SET_VALUE(state, { row, field, value }) {
    row[`field_${field.id}`] = value
  },
  UPDATE_ROWS(state, { rows }) {
    rows.forEach((newRow) => {
      const row = state.rows.find((row) => row.id === newRow.id)
      if (row !== undefined) {
        _.assign(row, newRow)
      }
    })
  },
  ADD_FIELD(state, { field, value }) {
    const name = `field_${field.id}`
    state.rows.forEach((row) => {
      // We have to use the Vue.set function here to make it reactive immediately.
      // If we don't do this the value in the field components of the grid and modal
      // don't have the correct value and will act strange.
      Vue.set(row, name, value)
    })
  },
  SET_ROW_LOADING(state, { row, value }) {
    row._.loading = value
  },
  REPLACE_ALL_FIELD_OPTIONS(state, fieldOptions) {
    state.fieldOptions = fieldOptions
  },
  SET_FIELD_OPTIONS_OF_FIELD(state, { fieldId, values }) {
    if (Object.prototype.hasOwnProperty.call(state.fieldOptions, fieldId)) {
      _.assign(state.fieldOptions[fieldId], values)
    } else {
      state.fieldOptions = _.assign({}, state.fieldOptions, {
        [fieldId]: values,
      })
    }
  },
  SET_ROW_HOVER(state, { row, value }) {
    row._.hover = value
  },
}

// Contains the timeout needed for the delayed delayed scroll top action.
let fireTimeout = null
// Contains a timestamp of the last fire of the related actions to the delayed
// scroll top action.
let lastFire = null
// Contains the
let lastScrollTop = null
let lastRequest = null
let lastRequestOffset = null
let lastRequestLimit = null
let lastSource = null

export const actions = {
  /**
   * This action calculates which rows we would like to have in the buffer based on
   * the scroll top offset and the window height. Based on that is calculates which
   * rows we need to fetch compared to what we already have. If we need to fetch
   * anything other then we already have or waiting for a new request will be made.
   */
  fetchByScrollTop(
    { commit, getters, dispatch },
    { gridId, scrollTop, windowHeight }
  ) {
    commit('SET_LAST_GRID_ID', gridId)

    // Calculate what the middle row index of the visible window based on the scroll
    // top.
    const middle = scrollTop + windowHeight / 2
    const countIndex = getters.getCount - 1
    const middleRowIndex = Math.min(
      Math.max(Math.ceil(middle / getters.getRowHeight) - 1, 0),
      countIndex
    )

    // Calculate the start and end index of the rows that are visible to the user in
    // the whole database.
    const visibleStartIndex = Math.max(
      middleRowIndex - getters.getRowPadding,
      0
    )
    const visibleEndIndex = Math.min(
      middleRowIndex + getters.getRowPadding,
      countIndex
    )

    // Calculate the start and end index of the buffer, which are the rows that we
    // load in the memory of the browser, based on all the rows in the database.
    const bufferRequestSize = getters.getBufferRequestSize
    const bufferStartIndex = Math.max(
      Math.ceil((visibleStartIndex - bufferRequestSize) / bufferRequestSize) *
        bufferRequestSize,
      0
    )
    const bufferEndIndex = Math.min(
      Math.ceil((visibleEndIndex + bufferRequestSize) / bufferRequestSize) *
        bufferRequestSize,
      getters.getCount
    )
    const bufferLimit = bufferEndIndex - bufferStartIndex

    // Determine if the user is scrolling up or down.
    const down =
      bufferStartIndex > getters.getBufferStartIndex ||
      bufferEndIndex > getters.getBufferEndIndex
    const up =
      bufferStartIndex < getters.getBufferStartIndex ||
      bufferEndIndex < getters.getBufferEndIndex

    let prependToBuffer = 0
    let appendToBuffer = 0
    let requestOffset = null
    let requestLimit = null

    // Calculate how many rows we want to add and remove from the current rows buffer in
    // the store if the buffer would transition to the desired state. Also the
    // request offset and limit are calculated for the next request based on what we
    // currently have in the buffer.
    if (down) {
      prependToBuffer = Math.max(
        -getters.getBufferLimit,
        getters.getBufferStartIndex - bufferStartIndex
      )
      appendToBuffer = Math.min(
        bufferLimit,
        bufferEndIndex - getters.getBufferEndIndex
      )
      requestOffset = Math.max(getters.getBufferEndIndex, bufferStartIndex)
      requestLimit = appendToBuffer
    } else if (up) {
      prependToBuffer = Math.min(
        bufferLimit,
        getters.getBufferStartIndex - bufferStartIndex
      )
      appendToBuffer = Math.max(
        -getters.getBufferLimit,
        bufferEndIndex - getters.getBufferEndIndex
      )
      requestOffset = Math.max(bufferStartIndex, 0)
      requestLimit = prependToBuffer
    }

    // Checks if we need to request anything and if there are any changes since the
    // last request we made. If so we need to initialize a new request.
    if (
      requestLimit > 0 &&
      (lastRequestOffset !== requestOffset || lastRequestLimit !== requestLimit)
    ) {
      // If another request is runnig we need to cancel that one because it won't
      // what we need at the moment.
      if (lastRequest !== null) {
        lastSource.cancel('Canceled in favor of new request')
      }

      // Doing the actual request and remember what we are requesting so we can compare
      // it when making a new request.
      lastRequestOffset = requestOffset
      lastRequestLimit = requestLimit
      lastSource = axios.CancelToken.source()
      lastRequest = GridService(this.$client)
        .fetchRows({
          gridId,
          offset: requestOffset,
          limit: requestLimit,
          cancelToken: lastSource.token,
        })
        .then(({ data }) => {
          data.results.forEach((part, index) => {
            populateRow(data.results[index])
          })
          commit('ADD_ROWS', {
            rows: data.results,
            prependToRows: prependToBuffer,
            appendToRows: appendToBuffer,
            count: data.count,
            bufferStartIndex,
            bufferLimit,
          })
          dispatch('visibleByScrollTop', {
            // Somehow we have to explicitly set these values to null.
            scrollTop: null,
            windowHeight: null,
          })
          lastRequest = null
        })
        .catch((error) => {
          if (!axios.isCancel(error)) {
            lastRequest = null
            throw error
          }
        })
    }
  },
  /**
   * Calculates which rows should be visible for the user based on the provided
   * scroll top and window height. Because we know what the padding above and below
   * the middle row should be and which rows we have in the buffer we can calculate
   * what the start and end index for the visible rows in the buffer should be.
   */
  visibleByScrollTop(
    { getters, commit },
    { scrollTop = null, windowHeight = null }
  ) {
    if (scrollTop !== null && windowHeight !== null) {
      commit('SET_SCROLL_TOP', { scrollTop, windowHeight })
    } else {
      scrollTop = getters.getScrollTop
      windowHeight = getters.getWindowHeight
    }

    const middle = scrollTop + windowHeight / 2
    const countIndex = getters.getCount - 1

    const middleRowIndex = Math.min(
      Math.max(Math.ceil(middle / getters.getRowHeight) - 1, 0),
      countIndex
    )

    // Calculate the start and end index of the rows that are visible to the user in
    // the whole table.
    const visibleStartIndex = Math.max(
      middleRowIndex - getters.getRowPadding,
      0
    )
    const visibleEndIndex = Math.min(
      middleRowIndex + getters.getRowPadding + 1,
      getters.getCount
    )

    // Calculate the start and end index of the buffered rows that are visible for
    // the user.
    const visibleRowStartIndex =
      Math.min(
        Math.max(visibleStartIndex, getters.getBufferStartIndex),
        getters.getBufferEndIndex
      ) - getters.getBufferStartIndex
    const visibleRowEndIndex =
      Math.max(
        Math.min(visibleEndIndex, getters.getBufferEndIndex),
        getters.getBufferStartIndex
      ) - getters.getBufferStartIndex

    // Calculate the top position of the html element that contains all the rows.
    // This element will be placed over the placeholder the correct position of
    // those rows.
    const top =
      Math.min(visibleStartIndex, getters.getBufferEndIndex) *
      getters.getRowHeight

    // If the index changes from what we already have we can commit the new indexes
    // to the state.
    if (
      visibleRowStartIndex !== getters.getRowsStartIndex ||
      visibleRowEndIndex !== getters.getRowsEndIndex ||
      top !== getters.getRowsTop
    ) {
      commit('SET_ROWS_INDEX', {
        startIndex: visibleRowStartIndex,
        endIndex: visibleRowEndIndex,
        top,
      })
    }
  },
  /**
   * This action is called every time the users scrolls which might result in a lot
   * of calls. Therefore it will dispatch the related actions, but only every 100
   * milliseconds to prevent calling the actions who do a lot of calculating a lot.
   */
  fetchByScrollTopDelayed({ dispatch }, { gridId, scrollTop, windowHeight }) {
    const fire = (scrollTop, windowHeight) => {
      lastFire = new Date().getTime()
      if (scrollTop === lastScrollTop) {
        return
      }
      lastScrollTop = scrollTop
      dispatch('fetchByScrollTop', { gridId, scrollTop, windowHeight })
      dispatch('visibleByScrollTop', { scrollTop, windowHeight })
    }

    const difference = new Date().getTime() - lastFire
    if (difference > 100) {
      clearTimeout(fireTimeout)
      fire(scrollTop, windowHeight)
    } else {
      clearTimeout(fireTimeout)
      fireTimeout = setTimeout(() => {
        fire(scrollTop, windowHeight)
      }, 100)
    }
  },
  /**
   * Fetches an initial set of rows and adds that data to the store.
   */
  async fetchInitial({ dispatch, commit, getters }, { gridId }) {
    commit('SET_LAST_GRID_ID', gridId)
    commit('CLEAR_ROWS')

    const limit = getters.getBufferRequestSize * 2
    const { data } = await GridService(this.$client).fetchRows({
      gridId,
      offset: 0,
      limit,
      includeFieldOptions: true,
    })
    data.results.forEach((part, index) => {
      populateRow(data.results[index])
    })
    commit('ADD_ROWS', {
      rows: data.results,
      prependToRows: 0,
      appendToRows: data.results.length,
      count: data.count,
      bufferStartIndex: 0,
      bufferLimit: data.count > limit ? limit : data.count,
    })
    commit('SET_ROWS_INDEX', {
      startIndex: 0,
      // @TODO mut calculate how many rows would fit and based on that calculate
      // what the end index should be.
      endIndex: data.count > 31 ? 31 : data.count,
      top: 0,
    })
    commit('REPLACE_ALL_FIELD_OPTIONS', data.field_options)
  },
  /**
   * Updates a grid view field value. It will immediately be updated in the store
   * and only if the change request fails it will reverted to give a faster
   * experience for the user.
   */
  updateValue({ commit, dispatch }, { table, row, field, value, oldValue }) {
    commit('SET_VALUE', { row, field, value })

    const values = {}
    values[`field_${field.id}`] = value
    return RowService(this.$client)
      .update(table.id, row.id, values)
      .catch((error) => {
        commit('SET_VALUE', { row, field, value: oldValue })
        throw error
      })
  },
  /**
   * Creates a new row. Based on the default values of the fields a row is created
   * which will be added to the store. Only if the request fails the row is @TODO
   * removed.
   */
  async create(
    { commit, getters, rootGetters, dispatch },
    { table, fields, values = {} }
  ) {
    // Fill the not provided values with the empty value of the field type so we can
    // immediately commit the created row to the state.
    fields.forEach((field) => {
      const name = `field_${field.id}`
      if (!(name in values)) {
        const fieldType = this.$registry.get('field', field._.type.type)
        const empty = fieldType.getEmptyValue(field)
        values[name] = empty
      }
    })

    // Populate the row and set the loading state to indicate that the row has not
    // yet been added.
    const row = _.assign({}, values)
    populateRow(row)
    row.id = 0
    row._.loading = true

    commit('ADD_ROWS', {
      rows: [row],
      prependToRows: 0,
      appendToRows: 1,
      count: getters.getCount + 1,
      bufferStartIndex: getters.getBufferStartIndex,
      bufferLimit: getters.getBufferLimit + 1,
    })
    dispatch('visibleByScrollTop', {
      scrollTop: null,
      windowHeight: null,
    })
    const index = getters.getRowsLength - 1

    // @TODO remove the correct row is the request fails.
    const { data } = await RowService(this.$client).create(table.id, values)
    commit('FINALIZE_ROW', { index, id: data.id })
  },
  /**
   * Deletes an existing row of the provided table. After deleting, the visible rows
   * range and the buffer are recalculated because we might need to show different
   * rows or add some rows to the buffer.
   */
  async delete(
    { commit, dispatch, getters },
    { table, grid, row, getScrollTop }
  ) {
    commit('SET_ROW_LOADING', { row, value: true })

    try {
      await RowService(this.$client).delete(table.id, row.id)
      commit('DELETE_ROW', row.id)

      // We use the provided function to recalculate the scrollTop offset in order
      // to get fresh data.
      const scrollTop = getScrollTop()
      const windowHeight = getters.getWindowHeight

      dispatch('fetchByScrollTop', {
        gridId: grid.id,
        scrollTop,
        windowHeight,
      })
      dispatch('visibleByScrollTop', { scrollTop, windowHeight })
    } catch (error) {
      commit('SET_ROW_LOADING', { row, value: false })
      throw error
    }
  },
  /**
   * Adds a field with a provided value to the rows in memory.
   */
  addField({ commit }, { field, value = null }) {
    commit('ADD_FIELD', { field, value })
  },
  /**
   * Updates the field options of a given field and also makes an API request to the
   * backend with the changed values. If the request fails the action is reverted.
   */
  async updateFieldOptionsOfField(
    { commit },
    { gridId, field, values, oldValues }
  ) {
    commit('SET_FIELD_OPTIONS_OF_FIELD', {
      fieldId: field.id,
      values,
    })
    const updateValues = { field_options: {} }
    updateValues.field_options[field.id] = values

    try {
      await GridService(this.$client).update({ gridId, values: updateValues })
    } catch (error) {
      commit('SET_FIELD_OPTIONS_OF_FIELD', {
        fieldId: field.id,
        values: oldValues,
      })
      throw error
    }
  },
  /**
   * Updates the field options of a given field in the store. So no API request to
   * the backend is made.
   */
  setFieldOptionsOfField({ commit }, { field, values }) {
    commit('SET_FIELD_OPTIONS_OF_FIELD', {
      fieldId: field.id,
      values,
    })
  },
  setRowHover({ commit }, { row, value }) {
    commit('SET_ROW_HOVER', { row, value })
  },
  /**
   * Refreshes all the buffered data values of a given field. The new values are
   * requested from the backend and replaced.
   */
  async refreshFieldValues({ commit, getters }, { field }) {
    const rowIds = getters.getAllRows.map((row) => row.id)
    const fieldIds = [field.id]
    const gridId = getters.getLastGridId

    const { data } = await GridService(this.$client).filterRows({
      gridId,
      rowIds,
      fieldIds,
    })
    commit('UPDATE_ROWS', { rows: data })
  },
}

export const getters = {
  isLoading(state) {
    return state.loading
  },
  isLoaded(state) {
    return state.loaded
  },
  getLastGridId(state) {
    return state.lastGridId
  },
  getCount(state) {
    return state.count
  },
  getRowHeight(state) {
    return state.rowHeight
  },
  getRowsTop(state) {
    return state.rowsTop
  },
  getRowsLength(state) {
    return state.rows.length
  },
  getPlaceholderHeight(state) {
    return state.count * state.rowHeight
  },
  getRowPadding(state) {
    return state.rowPadding
  },
  getAllRows(state) {
    return state.rows
  },
  getRows(state) {
    return state.rows.slice(state.rowsStartIndex, state.rowsEndIndex)
  },
  getRowsStartIndex(state) {
    return state.rowsStartIndex
  },
  getRowsEndIndex(state) {
    return state.rowsEndIndex
  },
  getBufferRequestSize(state) {
    return state.bufferRequestSize
  },
  getBufferStartIndex(state) {
    return state.bufferStartIndex
  },
  getBufferEndIndex(state) {
    return state.bufferStartIndex + state.bufferLimit
  },
  getBufferLimit(state) {
    return state.bufferLimit
  },
  getScrollTop(state) {
    return state.scrollTop
  },
  getWindowHeight(state) {
    return state.windowHeight
  },
  getAllFieldOptions(state) {
    return state.fieldOptions
  },
}

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations,
}
