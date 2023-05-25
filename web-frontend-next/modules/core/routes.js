import { resolve } from "pathe";

// Note that routes can't start with `/api/`, `/ws/` or `/media/` because they are
// reserved for the backend. In some cases, for example with the Heroku or Clouron
// deployment, the Baserow installation will share a single domain and port and then
// those URLS are forwarded to the backend or media files server. The rest is
// forwarded to the web-frontend.
export const routes = [
  {
    name: "index",
    path: "",
    file: resolve(__dirname, "./pages/index.vue"),
  },
  {
    name: "login",
    path: "/login",
    file: resolve(__dirname, "./pages/login.vue"),
  },
  {
    name: "signup",
    path: "/signup",
    file: resolve(__dirname, "./pages/signup.vue"),
  },
  {
    name: "forgot-password",
    path: "/forgot-password",
    file: resolve(__dirname, "./pages/forgotPassword.vue"),
  },
  // {
  //   name: "reset-password",
  //   path: "/reset-password/:token",
  //   file: resolve(__dirname, "./pages/resetPassword.vue"),
  // },
  {
    name: "dashboard",
    path: "/dashboard",
    file: resolve(__dirname, "./pages/dashboard.vue"),
  },
  // {
  //   name: "group-invitation",
  //   path: "/group-invitation/:token",
  //   file: resolve(__dirname, "./pages/workspaceInvitation.vue"),
  // }, // GroupDeprecation
  // {
  //   name: "workspace-invitation",
  //   path: "/workspace-invitation/:token",
  //   file: resolve(__dirname, "./pages/workspaceInvitation.vue"),
  // },
  // {
  //   name: "admin-settings",
  //   path: "/admin/settings",
  //   file: resolve(__dirname, "./pages/admin/settings.vue"),
  // },
  // {
  //   name: "style-guide",
  //   path: "/style-guide",
  //   file: resolve(__dirname, "./pages/styleGuide.vue"),
  // },
  // {
  //   name: "health-check",
  //   path: "/_health",
  //   file: resolve(__dirname, "./pages/_health.vue"),
  // },
  // {
  //   name: "settings",
  //   path: "/settings/:workspaceId",
  //   file: resolve(__dirname, "./pages/settings.vue"),
  //   children: [
  //     {
  //       name: "settings-members",
  //       path: "members",
  //       file: resolve(__dirname, "./pages/settings/members.vue"),
  //     },
  //     {
  //       name: "settings-invites",
  //       path: "invites",
  //       file: resolve(__dirname, "./pages/settings/invites.vue"),
  //     },
  //   ],
  // },
];

// if (process.env.NODE_ENV !== "production") {
//   routes.push({
//     name: "storybook",
//     path: "/storybook",
//     file: resolve(__dirname, "./pages/storybook.vue"),
//   });
// }
