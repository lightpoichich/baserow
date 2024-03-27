<template>
  <Modal>
    <h2 class="modal__title">
      {{ $t('leaveWorkspaceModal.title', { workspace: workspace.name }) }}
    </h2>

    <div class="modal__content">
      <Error :error="error"></Error>
      <div>
        <p>
          {{ $t('leaveWorkspaceModal.message', { workspace: workspace.name }) }}
        </p>
      </div>
    </div>

    <div class="modal__footer">
      <Button
        type="danger"
        :loading="loading"
        :disabled="loading"
        @click="leaveWorkspace()"
      >
        {{ $t('leaveWorkspaceModal.leave') }}
      </Button>
    </div>
  </Modal>
</template>

<script>
import modal from '@baserow/modules/core/mixins/modal'
import error from '@baserow/modules/core/mixins/error'

export default {
  name: 'LeaveWorkspaceModal',
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
    async leaveWorkspace() {
      this.hideError()
      this.loading = true

      const selected =
        this.$store.getters['workspace/getSelected'].id === this.workspace.id

      try {
        await this.$store.dispatch('workspace/leave', this.workspace)
        if (selected) {
          await this.$nuxt.$router.push({ name: 'dashboard' })
        }
        this.hide()
      } catch (error) {
        this.handleError(error, 'view')
      }

      this.loading = false
    },
  },
}
</script>
