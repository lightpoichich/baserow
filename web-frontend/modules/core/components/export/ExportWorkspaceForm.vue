<template>
  <form @submit.prevent="submit">
    <!--    <FormGroup small-label :label="$t('exportWorkspaceModal.exportSettings')" />-->
    <FormGroup
      :error="fieldHasErrors('name')"
      small-label
      :label="$t('exportWorkspaceModal.exportSettings')"
      required
    >
      <slot name="settings">
        <FormInput
          ref="structure_only"
          v-model="values.structure_only"
          type="checkbox"
          size="large"
          :error="fieldHasErrors('structure_only')"
          class="snapshots-modal__name-input"
        />
      </slot>

      <template #after-input>
        <slot></slot>
      </template>
    </FormGroup>
  </form>
</template>

<script>
import form from '@baserow/modules/core/mixins/form'
import ExportLoadingBar from '@baserow/modules/database/components/export/ExportLoadingBar.vue'
import { required } from 'vuelidate/lib/validators'

export default {
  name: 'ExportWorkspaceForm',
  components: { ExportLoadingBar },
  mixins: [form],
  data() {
    return {
      values: {
        structure_only: false,
      },
    }
  },
  validations() {
    return {
      values: {
        structure_only: {
          required,
        },
      },
    }
  },
}
</script>
