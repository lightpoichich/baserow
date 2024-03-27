<template>
  <Modal :small="true">
    <h2 class="modal__title">
      {{ $t('shareViewDisablePasswordModal.title') }}
    </h2>
    <div class="modal__content">
      <Error :error="error"></Error>
      <div>
        <p>
          {{ $t('shareViewDisablePasswordModal.description') }}
        </p>
      </div>
    </div>

    <div class="modal__footer">
      <Button type="secondary" @click.prevent="hide()">
        {{ $t('action.cancel') }}
      </Button>
      <Button
        type="danger"
        :loading="loading"
        :disabled="loading"
        @click.prevent="disableAndClose"
      >
        {{ $t('shareViewDisablePasswordModal.disable') }}
      </Button>
    </div>
  </Modal>
</template>

<script>
/**
 * A simple confirmation modal to check that the user is sure they want to remove
 * the password protection, cleaning the current password.
 */
import error from '@baserow/modules/core/mixins/error'
import modal from '@baserow/modules/core/mixins/modal'

export default {
  name: 'ShareViewDisablePasswordModal',
  components: {},
  mixins: [error, modal],
  props: {
    view: {
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
    async disableAndClose() {
      this.loading = true

      const view = this.view
      try {
        await this.$store.dispatch('view/update', {
          view,
          values: { public_view_password: '' },
        })

        this.hide()
      } catch (error) {
        this.handleError(error, 'table')
      }

      this.loading = false
    },
  },
}
</script>
