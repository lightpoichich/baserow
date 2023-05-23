function isValidHttpUrl(rawString) {
  try {
    const url = new URL(rawString);
    return url.protocol === "http:" || url.protocol === "https:";
  } catch (_) {
    return false;
  }
}

function invalidUrlEnvVariable(envVariableName, nuxtApp) {
  /**
   * This function lets us check on startup that a provided environment variable is
   * a valid url. If we didn't do this then whenever the user would try to send a
   * HTTP request they would get a mysterious 500 error raised by the http client.
   *
   * @type {string}
   */

  const envValue = nuxtApp.runtimeConfig.public[envVariableName];
  return envValue && !isValidHttpUrl(envValue);
}
/**
 * This middleware makes sure that the current user is admin else a 403 error
 * will be shown to the user.
 *
 *
 */

export default defineNuxtRouteMiddleware(async (to, from) => {
  const nuxtApp = useNuxtApp();

  // If nuxt generate, pass this middleware
  if (process.server) return;

  if (
    process.server &&
    !nuxtApp.runtimeConfig.public.baserowDisablePublicUrlCheck
  ) {
    const urlEnvVarsToCheck = [];
    if (nuxtApp.runtimeConfig.public.baserowPublicUrl) {
      urlEnvVarsToCheck.push("baserowPublicUrl");
    } else {
      urlEnvVarsToCheck.push("publicBackendUrl", "publicWebFrontendUrl");
    }

    for (const name of urlEnvVarsToCheck) {
      if (invalidUrlEnvVariable(name, nuxtApp)) {
        // noinspection HttpUrlsUsage
        return error({
          statusCode: 500,
          hideBackButton: true,
          message: i18n.t("urlCheck.invalidUrlEnvVarTitle", { name }),
          content: i18n.t("urlCheck.invalidUrlEnvVarDescription", { name }),
        });
      }
    }
  }
});
