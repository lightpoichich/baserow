<template>
  <ul v-if="!tableLoading" class="header__filter">
    <li class="header__filter-item">
      <GridViewHide
        :view="view"
        :fields="fields"
        :read-only="readOnly"
        :store-prefix="storePrefix"
      ></GridViewHide>
    </li>
  </ul>
</template>

<script>
import { mapState } from 'vuex'

import GridViewHide from '@baserow/modules/database/components/view/grid/GridViewHide'

export default {
  name: 'GridViewHeader',
  components: { GridViewHide },
  props: {
    fields: {
      type: Array,
      required: true,
    },
    view: {
      type: Object,
      required: true,
    },
    readOnly: {
      type: Boolean,
      required: true,
    },
    storePrefix: {
      type: String,
      required: true,
    },
  },
  computed: {
    ...mapState({
      tableLoading: (state) => state.table.loading,
    }),
  },
}
</script>
