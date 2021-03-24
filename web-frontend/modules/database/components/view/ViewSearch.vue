<template>
  <div>
    <a
      class="header__filter-link"
      ref="contextLink"
      @click="$refs.context.toggle($refs.contextLink, 'bottom', 'left', 4)"
    >
      <i class="header__search-icon fas fa-search"></i>
    </a>
    <!-- TODO Is using the same "refresh" functionality what we want? -->
    <ViewSearchContext
      ref="context"
      :view="view"
      @refresh="$emit('refresh')"
    ></ViewSearchContext>
  </div>
</template>

<script>
import ViewSearchContext from '@baserow/modules/database/components/view/ViewSearchContext'

export default {
  name: 'ViewSearch',
  components: { ViewSearchContext },
  props: {
    view: {
      type: Object,
      required: true,
    },
  },
  data: () => {
    return {}
  },
  computed: {
    sortTitle() {
      return 'Search'
    },
  },
  methods: {},
}
</script>
