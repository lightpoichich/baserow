<template>
  <Modal>
    <h2 class="box__title">
      {{ $t('exportWorkspaceModal.title') }} {{ workspace.name }}
    </h2>
    <p>
      {{ $t('exportWorkspaceModal.description') }}
    </p>
    <component
      :is="component"
      v-for="(component, index) in workspaceExportModalAlertComponents"
      :key="index"
    ></component>
    <Error :error="error"></Error>
    <div class="export-workspace-modal">
      <ExportWorkspaceForm ref="form" @submitted="submitted">
        <template v-if="jobIsRunning || jobHasSucceeded" #settings>
          <ProgressBar
            :value="job.progress_percentage"
            :status="jobHumanReadableState"
          />
        </template>
        <template #default>
          <Button
            v-if="!loading && !created"
            size="large"
            :loading="loading"
            :disabled="loading"
          >
            {{ $t('exportWorkspaceModal.export') }}
          </Button>
          <Button
            v-if="loading && !created"
            type="secondary"
            tag="a"
            size="large"
            @click="cancel()"
          >
            {{ $t('exportWorkspaceModal.cancel') }}</Button
          >
          <DownloadLink
            v-if="!loading && created"
            class="button button--large button--full-width modal-progress__export-button"
            :url="job.url"
            :filename="job.exported_file_name"
            :loading-class="'button--loading'"
          >
            {{ $t('exportTableLoadingBar.download') }}
          </DownloadLink>
        </template>
      </ExportWorkspaceForm>
    </div>
    <template #actions> </template>
  </Modal>
</template>

<script>
import modal from '@baserow/modules/core/mixins/modal'
import error from '@baserow/modules/core/mixins/error'
import SnapshotListItem from '@baserow/modules/core/components/snapshots/SnapshotListItem'
import WorkspaceService from '@baserow/modules/core/services/workspace'
import jobProgress from '@baserow/modules/core/mixins/jobProgress'
import ExportWorkspaceForm from '@baserow/modules/core/components/export/ExportWorkspaceForm'
import { notifyIf } from '@baserow/modules/core/utils/error'

export default {
  name: 'ExportWorkspaceModal',
  components: {
    ExportWorkspaceForm,
    SnapshotListItem,
  },
  mixins: [modal, error, jobProgress],
  props: {
    workspace: {
      type: Object,
      required: true,
    },
  },
  data() {
    return {
      job: null,
      loading: false,
      created: false,
    }
  },
  computed: {
    workspaceExportModalAlertComponents() {
      return Object.values(this.$registry.getAll('plugin'))
        .map((plugin) =>
          plugin.getExtraExportWorkspaceModalComponents(this.workspace)
        )
        .filter((component) => component !== null)
    },
  },
  beforeDestroy() {
    this.stopPollIfRunning()
  },
  methods: {
    show(...args) {
      this.hideError()
      // this.loadSnapshots()
      modal.methods.show.bind(this)(...args)
    },
    async submitted(values) {
      this.loading = true
      this.hideError()
      try {
        const { data } = await WorkspaceService(this.$client).export(
          this.workspace.id,
          values
        )
        this.startJobPoller(data)
      } catch (error) {
        this.loading = false
        this.handleError(error)
      }
    },
    async onJobDone() {
      this.loading = false
      this.created = true
    },

    async onJobFailed() {
      this.loading = false
      this.showError(
        this.$t('clientHandler.notCompletedTitle'),
        this.job.human_readable_error
      )
    },

    async onJobPollingError(error) {
      this.loading = false
      notifyIf(error)
    },
    cancel() {
      this.stopPollIfRunning()
      this.job = null
      this.finished = false
      this.loading = false
      this.$refs.form.reset()
    },
  },
}
</script>
