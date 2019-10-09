import { getGroupCookie, unsetGroupCookie } from '@/utils/group'

/**
 * This middleware is used to automatically fetch the groups and set a
 * selected group, which will automatically fetch the applications, if a group
 * id is stored as a cookie. This cookie will be set when selecting a group.
 */
export default function({ store, req, app }) {
  // If nuxt generate, pass this middleware
  if (process.server && !req) return

  // Get the selected group id
  const groupId = getGroupCookie(app.$cookies)

  // If a group id cookie is set, the user is authenticated and a selectedGroup
  // is not already set then we will fetch the groups and select that group.
  if (
    groupId &&
    store.getters['auth/isAuthenticated'] &&
    !store.getters['application/hasSelectedGroup']
  ) {
    return store
      .dispatch('group/fetchAll')
      .catch(() => {
        unsetGroupCookie(app.$cookies)
      })
      .then(() => {
        const group = store.getters['group/get'](groupId)
        if (group) {
          return store.dispatch('application/selectGroup', group)
        }
      })
  }
}
