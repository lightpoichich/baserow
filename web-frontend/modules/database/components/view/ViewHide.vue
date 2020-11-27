<template>
  <div>
    <a
      ref="contextLink"
      class="header__filter-link"
      :class="{
        'active--warning': view.sortings.length > 0,
      }"
      @click="$refs.context.toggle($refs.contextLink, 'bottom', 'left', 4)"
    >
      <i class="header__filter-icon fas fa-eye-slash"></i>
      Hide fields
    </a>
    <ViewHideContext
      ref="context"
      :view="view"
      :fields="fields"
      :primary="primary"
      @changed="$emit('changed')"
    ></ViewHideContext>
  </div>
</template>

<script>
import ViewHideContext from './ViewHideContext'

export default {
  name: 'ViewHide',
  components: { ViewHideContext },
  props: {
    primary: {
      type: Object,
      required: true,
    },
    fields: {
      type: Array,
      required: true,
    },
    view: {
      type: Object,
      required: true,
    },
  },
}
</script>
