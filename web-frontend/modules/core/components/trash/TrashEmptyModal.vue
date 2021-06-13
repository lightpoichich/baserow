<template>
  <Modal :very-small="true" :close-button="false">
    <h3>Are you sure you want to empty the trash of {{ name }}</h3>
    <p>
      This will permanently delete the listed items. After emptying they cannot
      be recovered.
    </p>
    <div class="actions">
      <div class="align-right">
        <a class="trash-confirm-empty__cancel-button" @click.prevent="hide()">
          Cancel
        </a>
        <a
          class="button button button--error"
          @click.prevent="emitEmptyAndClose"
        >
          Empty
        </a>
      </div>
    </div>
  </Modal>
</template>

<script>
import modal from '@baserow/modules/core/mixins/modal'

export default {
  name: 'TrashEmptyModal',
  components: {},
  mixins: [modal],
  props: {
    name: {
      type: String,
      required: true,
    },
  },
  methods: {
    emitEmptyAndClose() {
      this.$emit('empty')
      this.hide()
    },
  },
}
</script>
