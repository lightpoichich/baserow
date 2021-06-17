<template>
  <Modal :very-small="true" :close-button="false">
    <h3>
      Are you sure you want to
      {{ selectedIsTrashed ? 'empty the trash of' : 'permanently delete' }}
      {{ name }}
    </h3>
    <p>
      This will permanently delete
      {{
        selectedIsTrashed ? 'the listed items' : 'it and all of its contents'
      }}. After which they cannot be recovered.
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
          {{ selectedIsTrashed ? 'Empty' : 'Permanently delete' }}
        </a>
      </div>
    </div>
  </Modal>
</template>

<script>
/**
 * A simple confirmation modal to check that the user is sure they want to permanently
 * delete / empty.
 */
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
    selectedIsTrashed: {
      type: Boolean,
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
