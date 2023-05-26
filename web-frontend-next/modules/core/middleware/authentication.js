import {
  getTokenIfEnoughTimeLeft,
  setToken,
} from "@baserow/modules/core/utils/auth";

export default defineNuxtRouteMiddleware((to) => {
  const nuxtApp = useNuxtApp();
  const route = useRoute();
  // If nuxt generate or already authenticated, pass this middleware
  if (process.server || nuxtApp.$store.getters["auth/isAuthenticated"]) return;

  // token can be in the query string (SSO) or in the cookies (previous session)
  let refreshToken = route.params.token;
  if (refreshToken) {
    setToken(refreshToken);
  } else {
    refreshToken = getTokenIfEnoughTimeLeft();
  }

  if (refreshToken) {
    return nuxtApp.$store
      .dispatch("auth/refresh", refreshToken)
      .catch((error) => {
        if (error.response?.status === 401) {
          return redirect({ name: "login" });
        }
      });
  }
});
