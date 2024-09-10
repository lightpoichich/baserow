<template>
  <div
    v-if="open"
    ref="modalWrapper"
    class="modal__overlay"
    @click="outside($event)"
  >
    <div
      ref="modal"
      class="modal"
      :class="{
        'modal--full-height': fullHeight && size !== 'fullscreen',
        'modal--with-sidebar': sidebar,
        'modal--with-topbar': topbar,
        'modal--with-header': hasHeader,
        'modal--with-right-sidebar': rightSidebar,
        'modal--with-left-sidebar': leftSidebar,
        'modal--fullscreen': size === 'fullscreen' && !fullHeight,
        'modal--large': size === 'large',
        'modal--small': size === 'small',
        'modal--tiny': size === 'tiny',
        'modal--right': right,
      }"
    >
      <div v-if="topbar" class="modal__topbar">
        <slot name="topbar-content"></slot>

        <div class="modal__topbar-actions">
          <ul class="modal__topbar-icons">
            <slot name="topbar-actions"></slot>
          </ul>

          <i
            class="iconoir-cancel modal__topbar-icon-close"
            @click="hide()"
          ></i>
        </div>
      </div>

      <div class="modal__wrapper">
        <div v-if="leftSidebar" class="modal__sidebar modal__sidebar--left">
          <slot name="sidebar"></slot>
        </div>

        <div ref="contentWrapper" class="modal__content-wrapper">
          <div v-if="hasHeader" ref="header" class="modal__header">
            <slot name="header"></slot>
          </div>

          <div ref="content" class="modal__content">
            <slot name="content"></slot>
          </div>

          <div v-if="hasFooter" ref="footer" class="modal__footer">
            <slot name="footer"></slot>
          </div>
        </div>

        <a v-if="closeButton && !topbar" class="modal__close" @click="hide()">
          <i class="iconoir-cancel"></i>
        </a>

        <div v-if="rightSidebar" class="modal__sidebar modal__sidebar--right">
          <slot v-if="!sidebarCollapsed" name="sidebar"></slot>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import baseModal from '@baserow/modules/core/mixins/baseModal'

export default {
  name: 'Modal',
  mixins: [baseModal],
  props: {
    topbar: {
      type: Boolean,
      default: false,
      required: false,
    },
    leftSidebar: {
      type: Boolean,
      default: false,
      required: false,
    },
    rightSidebar: {
      type: Boolean,
      default: false,
      required: false,
    },
    hasHeader: {
      type: Boolean,
      default: true,
      required: false,
    },
    hasFooter: {
      type: Boolean,
      default: true,
      required: false,
    },
    /**
     * The size of the button.
     */
    size: {
      required: false,
      type: String,
      default: 'regular',
      validator(value) {
        return ['tiny', 'small', 'regular', 'large', 'fullscreen'].includes(
          value
        )
      },
    },
    closeButton: {
      type: Boolean,
      default: true,
      required: false,
    },
    fullHeight: {
      type: Boolean,
      default: false,
      required: false,
    },
    right: {
      type: Boolean,
      default: false,
      required: false,
    },
  },
  data() {
    return {
      sidebarCollapsed: false,
    }
  },
  computed: {
    sidebar() {
      return this.leftSidebar || this.rightSidebar
    },
  },
  methods: {
    collapseSidebar() {
      this.sidebarCollapsed = !this.sidebarCollapsed
    },
  },
}
</script>
