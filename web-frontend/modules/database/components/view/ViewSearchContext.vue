<template>
  <!--  TODO add the various loading etc display states -->
  <!--  TODO do we want to search on every keypress instead? -->
  <Context :class="{ 'context--loading-overlay': view._.loading }">
    <form class="context__form" @submit.prevent="doSearch">
      <div class="control">
        <div class="control__elements">
          <div class="search__context">
            <i class="fas fa-search search__context-icon"></i>
            <input
              v-model="search"
              type="text"
              placeholder="Search in all fields"
              class="input search__context-input"
              @keypress.enter="doSearch"
            />
          </div>
        </div>
      </div>
    </form>
  </Context>
</template>

<script>
import context from '@baserow/modules/core/mixins/context'

export default {
  name: 'ViewSearchContext',
  mixins: [context],
  props: {
    view: {
      type: Object,
      required: true,
    },
  },
  data() {
    return {
      search: '',
    }
  },
  methods: {
    async doSearch() {
      // TODO is it ok that we are tied to grid here? instead perhaps
      // the state should be moved onto view store and then grid gets it from the view?
      await this.$store.dispatch('view/grid/updateSearch', {
        search: this.search,
      })
      this.$emit('refresh')
    },
  },
}
</script>
