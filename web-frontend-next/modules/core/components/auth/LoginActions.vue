<template>
  <ul class="auth__action-links">
    <li v-for="loginAction in loginActions" :key="loginAction.name">
      <component
        :is="getLoginActionComponent(loginAction)"
        :options="loginAction"
        :invitation="invitation"
        :original="computedOriginal"
      >
      </component>
    </li>
    <slot></slot>
  </ul>
</template>

<script>
import { mapGetters } from "vuex";

export default {
  props: {
    invitation: {
      required: false,
      validator: (prop) => typeof prop === "object" || prop === null,
      default: null,
    },
    original: {
      type: String,
      required: false,
      default: null,
    },
  },
  computed: {
    ...mapGetters({
      loginActions: "authProvider/getAllLoginActions",
    }),
    computedOriginal() {
      let original = this.original;
      if (!original) {
        original = this.$route.query.original;
      }
      return original;
    },
  },
  methods: {
    getLoginActionComponent(loginAction) {
      const nuxtApp = useNuxtApp();
      return nuxtApp.$registry
        .get("authProvider", loginAction.type)
        .getLoginActionComponent();
    },
  },
};
</script>
