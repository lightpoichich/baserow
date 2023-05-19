<template><p>Homepage</p></template>

<script>
import { useStore } from "vuex";
export default {
  setup() {
    const store = useStore();
    const pageRedirect = store.getters["auth/isAuthenticated"]
      ? "/dashboard"
      : "/login";
    navigateTo(pageRedirect);
  },
};
</script>
