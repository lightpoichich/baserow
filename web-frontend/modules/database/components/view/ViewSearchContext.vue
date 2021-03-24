<template>
  <!--  TODO add the various loading etc display states -->
  <!--  TODO do we want to search on every keypress instead? -->
  <Context :class="{ 'context--loading-overlay': view._.loading }">
    <form class="context__form" @submit.prevent="doSearch">
      <div class="control">
        <div class="control__elements">
          <div class="input__with-icon">
            <input
              v-model="search"
              type="text"
              placeholder="Search in all fields"
              class="input"
              @keyup="delayedSearch"
            />
            <i class="fas fa-search"></i>
          </div>
        </div>
      </div>
      <div class="control">
        <div class="control__elements">
          <SwitchInput v-model="hiddenSearch" @input="doSearch()">
            hide not matching rows</SwitchInput
          >
        </div>
      </div>
    </form>
  </Context>
</template>

<script>
import _ from 'lodash'

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
      lastSearch: '',
      hiddenSearch: true,
      lastHide: true,
    }
  },
  methods: {
    delayedSearch: _.debounce(function () {
      this.doSearch()
    }, 400),
    async doSearch() {
      if (
        this.lastSearch === this.search &&
        this.lastHide === this.hiddenSearch
      ) {
        return
      }

      // TODO is it ok that we are tied to grid here? instead perhaps
      // the state should be moved onto view store and then grid gets it from the view?
      await this.$store.dispatch('view/grid/updateSearch', {
        search: this.search,
        hiddenSearch: this.hiddenSearch,
      })
      if (this.hiddenSearch || (this.lastHide && !this.hiddenSearch)) {
        this.$emit('refresh')
      }
      this.$emit('searched', this.search)

      this.lastSearch = this.search
      this.lastHide = this.hiddenSearch
    },
  },
}
</script>
