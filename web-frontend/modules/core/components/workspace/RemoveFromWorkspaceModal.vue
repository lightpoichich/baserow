<template>
  <Modal>
    <h2 class="modal__title">
      {{ $t('removeFromWorkspaceModal.title') }}
    </h2>

    <div class="modal__content">
      <Error :error="error"></Error>
      <div>
        <p>
          {{
            $t('removeFromWorkspaceModal.confirmation', {
              name: member.name,
              workspaceName: workspace.name,
            })
          }}
        </p>
      </div>
    </div>
    <div class="modal__footer">
      <Button
        type="danger"
        :loading="loading"
        :disabled="loading"
        @click.prevent="remove()"
      >
        {{ $t('removeFromWorkspaceModal.remove') }}
      </Button>
    </div>
  </Modal>
</template>

<script>
import modal from '@baserow/modules/core/mixins/modal'
import error from '@baserow/modules/core/mixins/error'
import WorkspaceService from '@baserow/modules/core/services/workspace'

export default {
  name: 'RemoveFromWorkspaceModal',
  mixins: [modal, error],
  props: {
    workspace: {
      type: Object,
      required: true,
    },
    member: {
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
    async remove() {
      if (this.loading) {
        return
      }
      this.loading = true
      try {
        await WorkspaceService(this.$client).deleteUser(this.member.id)
        await this.$store.dispatch('workspace/forceDeleteWorkspaceUser', {
          workspaceId: this.workspace.id,
          id: this.member.id,
          values: { user_id: this.member.user_id },
        })
        this.$emit('remove-user', this.member.id)
        this.hide()
      } catch (error) {
        this.loading = false
        this.handleError(error)
      } finally {
        this.loading = false
      }
    },
  },
}
</script>
