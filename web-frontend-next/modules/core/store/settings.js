import SettingsService from "@baserow/modules/core/services/settings";
import { clone } from "@baserow/modules/core/utils/object";

export default {
  namespaced: true,
  state() {
    return {
      loaded: false,
      settings: {},
    };
  },

  mutations: {
    SET_SETTINGS(state, values) {
      state.settings = values;
    },
    UPDATE_SETTINGS(state, values) {
      state.settings = Object.assign({}, state.settings, values);
    },
    SET_LOADED(state, value) {
      state.loaded = value;
    },
    HIDE_ADMIN_SIGNUP_PAGE(state) {
      state.settings.show_admin_signup_page = false;
    },
  },

  actions: {
    async load({ commit }) {
      const nuxtApp = useNuxtApp();
      const { data } = await SettingsService(nuxtApp.$client).get();

      commit("SET_SETTINGS", data);
      commit("SET_LOADED", true);
    },
    async update({ commit, getters }, values) {
      console.log(getters);
      const oldValues = clone(getters.get);
      commit("UPDATE_SETTINGS", values);

      try {
        await SettingsService(this.$client).update(values);
      } catch (e) {
        commit("SET_SETTINGS", oldValues);
        throw e;
      }
    },
    hideAdminSignupPage({ commit }) {
      commit("HIDE_ADMIN_SIGNUP_PAGE");
    },
  },

  getters: {
    isLoaded(state) {
      return state.loaded;
    },
    get(state) {
      return state.settings;
    },
  },
};
