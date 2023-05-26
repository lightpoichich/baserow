<template><p>Index</p></template>

<script>
import { useStore } from "vuex";
export default {
  setup() {
    const store = useStore();
    const pageRedirect = store.getters["auth/isAuthenticated"]
      ? "/dashboard"
      : "/login";

    console.log(pageRedirect);
    // navigateTo(pageRedirect);
  },
};
</script>
