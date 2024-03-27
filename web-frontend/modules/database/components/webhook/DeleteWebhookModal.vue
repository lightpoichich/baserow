<template>
  <Modal>
    <h2 class="modal__title">
      {{ $t('deleteWebhookModal.title', { webhookName: webhook.name }) }}
    </h2>
    <div class="modal__content">
      <Error :error="error"></Error>

      <p>
        {{ $t('deleteWebhookModal.body') }}
      </p>
    </div>

    <div class="modal__footer">
      <Button
        type="danger"
        :loading="loading"
        :disabled="loading"
        @click="deleteWebhook()"
      >
        {{ $t('deleteWebhookModal.deleteButton') }}
      </Button>
    </div>
  </Modal>
</template>

<script>
import modal from '@baserow/modules/core/mixins/modal'
import error from '@baserow/modules/core/mixins/error'
import WebhookService from '@baserow/modules/database/services/webhook'

export default {
  name: 'DeleteViewModal',
  mixins: [modal, error],
  props: {
    webhook: {
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
    async deleteWebhook() {
      this.loading = true

      try {
        await WebhookService(this.$client).delete(this.webhook.id)
        this.$emit('deleted', this.webhook)
      } catch (error) {
        this.handleError(error)
      }

      this.loading = false
    },
  },
}
</script>
