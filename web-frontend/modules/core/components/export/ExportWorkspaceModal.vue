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
      <ExportWorkspaceForm
        v-if="!limitReached"
        ref="form"
        :snapshots="snapshots"
        @submitted="submitted"
      >
        <template v-if="jobIsRunning || jobHasSucceeded" #input>
          <ProgressBar
            :value="job.progress_percentage"
            :status="jobHumanReadableState"
          />
        </template>
        <template #default>
          <Button
            v-if="!createFinished"
            size="large"
            :loading="createLoading"
            :disabled="createLoading"
          >
            {{ $t('snapshotsModal.create') }}
          </Button>
          <Button v-else type="secondary" tag="a" size="large" @click="reset()">
            {{ $t('snapshotsModal.reset') }}</Button
          >
        </template>
      </ExportWorkspaceForm>
      <div v-else>
        {{ $t('snapshotsModal.limitReached') }}
      </div>
    </div>
    <template #actions> </template>
  </Modal>
</template>

<script>
import modal from '@baserow/modules/core/mixins/modal'
import error from '@baserow/modules/core/mixins/error'
import SnapshotListItem from '@baserow/modules/core/components/snapshots/SnapshotListItem'
import SnapshotsService from '@baserow/modules/core/services/snapshots'
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
      createLoading: false,
      createFinished: false,
      snapshotsLoading: false,
      snapshots: [],
      // Currently we don't query the backend to fetch the limit
      limitReached: false,
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
      // this.createLoading = true
      // this.hideError()
      // try {
      //   const { data } = await SnapshotsService(this.$client).create(
      //     this.application.id,
      //     values
      //   )
      //   this.startJobPoller(data)
      // } catch (error) {
      //   this.createLoading = false
      //   this.handleError(error)
      // }
    },
    async onJobDone() {
      // this.createLoading = false
      // this.createFinished = true
      // await this.loadSnapshots()
    },

    async onJobFailed() {
      // this.createLoading = false
      // this.showError(
      //   this.$t('clientHandler.notCompletedTitle'),
      //   this.job.human_readable_error
      // )
    },

    async onJobPollingError(error) {
      // this.createLoading = false
      // notifyIf(error)
    },
    async loadSnapshots() {
      // this.snapshotsLoading = true
      // this.snapshots = []
      // try {
      //   const { data } = await SnapshotsService(this.$client).list(
      //     this.application.id
      //   )
      //   this.snapshots = data
      // } catch (error) {
      //   this.handleError(error)
      // } finally {
      //   this.snapshotsLoading = false
      // }
    },
    snapshotDeleted(deletedSnapshot) {
      // this.snapshots = this.snapshots.filter(
      //   (snapshot) => snapshot.id !== deletedSnapshot.id
      // )
    },
    reset() {
      // this.stopPollIfRunning()
      // this.job = null
      // this.createFinished = false
      // this.createLoading = false
      // this.$refs.form.resetName()
    },
    getCustomHumanReadableJobState(jobState) {
      // if (jobState.startsWith('importing')) {
      //   return this.$t('snapshotsModal.importingState')
      // }
      // return ''
    },
  },
}
</script>
