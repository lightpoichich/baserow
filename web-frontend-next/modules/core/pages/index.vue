<template>
  <h1>Index</h1>
  <p>Authenticated: {{ $store.getters["auth/isAuthenticated"] }}</p>
</template>

<script>
import { useStore } from "vuex";

export default {
  setup() {
    console.log("pwet");
    const store = useStore();
    console.log(store.getters["auth/isAuthenticated"]);
    const pageRedirect = store.getters["auth/isAuthenticated"]
      ? "/dashboard"
      : "/login";
    console.log(pageRedirect);
    // navigateTo(pageRedirect);
  },
};
</script>
