<template>
  <div>
    <div class="auth__logo">
      <NuxtLink :to="{ name: 'index' }">
        <img src="@baserow/modules/core/static/img/logo.svg" alt="" />
      </NuxtLink>
    </div>
    <div class="auth__head auth__head--more-margin">
      <h1 class="auth__head-title">
        {{ $t("signup.title") }}
      </h1>
      <LangPicker />
    </div>
    <template v-if="shouldShowAdminSignupPage">
      <Alert :title="$t('signup.requireFirstUser')">{{
        $t("signup.requireFirstUserMessage")
      }}</Alert>
    </template>
    <template v-if="!isSignupEnabled">
      <Alert
        simple
        type="error"
        icon="exclamation"
        :title="$t('signup.disabled')"
        >{{ $t("signup.disabledMessage") }}</Alert
      >
      <NuxtLink :to="{ name: 'login' }" class="button button--full-width">
        {{ $t("action.backToLogin") }}
      </NuxtLink>
    </template>
    <template v-else>
      <PasswordRegister
        v-if="afterSignupStep < 0 && passwordLoginEnabled"
        :invitation="invitation"
        @success="next"
      >
      </PasswordRegister>
      <LoginButtons
        show-border="top"
        :hide-if-no-buttons="true"
        :invitation="invitation"
      />
      <LoginActions v-if="!shouldShowAdminSignupPage" :invitation="invitation">
        <li>
          {{ $t("signup.loginText") }}
          <NuxtLink :to="{ name: 'login' }">
            {{ $t("action.login") }}
          </NuxtLink>
        </li>
      </LoginActions>
      <component
        :is="afterSignupStepComponents[afterSignupStep]"
        @success="next"
      ></component>
    </template>
  </div>
</template>

<script>
import { useStore, mapGetters } from "vuex";
import PasswordRegister from "@baserow/modules/core/components/auth/PasswordRegister";
import LangPicker from "@baserow/modules/core/components/LangPicker";
import LoginButtons from "@baserow/modules/core/components/auth/LoginButtons";
import LoginActions from "@baserow/modules/core/components/auth/LoginActions";
import workspaceInvitationToken from "@baserow/modules/core/mixins/workspaceInvitationToken";

definePageMeta({
  layout: "login",
  middleware: ["settings"],
});

export default {
  components: { PasswordRegister, LangPicker, LoginButtons, LoginActions },
  async setup() {
    const { t } = useI18n();
    const store = useStore();
    const route = useRoute();
    const nuxtApp = useNuxtApp();

    useHead({
      title: t("signup.headTitle"),
    });

    if (store.getters["auth/isAuthenticated"]) {
      return navigateTo({ name: "dashboard" });
    }
    await store.dispatch("authProvider/fetchLoginOptions");
    return await workspaceInvitationToken.asyncData({ route, nuxtApp });
  },
  data() {
    return {
      afterSignupStep: -1,
    };
  },
  computed: {
    isSignupEnabled() {
      return (
        this.settings.allow_new_signups ||
        (this.settings.allow_signups_via_workspace_invitations &&
          this.invitation?.id)
      );
    },
    shouldShowAdminSignupPage() {
      return this.settings.show_admin_signup_page;
    },
    afterSignupStepComponents() {
      return Object.values(this.$registry.getAll("plugin"))
        .reduce((components, plugin) => {
          components = components.concat(plugin.getAfterSignupStepComponent());
          return components;
        }, [])
        .filter((component) => component !== null);
    },
    ...mapGetters({
      settings: "settings/get",
      loginActions: "authProvider/getAllLoginActions",
      passwordLoginEnabled: "authProvider/getPasswordLoginEnabled",
    }),
  },
  methods: {
    next() {
      if (this.afterSignupStep + 1 < this.afterSignupStepComponents.length) {
        this.afterSignupStep++;
      } else {
        this.$nuxt.$router.push({ name: "dashboard" }, () => {
          this.$store.dispatch("settings/hideAdminSignupPage");
        });
      }
    },
  },
};
</script>
