<template>
  <Modal small>
    <h2 class="modal__title">
      {{ $t('clearAllNotificationsConfirmModal.title') }}
    </h2>

    <div class="modal__content">
      <p>
        {{ $t('clearAllNotificationsConfirmModal.message') }}
      </p>
    </div>

    <div class="modal__footer">
      <Button
        type="secondary"
        @click.prevent="
          $emit('cancel', $event)
          hide()
        "
        >{{ $t('action.cancel') }}</Button
      >

      <Button
        type="danger"
        @click.prevent="
          $emit('confirm', $event)
          hide()
        "
      >
        {{ $t('action.delete') }}
      </Button>
    </div>
  </Modal>
</template>

<script>
import modal from '@baserow/modules/core/mixins/modal'

export default {
  name: 'ClearAllNotificationsConfirmModal',
  mixins: [modal],
}
</script>
