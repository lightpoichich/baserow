<template>
  <div
    ref="modalWrapper"
    :class="{ hidden: !open }"
    class="modal-wrapper"
    @click="outside($event)"
  >
    <div class="modal-box">
      <a class="modal-close" @click="hide()">
        <i class="fas fa-times"></i>
      </a>
      <slot></slot>
    </div>
  </div>
</template>

<script>
import MoveToBody from '@/mixins/moveToBody'

export default {
  name: 'CreateGroupModal',
  mixins: [MoveToBody],
  data() {
    return {
      open: false
    }
  },
  methods: {
    /**
     * Toggle the open state of the modal.
     */
    toggle(value) {
      if (value === undefined) {
        value = !this.open
      }

      if (value) {
        this.show()
      } else {
        this.hide()
      }
    },
    /**
     * Show the modal.
     */
    show() {
      this.open = true
    },
    /**
     * Hide the modal.
     */
    hide() {
      this.open = false
    },
    /**
     * If someone actually clicked on the modal wrapper and not one of his children the
     * modal should be closed.
     */
    outside(event) {
      if (event.target === this.$refs.modalWrapper) {
        this.hide()
      }
    }
  }
}
</script>
