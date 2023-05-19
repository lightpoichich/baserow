export default {
  namespaced: true,
  state() {
    return {
      collapsed: false,
    };
  },

  mutations: {
    SET_COLLAPSED(state, collapsed) {
      state.collapsed = collapsed;
    },
  },

  actions: {
    toggleCollapsed({ commit, getters }, value) {
      if (value === undefined) {
        value = !getters.isCollapsed;
      }
      commit("SET_COLLAPSED", value);
    },
  },

  getters: {
    isCollapsed(state) {
      return !!state.collapsed;
    },
  },
};
