<template>
  <div
    v-move-to-body
    v-click-outside="hide"
    class="context"
    :class="{ 'visibility-hidden': !open }"
  >
    <slot></slot>
  </div>
</template>

<script>
import { isElement } from '@/utils/dom'

export default {
  name: 'Context',
  data() {
    return {
      open: false,
      opener: null,
      children: []
    }
  },
  /**
   * Because we don't want the parent context to close when a user clicks 'outside' that
   * element and in the child element we need to register the child with their parent to
   * prevent this.
   */
  beforeMount() {
    let $parent = this.$parent
    while ($parent !== undefined) {
      if ($parent.registerContextChild) {
        $parent.registerContextChild(this.$el)
        break
      }
      $parent = $parent.$parent
    }
  },
  methods: {
    /**
     * Toggles the open state of the context menu.
     *
     * @param target      The original element element that changed the state of the
     *                    context, this will be used to calculate the correct position.
     * @param vertical    Bottom positions the context under the target.
     *                    Top positions the context above the target.
     * @param horizontal  Left aligns the context with the left side of the target.
     *                    Right aligns the context with the right side of the target.
     * @param offset      The distance between the target element and the context.
     * @param value       True if context must be shown, false if not and undefine
     *                    will invert the current state.
     */
    toggle(
      target,
      vertical = 'bottom',
      horizontal = 'left',
      offset = 10,
      value
    ) {
      if (value === undefined) {
        value = !this.open
      }

      if (value) {
        const css = this.calculatePosition(target, vertical, horizontal, offset)

        // Set the calculated positions of the context.
        for (const key in css) {
          const value = css[key] !== null ? Math.ceil(css[key]) + 'px' : 'auto'
          this.$el.style[key] = value
        }
      }

      // If we store the element who opened the context menu we can exclude the element
      // when clicked outside of this element.
      this.opener = value ? target : null
      this.open = value
    },
    hide(event) {
      // Checks if the click is inside one of our children. In that code the context
      // must stay open.
      const isChild = this.children.some(element =>
        isElement(element, event.target)
      )

      // Checks if the context is already opened, if the click was not on the opener
      // because he can trigger the toggle method and if the click was not in one of
      // our child contexts.
      if (this.open && !isElement(this.opener, event.target) && !isChild) {
        this.open = false
      }
    },
    /**
     * Calculates the absolute position of the context based on the original clicked
     * element.
     */
    calculatePosition(target, vertical, horizontal, offset) {
      const targetRect = target.getBoundingClientRect()
      const contextRect = this.$el.getBoundingClientRect()
      const positions = { top: null, right: null, bottom: null, left: null }

      // Calculate if top, bottom, left and right positions are possible.
      const canTop = targetRect.top - contextRect.height - offset > 0
      const canBottom =
        window.innerHeight - targetRect.bottom - contextRect.height - offset > 0
      const canRight = targetRect.right - contextRect.width > 0
      const canLeft =
        window.innerWidth - targetRect.left - contextRect.width > 0

      // If bottom, top, left or right doesn't fit, but their opposite does we switch to
      // that.
      if (vertical === 'bottom' && !canBottom && canTop) {
        vertical = 'top'
      }

      if (vertical === 'top' && !canTop) {
        vertical = 'bottom'
      }

      if (horizontal === 'left' && !canLeft && canRight) {
        horizontal = 'right'
      }

      if (horizontal === 'right' && !canRight) {
        horizontal = 'left'
      }

      // Calculate the correct positions for horizontal and vertical values.
      if (horizontal === 'left') {
        positions.left = targetRect.left
      }

      if (horizontal === 'right') {
        positions.right = window.innerWidth - targetRect.right
      }

      if (vertical === 'bottom') {
        positions.top = targetRect.bottom + offset
      }

      if (vertical === 'top') {
        positions.bottom = window.innerHeight - targetRect.top + offset
      }

      return positions
    },
    /**
     * A child context can register itself with the parent to prevent closing of the
     * parent when clicked inside the child.
     *
     * @param element HTMLElement
     */
    registerContextChild(element) {
      this.children.push(element)
    }
  }
}
</script>
