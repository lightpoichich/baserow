<template>
  <form @submit.prevent="submit">
    <!--    <FormGroup small-label :label="$t('exportWorkspaceModal.exportSettings')" />-->
  </form>
</template>

<script>
import form from '@baserow/modules/core/mixins/form'
import ExportLoadingBar from '@baserow/modules/database/components/export/ExportLoadingBar.vue'

export default {
  name: 'ExportWorkspaceForm',
  components: { ExportLoadingBar },
  mixins: [form],
  props: {
    snapshots: {
      type: Array,
      required: true,
    },
  },
  data() {
    return {
      values: {
        structure_only: false,
      },
    }
  },
}
</script>
