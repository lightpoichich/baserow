import { isSecureURL } from "./string";

// NOTE: this has been deliberately left as `group`. A future task will rename it.
const cookieWorkspaceName = "baserow_group_id";

export const setWorkspaceCookie = (workspaceId) => {
  if (process.SERVER_BUILD) return;
  const runtimeConfig = useRuntimeConfig();
  const secure = isSecureURL(runtimeConfig.public.publicWebFrontendUrl);

  const cookie = useCookie(cookieWorkspaceName, {
    default: () => workspaceId,
    path: "/",
    maxAge: 60 * 60 * 24 * 7,
    sameSite: "lax",
    secure,
  });
};

export const unsetWorkspaceCookie = () => {
  if (process.SERVER_BUILD) return;
  const cookie = useCookie(cookieWorkspaceName);
  cookie.value = null;
};

export const getWorkspaceCookie = () => {
  if (process.SERVER_BUILD) return;
  const cookie = useCookie(cookieWorkspaceName);
  return cookie.value;
};
