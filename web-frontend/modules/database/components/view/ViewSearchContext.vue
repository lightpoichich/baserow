<template>
  <Context :class="{ 'context--loading-overlay': view._.loading }">
    <form class="context__form" @submit.prevent="doSearch">
      <div class="control">
        <div class="control__elements">
          <div class="input__with-icon" :class="searchInputIconClasses">
            <input
              v-model="search"
              type="text"
              placeholder="Search in all rows"
              class="input"
              :disabled="searchLoading"
              @keyup="delayedSearch"
            />
            <i class="fas fa-search"></i>
          </div>
        </div>
      </div>
      <div class="control">
        <div class="control__right">
          <SwitchInput
            v-model="hiddenSearch"
            :disabled="searchLoading"
            @input="doSearch()"
          >
            hide not matching rows
          </SwitchInput>
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
      searchLoading: false,
    }
  },
  computed: {
    searchInputIconClasses() {
      return {
        'input__with-icon--loading': this.searchLoading,
      }
    },
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

      this.searchLoading = true
      await this.$store.dispatch('view/grid/updateSearch', {
        search: this.search,
        hiddenSearch: this.hiddenSearch,
      })
      if (!this.hiddenSearch) {
        await this.$store.dispatch('view/grid/refreshSearch', {})
      }
      if (this.hiddenSearch || (this.lastHide && !this.hiddenSearch)) {
        const callback = function () {
          this.searchLoading = false
        }
        this.$emit('refresh', {
          callback: callback.bind(this),
        })
      } else {
        this.searchLoading = false
      }
      this.$emit('searched', this.search)

      this.lastSearch = this.search
      this.lastHide = this.hiddenSearch
    },
  },
}
</script>
