<template>
  <ModalV2
    :can-close="!jobIsRunning"
    :close-button="!jobIsRunning"
    @show="loading = false"
    @hidden="handleHidden"
  >
    <template #header-content>
      <h2>
        {{ $t('action.createNew') }} {{ applicationType.getName() | lowercase }}
      </h2>
    </template>

    <template #content>
      <Error :error="error"></Error>

      <component
        :is="applicationType.getApplicationFormComponent()"
        ref="applicationForm"
        :default-name="getDefaultName()"
        :loading="loading"
        @submitted="submitted"
        @job-done="handleJobDone($event)"
        @job-updated="handleJobUpdated($event)"
        @import-type-changed="importType = $event"
      >
      </component>
    </template>

    <template #footer-content>
      <ProgressBar
        v-if="importType === 'airtable' && (jobIsRunning || jobHasSucceeded)"
        :value="jobProgressPercentage"
        :status="jobStatus"
      />

      <template v-if="importType === 'airtable'">
        <Button
          v-if="!jobHasSucceeded"
          :loading="jobIsRunning"
          :disabled="jobIsRunning"
          @click="$refs.applicationForm.submit()"
        >
          {{ $t('importFromAirtable.importButtonLabel') }}
        </Button>

        <Button v-else type="secondary" @click="openDatabase">
          {{ $t('importFromAirtable.openButtonLabel') }}</Button
        >
      </template>

      <Button
        v-else
        type="primary"
        :loading="loading"
        :disabled="loading"
        @click="$refs.applicationForm.submit()"
      >
        {{ $t('action.add') }}
        {{ applicationType.getName() | lowercase }}
      </Button>
    </template>
  </ModalV2>
</template>

<script>
import modalv2 from '@baserow/modules/core/mixins/modalv2'
import error from '@baserow/modules/core/mixins/error'
import { getNextAvailableNameInSequence } from '@baserow/modules/core/utils/string'

export default {
  name: 'CreateApplicationModal',
  mixins: [modalv2, error],
  props: {
    applicationType: {
      type: Object,
      required: true,
    },
    workspace: {
      type: Object,
      required: true,
    },
  },
  data() {
    return {
      loading: false,
      importType: null,
      jobHasSucceeded: false,
      jobIsRunning: false,
      jobStatus: '',
      jobProgressPercentage: 0,
      jobDatabaseId: null,
    }
  },
  computed: {},
  methods: {
    getDefaultName() {
      const excludeNames = this.$store.getters['application/getAllOfWorkspace'](
        this.workspace
      ).map((application) => application.name)
      const baseName = this.applicationType.getDefaultName()
      return getNextAvailableNameInSequence(baseName, excludeNames)
    },
    async submitted(values) {
      this.loading = true
      this.hideError()

      try {
        const application = await this.$store.dispatch('application/create', {
          type: this.applicationType.type,
          workspace: this.workspace,
          values,
        })
        this.$emit('created', application)
        // select the application just created in the sidebar and open it
        await this.$store.dispatch('application/selectById', application.id)
        await this.$registry
          .get('application', application.type)
          .select(application, this)
        this.hide()
      } catch (error) {
        this.handleError(error, 'application')
      } finally {
        this.loading = false
      }
    },
    async openDatabase() {
      const application = this.$store.getters['application/get'](
        this.jobDatabaseId
      )
      const type = this.$registry.get('application', application.type)
      if (await type.select(application, this)) {
        this.hide()
        this.jobIsRunning = false
        this.jobHasSucceeded = false
      }
    },
    handleJobDone(event) {
      this.jobStatus = event.state
      this.jobProgressPercentage = event.progress_percentage
      this.jobIsRunning = false
      this.jobHasSucceeded = true
      this.jobDatabaseId = event.databaseId
    },
    handleJobUpdated(event) {
      this.jobIsRunning = true
      this.jobStatus = event.state
      this.jobProgressPercentage = event.progress_percentage
    },
    handleHidden() {
      this.importType = null
      this.jobIsRunning = false
      this.jobHasSucceeded = false
      this.jobStatus = ''
      this.jobProgressPercentage = 0
      this.jobDatabaseId = null
    },
  },
}
</script>
