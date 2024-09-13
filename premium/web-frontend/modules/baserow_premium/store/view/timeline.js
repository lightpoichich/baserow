import bufferedRows from '@baserow/modules/database/store/view/bufferedRows'
import fieldOptions from '@baserow/modules/database/store/view/fieldOptions'
import TimelineService from '@baserow_premium/services/views/timeline'

export function populateRow(row, metadata = {}) {
  row._ = {
    metadata,
    dragging: false,
  }
  return row
}

const timelineBufferedRows = bufferedRows({
  service: TimelineService,
  populateRow,
})

const timelineFieldOptions = fieldOptions()

export const state = () => ({
  startDateFieldId: null,
  endDateFieldId: null,
  ...timelineBufferedRows.state(),
  ...timelineFieldOptions.state(),
})

export const mutations = {
  ...timelineBufferedRows.mutations,
  ...timelineFieldOptions.mutations,
  SET_START_FIELD_ID(state, startDateFieldId ) {
    state.startDateFieldId = startDateFieldId
  },
  SET_END_FIELD_ID(state, endDateFieldId ) {
    state.endDateFieldId = endDateFieldId
  },
  SET_TITLE_FIELD_ID(state, titleFieldId ) {
    state.titleFieldId = titleFieldId
  }
}

export const actions = {
  ...timelineBufferedRows.actions,
  ...timelineFieldOptions.actions,
  async fetchInitial({ dispatch, commit, rootGetters }, { viewId, fields }) {
    const view = rootGetters['view/get'](viewId)
    commit('SET_START_FIELD_ID', view.start_date_field)
    commit('SET_END_FIELD_ID', view.end_date_field)

    const data = await dispatch('fetchInitialRows', {
      viewId,
      fields,
      initialRowArguments: { includeFieldOptions: true },
    })
    await dispatch('forceUpdateAllFieldOptions', data.field_options)
    

  },
}

export const getters = {
  ...timelineBufferedRows.getters,
  ...timelineFieldOptions.getters,
}

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations,
}
