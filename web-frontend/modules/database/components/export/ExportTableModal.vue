<template>
  <Modal>
    <h2 class="box__title">Export {{ table.name }}</h2>
    <Error :error="error"></Error>
    <ExportTableForm
      :table="table"
      :view="view"
      :job="job"
      :loading="loading"
      @submitted="submitted"
      @values-changed="valuesChanged"
    ></ExportTableForm>
  </Modal>
</template>

<script>
import modal from '@baserow/modules/core/mixins/modal'
import error from '@baserow/modules/core/mixins/error'
import ExportTableForm from '@baserow/modules/database/components/export/ExportTableForm'
import ExporterService from '@baserow/modules/database/services/export'

export default {
  name: 'ExportTableModal',
  components: { ExportTableForm },
  mixins: [modal, error],
  props: {
    table: {
      type: Object,
      required: true,
    },
    view: {
      type: Object,
      required: false,
      default: null,
    },
  },
  data() {
    return {
      loading: false,
      job: null,
      pollInterval: null,
    }
  },
  computed: {
    jobIsRunning() {
      return (
        this.job !== null && ['exporting', 'pending'].includes(this.job.status)
      )
    },
    jobHasFailed() {
      return ['failed', 'cancelled'].includes(this.job.status)
    },
  },
  destroyed() {
    this.stopPollIfRunning()
  },
  methods: {
    async submitted(values) {
      this.loading = true
      this.hideError()

      try {
        const { data } = await ExporterService(this.$client).export(
          this.table.id,
          values
        )
        this.job = data
        if (this.pollInterval !== null) {
          clearInterval(this.pollInterval)
        }
        this.pollInterval = setInterval(this.getLatestJobInfo, 1000)
      } catch (error) {
        this.stopPollAndHandleError(error)
      }
    },
    async getLatestJobInfo() {
      try {
        const { data } = await ExporterService(this.$client).get(this.job.id)
        this.job = data
        if (!this.jobIsRunning) {
          this.loading = false
          this.stopPollIfRunning()
        }
        if (this.jobHasFailed) {
          const title =
            this.job.status === 'failed' ? 'Export Failed' : 'Export Cancelled'
          const message =
            this.job.status === 'failed'
              ? 'The export failed due to a server error.'
              : 'The export was cancelled.'
          this.showError(title, message)
        }
      } catch (error) {
        this.stopPollAndHandleError(error)
      }
    },
    stopPollAndHandleError(error) {
      this.loading = false
      this.stopPollIfRunning()
      this.handleError(error, 'application')
    },
    stopPollIfRunning() {
      if (this.pollInterval) {
        clearInterval(this.pollInterval)
      }
    },
    valuesChanged(newValues) {
      this.job = null
    },
  },
}
</script>
