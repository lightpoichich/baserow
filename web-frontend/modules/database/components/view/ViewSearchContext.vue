<template>
  <Context :class="{ 'context--loading-overlay': view._.loading }">
    <form class="context__form" @submit.prevent="searchIfChanged">
      <div class="control">
        <div class="control__elements">
          <div class="input__with-icon" :class="searchInputIconClasses">
            <input
              v-model="activeSearchTerm"
              type="text"
              placeholder="Search in all rows"
              class="input"
              :disabled="loading"
              @keyup="delayedSearch"
            />
            <i class="fas fa-search"></i>
          </div>
        </div>
      </div>
      <div class="control">
        <div class="control__right">
          <SwitchInput
            v-model="hideRowsNotMatchingSearch"
            :disabled="loading"
            @input="searchIfChanged()"
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
      activeSearchTerm: '',
      lastSearch: '',
      hideRowsNotMatchingSearch: true,
      lastHide: true,
      loading: false,
    }
  },
  computed: {
    searchInputIconClasses() {
      return {
        'input__with-icon--loading': this.loading,
      }
    },
  },
  methods: {
    delayedSearch: _.debounce(function () {
      this.searchIfChanged()
    }, 400),
    async searchIfChanged() {
      if (
        this.lastSearch === this.activeSearchTerm &&
        this.lastHide === this.hideRowsNotMatchingSearch
      ) {
        return
      }
      await this.performSearch()

      this.$emit('searchChanged', this.activeSearchTerm)

      this.lastSearch = this.activeSearchTerm
      this.lastHide = this.hideRowsNotMatchingSearch
    },
    async performSearch() {
      this.loading = true
      this.$store.commit('view/grid/SET_SEARCH', {
        activeSearchTerm: this.activeSearchTerm,
        hideRowsNotMatchingSearch: this.hideRowsNotMatchingSearch,
      })

      const needToTriggerServerSideRefresh =
        this.hideRowsNotMatchingSearch || this.lastHide

      if (needToTriggerServerSideRefresh) {
        const callback = function () {
          this.loading = false
        }
        this.$emit('refresh', {
          callback: callback.bind(this),
        })
      } else {
        await this.$store.dispatch('view/grid/updateSearchMatches')
        this.loading = false
      }
    },
  },
}
</script>
