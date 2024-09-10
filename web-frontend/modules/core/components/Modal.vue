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
        <div
          v-if="leftSidebar"
          class="modal__sidebar modal__sidebar--left"
          :class="{ 'modal__sidebar--scrollable': leftSidebarScrollable }"
        >
          <slot name="sidebar"></slot>
        </div>

        <div ref="contentWrapper" class="modal__content-wrapper">
          <div ref="header" class="modal__header">
            <slot name="header"></slot>
          </div>

          <div ref="content" class="modal__content">
            <slot name="content"></slot>
          </div>

          <div ref="footer" class="modal__footer">
            <slot name="footer"></slot>
          </div>
        </div>

        <a v-if="closeButton" class="modal__close" @click="hide()">
          <i class="iconoir-cancel"></i>
        </a>
        <!-- 
        <div ref="actions" class="modal__actions">
          

          <a
            v-if="collapsibleRightSidebar"
            class="modal__collapse"
            @click="collapseSidebar"
          >
            <i
              :class="{
                'iconoir-fast-arrow-right': !sidebarCollapsed,
                'iconoir-fast-arrow-left': sidebarCollapsed,
              }"
            ></i>
          </a>
          <slot name="actions"></slot>
        </div> -->

        <div
          v-if="rightSidebar"
          class="modal__sidebar modal__sidebar--right"
          :class="{
            'modal__sidebar--scrollable': rightSidebarScrollable,
            'modal__sidebar--collapsed': sidebarCollapsed,
          }"
        >
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
    fullScreen: {
      type: Boolean,
      default: false,
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
    leftSidebarScrollable: {
      type: Boolean,
      default: false,
      required: false,
    },
    rightSidebarScrollable: {
      type: Boolean,
      default: false,
      required: false,
    },
    collapsibleRightSidebar: {
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
