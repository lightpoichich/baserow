/**
 * This middleware makes sure the settings are fetched and available in the store.
 */
export default defineNuxtRouteMiddleware(async (to, from) => {
  const nuxtApp = useNuxtApp();
  // If nuxt generate, pass this middleware
  if (process.server) return;

  if (!nuxtApp.$store.getters["settings/isLoaded"]) {
    await nuxtApp.$store.dispatch("settings/load");
  }
});
