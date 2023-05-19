<template>
  <div>
    <Login
      :display-header="true"
      :redirect-on-success="true"
      :invitation="invitation"
      :redirect-by-default="redirectByDefault"
    ></Login>
  </div>
</template>

<script>
import { useStore } from "vuex";

import Login from "@baserow/modules/core/components/auth/Login";
import workspaceInvitationToken from "@baserow/modules/core/mixins/workspaceInvitationToken";

definePageMeta({
  layout: "login",
});

export default {
  components: { Login },
  async setup() {
    const store = useStore();
    const route = useRoute();
    const app = useNuxtApp();
    const { t } = useI18n();
    const runtimeConfig = useRuntimeConfig();

    useHead({
      title: t("login.title"),
      link: [
        {
          rel: "canonical",
          href: runtimeConfig.public.publicWebFrontendUrl + route.path,
        },
      ],
    });

    if (store.getters["settings/get"].show_admin_signup_page === true)
      navigateTo("/signup");
    else if (store.getters["auth/isAuthenticated"]) navigateTo("/dashboard");

    return await workspaceInvitationToken.asyncData({ route, app });
  },

  computed: {
    redirectByDefault() {
      if (this.$route.query.noredirect === null) {
        return false;
      }
      return true;
    },
  },
};
</script>
