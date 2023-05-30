import { isSecureURL } from "./string";
import jwtDecode from "jwt-decode";

const cookieTokenName = "jwt_token";

export const setToken = (token, key = cookieTokenName) => {
  if (process.SERVER_BUILD) return;
  const runtimeConfig = useRuntimeConfig();
  const secure = isSecureURL(runtimeConfig.public.publicWebFrontendUrl);

  const cookie = useCookie(key, {
    path: "/",
    maxAge: 60 * 60 * 24 * 7,
    sameSite: "lax",
    secure,
  });

  cookie.value = token;
};

export const unsetToken = (key = cookieTokenName) => {
  if (process.SERVER_BUILD) return;
  const cookie = useCookie(key);
  cookie.value = null;
};

export const getToken = (key = cookieTokenName) => {
  const cookie = useCookie(key);
  return cookie.value;
};

export const getTokenIfEnoughTimeLeft = (key = cookieTokenName) => {
  const token = getToken(key);
  const now = Math.ceil(new Date().getTime() / 1000);
  let data;
  try {
    data = jwtDecode(token);
  } catch (error) {
    return null;
  }

  // Return the token if it is still valid for more of the 10% of the lifespan.
  return data && (data.exp - now) / (data.exp - data.iat) > 0.1 ? token : null;
};

export const logoutAndRedirectToLogin = (
  router,
  store,
  showSessionExpiredNotification = false
) => {
  store.dispatch("auth/logoff");
  router.push({ name: "login", query: { noredirect: null } }, () => {
    if (showSessionExpiredNotification) {
      store.dispatch("notification/setUserSessionExpired", true);
    }
    store.dispatch("auth/clearAllStoreUserData");
  });
};
