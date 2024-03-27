<template>
  <Modal>
    <h2 class="modal__title">
      {{
        create
          ? $t('integrationCreateEditModal.createTitle')
          : $t('integrationCreateEditModal.editTitle')
      }}
    </h2>
    <div class="modal__content">
      <Alert v-if="actualIntegrationType.warning" type="warning">
        <template #title>{{
          $t('integrationCreateEditModal.warningTitle')
        }}</template>
        <span>{{ actualIntegrationType.warning }}</span>
      </Alert>

      <IntegrationEditForm
        ref="form"
        :application="application"
        :default-values="create ? getDefaultIntegrationValues() : integration"
        :integration-type="actualIntegrationType"
        @submitted="submit"
      />

      <Error :error="error"></Error>
    </div>

    <div class="modal__footer">
      <Button
        :loading="loading"
        :disabled="loading"
        @click.prevent="$refs.form.submit()"
      >
        {{ create ? $t('action.create') : $t('action.save') }}
      </Button>
    </div>
  </Modal>
</template>

<script>
import { mapActions } from 'vuex'
import error from '@baserow/modules/core/mixins/error'
import modal from '@baserow/modules/core/mixins/modal'
import IntegrationEditForm from '@baserow/modules/core/components/integrations/IntegrationEditForm'
import { getNextAvailableNameInSequence } from '@baserow/modules/core/utils/string'

export default {
  components: { IntegrationEditForm },
  mixins: [modal, error],
  props: {
    application: {
      type: Object,
      required: true,
    },
    integration: {
      type: Object,
      required: false,
      default: null,
    },
    integrationType: {
      type: Object,
      required: false,
      default: null,
    },
    create: {
      type: Boolean,
      required: false,
      default: false,
    },
  },
  data() {
    return { loading: false }
  },
  computed: {
    actualIntegrationType() {
      if (this.create) {
        return this.integrationType
      }
      return this.$registry.get('integration', this.integration.type)
    },
    integrations() {
      return this.$store.getters['integration/getIntegrations'](
        this.application
      )
    },
  },
  methods: {
    ...mapActions({
      actionUpdateIntegration: 'integration/update',
      actionCreateIntegration: 'integration/create',
    }),

    shown() {
      this.hideError()
    },
    getDefaultIntegrationValues() {
      const name = getNextAvailableNameInSequence(
        this.actualIntegrationType.name,
        this.integrations.map(({ name }) => name)
      )

      return { name, ...this.actualIntegrationType.getDefaultValues() }
    },
    async submit(values) {
      this.loading = true
      this.hideError()
      try {
        if (this.create) {
          const newIntegration = await this.actionCreateIntegration({
            application: this.application,
            integrationType: this.actualIntegrationType.type,
            values,
          })
          this.$emit('created', newIntegration)
        } else {
          await this.actionUpdateIntegration({
            application: this.application,
            integrationId: this.integration.id,
            values,
          })
        }
        this.hide()
      } catch (error) {
        this.handleError(error)
      }
      this.loading = false
    },
  },
}
</script>
