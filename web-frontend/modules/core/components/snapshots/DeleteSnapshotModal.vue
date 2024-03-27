<template>
  <Modal tiny :close-button="false">
    <h3 class="modal__title">{{ $t('deleteSnapshotModal.title') }}</h3>

    <div class="modal__content">
      <p>
        {{ $t('deleteSnapshotModal.content', { name: snapshot.name }) }}
      </p>
    </div>

    <div class="modal__footer">
      <Button type="secondary" @click.prevent="hide">
        {{ $t('action.cancel') }}</Button
      >
      <Button
        type="danger"
        :loading="loading"
        :disabled="loading"
        @click.prevent="confirm"
      >
        {{ $t('deleteSnapshotModal.confirm') }}</Button
      >
    </div>
  </Modal>
</template>

<script>
import modal from '@baserow/modules/core/mixins/modal'
import Modal from '@baserow/modules/core/components/Modal'
import SnapshotsService from '@baserow/modules/core/services/snapshots'
import { notifyIf } from '@baserow/modules/core/utils/error'

export default {
  components: {
    Modal,
  },
  mixins: [modal],
  props: {
    snapshot: {
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
    async confirm() {
      this.loading = true

      try {
        await SnapshotsService(this.$client).delete(this.snapshot.id)
        this.$emit('snapshot-deleted', this.snapshot)
        this.hide()
      } catch (error) {
        notifyIf(error)
      } finally {
        this.loading = false
      }
    },
  },
}
</script>
