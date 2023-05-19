<template>
  <Alert
    v-if="error.visible"
    type="error"
    icon="exclamation"
    :title="error.title"
    >{{ error.message }}</Alert
  >
</template>

<script>
import Alert from "@baserow/modules/core/components/Alert";
/**
 * This component works the best if the parent has the error mixin.
 */
export default {
  components: { Alert },
  props: {
    error: {
      required: true,
      type: Object,
    },
  },
};
</script>
