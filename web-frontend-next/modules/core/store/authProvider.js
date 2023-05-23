import authProviderService from "@baserow/modules/core/services/authProvider";

function populateProviderLoginOptions(authProviderType, registry) {
  const type = registry.get("authProvider", authProviderType.type);
  return type.populateLoginOptions(authProviderType);
}

export default {
  namespaced: true,
  state() {
    return {
      loginOptionsLoaded: false,
      loginOptions: {},
    };
  },

  mutations: {
    SET_LOGIN_OPTIONS(state, loginOptions) {
      state.loginOptions = loginOptions;
      state.loginOptionsLoaded = true;
    },
  },

  actions: {
    async fetchLoginOptions({ commit }) {
      const nuxtApp = useNuxtApp();

      const { data } = await authProviderService(
        nuxtApp.$client
      ).fetchLoginOptions();
      const loginOptions = {};
      for (const providerTypeLoginOption of Object.values(data)) {
        const loginOption = populateProviderLoginOptions(
          providerTypeLoginOption,
          nuxtApp.$registry
        );
        loginOptions[providerTypeLoginOption.type] = loginOption;
      }
      commit("SET_LOGIN_OPTIONS", loginOptions);
      return loginOptions;
    },
  },

  getters: {
    areLoginOptionsLoaded(state) {
      return state.loginOptionsLoaded;
    },
    getLoginOptionsForType: (state) => (type) => {
      return state.loginOptions[type];
    },
    getAllLoginButtons: (state) => {
      let optionsWithButton = [];
      for (const loginOption of Object.values(state.loginOptions)) {
        if (
          loginOption.hasLoginButton &&
          loginOption.items &&
          loginOption.items.length > 0
        ) {
          optionsWithButton = optionsWithButton.concat(loginOption.items);
        }
      }
      return optionsWithButton;
    },
    getAllLoginActions: (state) => {
      const loginActions = [];
      for (const loginOption of Object.values(state.loginOptions)) {
        if (loginOption.hasLoginAction) {
          loginActions.push(loginOption);
        }
      }

      return loginActions;
    },
    getPasswordLoginEnabled: (state) => {
      return !!state.loginOptions.password;
    },
    getDefaultRedirectUrl: (state) => {
      const loginOptionsArr = Object.values(state.loginOptions);
      const possibleRedirectLoginOptions = loginOptionsArr.filter(
        (loginOption) => loginOption.default_redirect_url
      );
      if (
        loginOptionsArr.length === 1 &&
        possibleRedirectLoginOptions.length === 1
      ) {
        return possibleRedirectLoginOptions[0].default_redirect_url;
      }
      return null;
    },
  },
};
