import { Application } from '@/core/applications'
import ApplicationService from '@/services/application'
import { setGroupCookie } from '@/utils/group'
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
  items: [],
  selectedGroup: {}
})

export const mutations = {
  REGISTER(state, application) {
    state.applications[application.type] = application
  },
  SET_SELECTED_GROUP(state, group) {
    state.selectedGroup = group
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
   * Choose an existing group. It will fetch all the applications of that group,
   * sets a cookie so the next time the page loads the group is still selected
   * and populates each item.
   */
  selectGroup({ commit, getters, dispatch }, group) {
    commit('SET_LOADING', true)

    return ApplicationService.fetchAll(group.id)
      .then(({ data }) => {
        commit('SET_SELECTED_GROUP', group)
        setGroupCookie(group.id, this.app.$cookies)

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
          'Unable to select group',
          "You're unable to select the group. This could be because you're not part of the group."
        )
      })
      .then(() => {
        commit('SET_LOADING', false)
      })
  },
  /**
   * If a selected group is deleted or for example the user logs off the current
   * group must be unselected which means that all the fetched items will be
   * forgotten.
   */
  unselectGroup({ commit }) {
    commit('SET_SELECTED_GROUP', {})
    commit('SET_ITEMS', [])
  },
  /**
   * Creates a new application with the given type and values for the currently
   * selected group.
   */
  create({ commit, getters, dispatch }, { type, values }) {
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
    return ApplicationService.create(getters.selectedGroupId, values)
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
  update({ commit, dispatch }, { id, values }) {
    return ApplicationService.update(id, values)
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
  delete({ commit, dispatch }, id) {
    return ApplicationService.delete(id)
      .then(() => {
        commit('DELETE_ITEM', id)
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
  selectedGroupId(state) {
    return state.selectedGroup.id
  },
  hasSelectedGroup(state) {
    return state.selectedGroup.hasOwnProperty('id')
  },
  applications(state) {
    return state.applications
  },
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
