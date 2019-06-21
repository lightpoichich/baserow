export default function({ store }) {
  if (!process.browser) {
    return
  }

  const user = JSON.parse(localStorage.getItem('user'))
  if (user) {
    store.commit('auth/SET_USER_DATA', user)
    store.dispatch('auth/refresh')
  }
}
