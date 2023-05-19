import { createStore } from "vuex";

import sidebarStoreModule from "../store/sidebar";
import undoRedoStoreModule from "../store/undoRedo";
import workspaceStoreModule from "../store/workspace";
import settingsStoreModule from "../store/settings";
import notificationStoreModule from "../store/notification";
import jobStoreModule from "../store/job";
import authProviderStoreModule from "../store/authProvider";
import authStoreModule from "../store/auth";
import applicationStoreModule from "../store/application";

const store = createStore({
  modules: {
    sidebar: sidebarStoreModule,
    undoRedo: undoRedoStoreModule,
    workspace: workspaceStoreModule,
    settings: settingsStoreModule,
    notification: notificationStoreModule,
    job: jobStoreModule,
    authProvider: authProviderStoreModule,
    auth: authStoreModule,
    application: applicationStoreModule,
  },
});

export default defineNuxtPlugin({
  async setup(nuxtApp) {
    nuxtApp.vueApp.use(store);
    nuxtApp.provide("store", store);
  },
});
