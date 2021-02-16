/**
 * This middleware makes sure the config is fetched and available in the store.
 */
export default async function ({ store, req }) {
  // If nuxt generate, pass this middleware
  if (process.server && !req) return

  if (!store.getters['config/isLoaded']) {
    await store.dispatch('config/load')
  }
}
