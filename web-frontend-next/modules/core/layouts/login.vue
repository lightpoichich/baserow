<template>
  <div>
    <!-- <Notifications></Notifications> -->
    <div class="auth__page">
      <p>Login layout</p>
      <slot />
    </div>
  </div>
</template>

<script>
// import Notifications from "@baserow/modules/core/components/notifications/Notifications";

export default {
  components: {},
  middleware: ["settings", "urlCheck"],
  head() {
    return {
      bodyAttrs: {
        class: "auth__body",
      },
    };
  },
};
</script>
