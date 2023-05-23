<template>
  <div>
    <!-- <Notifications></Notifications> -->
    <div class="auth__page">
      <slot />
    </div>
  </div>
</template>

<script>
// import Notifications from "@baserow/modules/core/components/notifications/Notifications";

export default {
  components: {},
  head() {
    return {
      bodyAttrs: {
        class: "auth__body",
      },
    };
  },
};
</script>
