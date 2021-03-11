<template>
  <div v-show="dragging">
    <div
      class="grid-view__field-dragging"
      :style="{ width: width + 'px', left: draggingLeft + 'px' }"
    ></div>
    <div
      class="grid-view__field-target"
      :style="{ left: targetLeft + 'px' }"
    ></div>
  </div>
</template>

<script>
import gridViewHelpers from '@baserow/modules/database/mixins/gridViewHelpers'

export default {
  name: 'GridViewFieldDragging',
  mixins: [gridViewHelpers],
  props: {
    view: {
      type: Object,
      required: true,
    },
    fields: {
      type: Array,
      required: true,
    },
    containerWidth: {
      type: Number,
      required: true,
    },
  },
  data() {
    return {
      dragging: false,
      field: null,
      targetFieldId: null,
      mouseStart: 0,
      scrollStart: 0,
      width: 0,
      draggingLeft: 0,
      targetLeft: 0,
      lastMoveEvent: null,
      autoScrolling: false,
    }
  },
  beforeDestroy() {
    this.cancel()
  },
  methods: {
    getFieldLeft(id) {
      let left = 0
      for (let i = 0; i < this.fields.length; i++) {
        if (this.fields[i].id === id) {
          break
        }
        left += this.getFieldWidth(this.fields[i].id)
      }
      return left
    },
    /**
     * Called when the field dragging must start. It will register the global mouse
     * move, mouse up events and keyup events so that the user can drag the item to
     * the correct position.
     */
    start(field, event) {
      this.field = field
      this.targetFieldId = field.id
      this.dragging = true
      this.mouseStart = event.clientX
      this.scrollStart = this.$parent.$el.scrollLeft
      this.draggingLeft = 0
      this.targetLeft = 0

      this.$el.moveEvent = (event) => this.move(event)
      window.addEventListener('mousemove', this.$el.moveEvent)

      this.$el.upEvent = (event) => this.up(event)
      window.addEventListener('mouseup', this.$el.upEvent)

      this.$el.keydownEvent = (event) => {
        if (event.keyCode === 27) {
          // When the user presses the escape key we want to cancel the action
          this.cancel(event)
        }
      }
      document.body.addEventListener('keydown', this.$el.keydownEvent)
      this.move(event, false)
    },
    /**
     * The move method is called when every time the user moves the mouse while
     * dragging a field. It can also be called while auto scrolling.
     */
    move(event = null, startAutoScroll = true) {
      if (event !== null) {
        event.preventDefault()
        this.lastMoveEvent = event
      } else {
        event = this.lastMoveEvent
      }

      // This is the horizontally scrollable element.
      const element = this.$parent.$el

      this.width = this.getFieldWidth(this.field.id)

      // Calculate the left position of the dragging animation. This is the transparent
      // overlay that has the same width as the field.
      this.draggingLeft = Math.min(
        this.getFieldLeft(this.field.id) +
          event.clientX -
          this.mouseStart +
          this.$parent.$el.scrollLeft -
          this.scrollStart,
        this.containerWidth - this.width
      )

      // Calculate which after which field we want to place the field that is currently
      // being dragged. This is named the target. We also calculate wat which position
      // the field would up for visualisation purposes.
      const mouseLeft =
        event.clientX -
        element.getBoundingClientRect().left +
        element.scrollLeft
      let left = 0
      for (let i = 0; i < this.fields.length; i++) {
        const width = this.getFieldWidth(this.fields[i].id)
        const nextWidth =
          i + 1 < this.fields.length
            ? this.getFieldWidth(this.fields[i + 1].id)
            : width
        const leftHalf = left + Math.floor(width / 2)
        const rightHalf = left + width + Math.floor(nextWidth / 2)
        if (i === 0 && mouseLeft < leftHalf) {
          this.targetFieldId = 0
          this.targetLeft = 0
          break
        }
        if (mouseLeft > leftHalf && mouseLeft < rightHalf) {
          this.targetFieldId = this.fields[i].id
          this.targetLeft = left + width
          break
        }
        left += width
      }

      // If the user is not already auto scrolling, which happens while dragging and
      // moving the element outside of the view port left at the left or right side,
      // we might need to initiate that process.
      if (!this.autoScrolling || !startAutoScroll) {
        const relativeLeft = this.draggingLeft - element.scrollLeft
        const relativeRight = relativeLeft + this.getFieldWidth(this.field.id)
        const maxScrollLeft = element.scrollWidth - element.clientWidth
        let speed = 0

        if (relativeLeft < 0 && element.scrollLeft > 0) {
          // If the dragging animation falls out of the left side of the viewport we
          // need to auto scroll to the left.
          speed = -Math.ceil(Math.min(Math.abs(relativeLeft), 100) / 20)
        } else if (
          relativeRight > element.clientWidth &&
          element.scrollLeft < maxScrollLeft
        ) {
          // If the dragging animation falls out of the right side of the viewport we
          // need to auto scroll to the right.
          speed = Math.ceil(
            Math.min(relativeRight - element.clientWidth, 100) / 20
          )
        }

        // If the speed is either a position or negative, so not 0, we know that we
        // need to start auto scrolling.
        if (speed !== 0) {
          this.autoScrolling = true
          this.$emit('scroll', { pixelY: 0, pixelX: speed })
          this.$el.scrollTimeout = setTimeout(() => {
            this.move(null, false)
          }, 1)
        } else {
          this.autoScrolling = false
        }
      }
    },
    /**
     * Can be called when the current dragging state needs to be stopped. It will
     * remove all the created event listeners and timeouts.
     */
    cancel() {
      this.dragging = false
      window.removeEventListener('mousemove', this.$el.moveEvent)
      window.removeEventListener('mouseup', this.$el.upEvent)
      document.body.addEventListener('keydown', this.$el.keydownEvent)
      clearTimeout(this.$el.scrollTimeout)
    },
    /**
     * Called when the user releases the mouse on a the desired position. It will
     * calculate the new position of the field in the list and if it has changed
     * position, then the order in the field options is updated accordingly.
     */
    up(event) {
      event.preventDefault()
      this.cancel()

      // We don't need to do anything if the field needs to be placed after itself
      // because that wouldn't change the position.
      if (this.field.id === this.targetFieldId) {
        return
      }

      const oldOrder = this.fields.map((field) => field.id)
      // Create an array of field ids in the correct order excluding the field that
      // needs to be repositioned because that one will be added later.
      const newOrder = this.fields
        .filter((field) => field.id !== this.field.id)
        .map((field) => field.id)
      if (this.targetFieldId === 0) {
        // If the target field id is 0 the field needs to be moved to the beginning.
        newOrder.unshift(this.field.id)
      } else {
        // Calculate after which field the field that needs to be repositioned needs to
        // be placed.
        const targetIndex = newOrder.findIndex(
          (id) => id === this.targetFieldId
        )
        newOrder.splice(targetIndex + 1, 0, this.field.id)
      }

      // Check if the new order differs from the old order. If that is not the case we
      // don't need to update the field options because nothing will be changed anyway.
      if (JSON.stringify(oldOrder) === JSON.stringify(newOrder)) {
        return
      }

      this.$store.dispatch('view/grid/updateFieldOptionsOrder', {
        gridId: this.view.id,
        order: newOrder,
      })
    },
  },
}
</script>
