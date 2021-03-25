<template>
  <div>
    <a
      ref="contextLink"
      class="header__filter-link"
      :class="{
        'active--searched': search.length > 0,
      }"
      @click="$refs.context.toggle($refs.contextLink, 'bottom', 'left', 4)"
    >
      <i class="header__search-icon fas fa-search"></i>
      {{ search }}
    </a>
    <ViewSearchContext
      ref="context"
      :view="view"
      @refresh="$emit('refresh', $event)"
      @searched="onSearched"
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
    return {
      search: '',
    }
  },
  computed: {
    sortTitle() {
      return 'Search'
    },
  },
  methods: {
    onSearched(newSearch) {
      this.search = newSearch
    },
  },
}
</script>
