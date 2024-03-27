<template>
  <div
    v-if="open"
    ref="modalWrapper"
    class="modal__wrapper"
    @click="outside($event)"
  >
    <div
      class="modal"
      :class="{
        'modal--full-height': fullHeight,
        'modal--full-max-height': !fullHeight && contentScrollable,
        'modal--with-sidebar': sidebar,
        'modal--full-screen': fullScreen,
        'modal--wide': wide,
        'modal--small': small,
        'modal--tiny': tiny,
        'modal--right': right,
      }"
    >
      <div
        v-if="leftSidebar"
        class="modal__box-sidebar modal__box-sidebar--left"
        :class="{ 'modal__box-sidebar--scrollable': leftSidebarScrollable }"
      >
        <slot name="sidebar"></slot>
      </div>
      <div
        class="modal__content-wrapper"
        :class="{
          'modal__content-wrapper--scrollable': contentScrollable,
          // 'modal__box-content-no-padding': !contentPadding,
        }"
      >
        <slot></slot>
        <div class="modal__actions">
          <a
            v-if="closeButton && canClose"
            class="modal__close"
            @click="hide()"
          >
            <i class="iconoir-cancel"></i>
          </a>

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
        </div>
      </div>

      <div
        v-if="rightSidebar"
        class="modal__box-sidebar modal__box-sidebar--right"
        :class="{
          'modal__box-sidebar--scrollable': rightSidebarScrollable,
          'modal__box-sidebar--collapsed': sidebarCollapsed,
        }"
      >
        <slot v-if="!sidebarCollapsed" name="sidebar"></slot>
      </div>

      <!-- <template v-if="!sidebar">
        <slot></slot>
        <slot name="content"></slot>
        <div class="modal__actions">
          <a
            v-if="closeButton && canClose"
            class="modal__close"
            @click="hide()"
          >
            <i class="iconoir-cancel"></i>
          </a>
          <slot name="actions"></slot>
        </div>
      </template> -->
    </div>
  </div>
</template>

<script>
import baseModal from '@baserow/modules/core/mixins/baseModal'

export default {
  name: 'Modal',
  mixins: [baseModal],
  props: {
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
    wide: {
      type: Boolean,
      default: false,
      required: false,
    },
    small: {
      type: Boolean,
      default: false,
      required: false,
    },
    tiny: {
      type: Boolean,
      default: false,
      required: false,
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
    contentScrollable: {
      type: Boolean,
      default: false,
      required: false,
    },
    // contentPadding: {
    //   type: Boolean,
    //   default: true,
    //   required: false,
    // },
    rightSidebarScrollable: {
      type: Boolean,
      default: false,
      required: false,
    },
    canClose: {
      type: Boolean,
      default: true,
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
