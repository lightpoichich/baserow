import { Application } from '@/core/applications'
import ApplicationService from '@/services/application'
import { notify404, notifyError } from '@/utils/error'

function populateApplication(application, getters) {
  application._ = {
    type: getters.getApplicationByType(application.type).serialize(),
    loading: false
  }
  return application
}

export const state = () => ({
  applications: {},
  loading: false,
  items: []
})

export const mutations = {
  REGISTER(state, application) {
    state.applications[application.type] = application
  },
  SET_ITEMS(state, applications) {
    state.items = applications
  },
  SET_LOADING(state, value) {
    state.loading = value
  },
  SET_ITEM_LOADING(state, { application, value }) {
    application._.loading = value
  },
  ADD_ITEM(state, item) {
    state.items.push(item)
  },
  UPDATE_ITEM(state, values) {
    const index = state.items.findIndex(item => item.id === values.id)
    Object.assign(state.items[index], state.items[index], values)
  },
  DELETE_ITEM(state, id) {
    const index = state.items.findIndex(item => item.id === id)
    state.items.splice(index, 1)
  }
}

export const actions = {
  /**
   * Register a new application within the registry. The is commonly used when
   * creating an extension.
   */
  register({ commit }, application) {
    if (!(application instanceof Application)) {
      throw Error('The application must be an instance of Application.')
    }

    commit('REGISTER', application)
  },
  /**
   * Changes the loading state of a specific item.
   */
  setItemLoading({ commit }, { application, value }) {
    commit('SET_ITEM_LOADING', { application, value })
  },
  /**
   * Fetches all the applications of a given group. The is mostly called when
   * the user selects a different group.
   */
  fetchAll({ commit, getters, dispatch }, group) {
    commit('SET_LOADING', true)

    return ApplicationService.fetchAll(group.id)
      .then(({ data }) => {
        data.forEach((part, index, d) => {
          populateApplication(data[index], getters)
        })
        commit('SET_ITEMS', data)
      })
      .catch(error => {
        commit('SET_ITEMS', [])

        notify404(
          dispatch,
          error,
          'Unable to fetch applications',
          "You're unable to fetch the application of this group. " +
            "This could be because you're not part of the group."
        )
      })
      .then(() => {
        commit('SET_LOADING', false)
      })
  },
  /**
   * Clears all the currently selected applications, this could be called when
   * the group is deleted of when the user logs off.
   */
  clearAll({ commit }) {
    commit('SET_ITEMS', [])
  },
  /**
   * Creates a new application with the given type and values for the currently
   * selected group.
   */
  create({ commit, getters, rootGetters, dispatch }, { type, values }) {
    if (values.hasOwnProperty('type')) {
      throw new Error(
        'The key "type" is a reserved, but is already set on the ' +
          'values when creating a new application.'
      )
    }

    if (!getters.applicationTypeExists(type)) {
      throw new Error(`An application with type "${type}" doesn't exist.`)
    }

    values.type = type
    return ApplicationService.create(rootGetters['group/selectedId'], values)
      .then(({ data }) => {
        populateApplication(data, getters)
        commit('ADD_ITEM', data)
      })
      .catch(error => {
        notify404(
          dispatch,
          error,
          'Could not create application',
          "You're unable to create a new application for the selected " +
            "group. This could be because you're not part of the group."
        )
      })
  },
  /**
   * Updates the values of an existing application.
   */
  update({ commit, dispatch }, { application, values }) {
    return ApplicationService.update(application.id, values)
      .then(({ data }) => {
        commit('UPDATE_ITEM', data)
      })
      .catch(error => {
        notifyError(
          dispatch,
          error,
          'ERROR_USER_NOT_IN_GROUP',
          'Rename not allowed',
          "You're not allowed to rename the application because you're " +
            'not part of the group where the application is in.'
        )
      })
  },
  /**
   * Deletes an existing application.
   */
  delete({ commit, dispatch }, application) {
    return ApplicationService.delete(application.id)
      .then(() => {
        commit('DELETE_ITEM', application.id)
      })
      .catch(error => {
        notifyError(
          dispatch,
          error,
          'ERROR_USER_NOT_IN_GROUP',
          'Delete not allowed',
          "You're not allowed to rename the application because you're" +
            ' not part of the group where the application is in.'
        )
      })
  }
}

export const getters = {
  isLoading(state) {
    return state.loading
  },
  applicationTypeExists: state => type => {
    return state.applications.hasOwnProperty(type)
  },
  getApplicationByType: state => type => {
    if (!state.applications.hasOwnProperty(type)) {
      throw new Error(`An application with type "${type}" doesn't exist.`)
    }
    return state.applications[type]
  }
}
