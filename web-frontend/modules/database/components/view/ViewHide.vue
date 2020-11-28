<template>
  <div>
    <a
      ref="contextLink"
      class="header__filter-link"
      :class="{
        'active--primary': hiddenFields.length > 0,
      }"
      @click="$refs.context.toggle($refs.contextLink, 'bottom', 'left', 4)"
    >
      <i class="header__filter-icon fas fa-eye-slash"></i>
      <span v-if="hiddenFields.length === 1"
        >{{ hiddenFields.length }} hidden field</span
      >
      <span v-else-if="hiddenFields.length > 1"
        >{{ hiddenFields.length }} hidden fields</span
      >
      <span v-else>Hide fields</span>
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
import { mapGetters } from 'vuex'
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
  computed: {
    hiddenFields() {
      return this.fields.filter((field) => {
        return this.fieldOptions[field.id].hidden
      })
    },
    ...mapGetters({
      fieldOptions: 'view/grid/getAllFieldOptions',
    }),
  },
}
</script>
