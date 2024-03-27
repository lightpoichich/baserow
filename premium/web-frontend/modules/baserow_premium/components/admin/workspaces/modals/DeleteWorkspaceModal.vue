<template>
  <Modal>
    <h2 class="modal__title">
      {{ $t('deleteWorkspaceModal.title', workspace) }}
    </h2>

    <div class="modal__content">
      <Error :error="error"></Error>
      <i18n path="deleteWorkspaceModal.confirmation" tag="p">
        <template #name>
          <strong>{{ workspace.name }}</strong>
        </template>
      </i18n>
      <p>
        {{ $t('deleteWorkspaceModal.comment') }}
      </p>
    </div>

    <div class="modal__footer">
      <Button
        type="danger"
        :disabled="loading"
        :loading="loading"
        @click.prevent="deleteWorkspace()"
      >
        {{ $t('deleteWorkspaceModal.delete', workspace) }}</Button
      >
    </div>
  </Modal>
</template>

<script>
import modal from '@baserow/modules/core/mixins/modal'
import error from '@baserow/modules/core/mixins/error'
import WorkspacesAdminService from '@baserow_premium/services/admin/workspaces'

export default {
  name: 'DeleteWorkspaceModal',
  mixins: [modal, error],
  props: {
    workspace: {
      type: Object,
      required: true,
    },
  },
  data() {
    return {
      loading: false,
    }
  },
  methods: {
    async deleteWorkspace() {
      this.hideError()
      this.loading = true

      try {
        await WorkspacesAdminService(this.$client).delete(this.workspace.id)
        this.$emit('workspace-deleted', this.workspace.id)
        this.hide()
      } catch (error) {
        this.handleError(error, 'workspace')
      }

      this.loading = false
    },
  },
}
</script>
