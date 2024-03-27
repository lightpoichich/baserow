<template>
  <Modal>
    <h2 class="modal__title">{{ $t('createWorkspaceModal.createNew') }}</h2>
    <div class="modal__content">
      <Error :error="error"></Error>
      <WorkspaceForm
        ref="workspaceForm"
        :default-name="getDefaultName()"
        @submitted="submitted"
      >
      </WorkspaceForm>
    </div>

    <div class="modal__footer">
      <Button
        type="primary"
        :loading="loading"
        :disabled="loading"
        @click="$refs.workspaceForm.submit()"
      >
        {{ $t('createWorkspaceModal.add') }}
      </Button>
    </div>
  </Modal>
</template>

<script>
import modal from '@baserow/modules/core/mixins/modal'
import error from '@baserow/modules/core/mixins/error'
import { getNextAvailableNameInSequence } from '@baserow/modules/core/utils/string'

import WorkspaceForm from './WorkspaceForm'
import { ResponseErrorMessage } from '@baserow/modules/core/plugins/clientHandler'

export default {
  name: 'CreateWorkspaceModal',
  components: { WorkspaceForm },
  mixins: [modal, error],
  data() {
    return {
      loading: false,
    }
  },
  methods: {
    getDefaultName() {
      const excludeNames = this.$store.getters['workspace/getAll'].map(
        (workspace) => workspace.name
      )
      const baseName = this.$t('createWorkspaceModal.defaultName')
      return getNextAvailableNameInSequence(baseName, excludeNames)
    },
    async submitted(values) {
      this.loading = true
      this.hideError()

      try {
        const workspace = await this.$store.dispatch('workspace/create', values)
        await this.$store.dispatch('workspace/select', workspace)
        this.loading = false
        this.$emit('created', workspace)
        await this.$router.push({
          name: 'workspace',
          params: { workspaceId: workspace.id },
        })
        this.hide()
      } catch (error) {
        this.loading = false
        this.handleError(error, 'workspace')
        this.handleError(error, 'workspace', {
          PERMISSION_DENIED: new ResponseErrorMessage(
            this.$t('createWorkspaceModal.permissionDeniedTitle'),
            this.$t('createWorkspaceModal.permissionDeniedBody')
          ),
        })
      }
    },
  },
}
</script>
