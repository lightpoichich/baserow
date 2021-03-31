<template>
  <Context
    :class="{ 'context--loading-overlay': view._.loading }"
    @shown="focus"
  >
    <form
      class="context__form"
      @submit.prevent="updateSearchLinkTextAndSearch(true)"
    >
      <div class="control margin-bottom-1">
        <div class="control__elements">
          <div
            class="input__with-icon"
            :class="{ 'input__with-icon--loading': loading }"
          >
            <input
              ref="activeSearchTermInput"
              v-model="activeSearchTerm"
              type="text"
              placeholder="Search in all rows"
              class="input"
              @keyup="updateSearchLinkTextAndSearch"
            />
            <i class="fas fa-search"></i>
          </div>
        </div>
      </div>
      <div class="control control--align-right margin-bottom-0">
        <SwitchInput
          v-model="hideRowsNotMatchingSearch"
          @input="searchIfChanged()"
        >
          hide not matching rows
        </SwitchInput>
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
  methods: {
    focus() {
      this.$nextTick(function () {
        this.$refs.activeSearchTermInput.focus()
      })
    },
    updateSearchLinkTextAndSearch(forceImmediateSearch = false) {
      this.$emit('search-changed', this.activeSearchTerm)
      if (this.hideRowsNotMatchingSearch && !forceImmediateSearch) {
        // noinspection JSValidateTypes
        this.debouncedSearchIfChanged()
      } else {
        this.searchIfChanged()
      }
    },
    debouncedSearchIfChanged: _.debounce(function () {
      this.searchIfChanged()
    }, 400),
    searchIfChanged() {
      if (
        this.lastSearch === this.activeSearchTerm &&
        this.lastHide === this.hideRowsNotMatchingSearch
      ) {
        return
      }
      this.triggerSearch()

      this.lastSearch = this.activeSearchTerm
      this.lastHide = this.hideRowsNotMatchingSearch
    },
    triggerSearch() {
      this.loading = true
      this.$store.commit('view/grid/SET_SEARCH', {
        activeSearchTerm: this.activeSearchTerm,
        hideRowsNotMatchingSearch: this.hideRowsNotMatchingSearch,
      })

      const needToTriggerServerSideRefresh =
        this.hideRowsNotMatchingSearch || this.lastHide

      if (needToTriggerServerSideRefresh) {
        this.$emit('refresh', {
          callback: this.finishedLoading,
        })
      } else {
        // Force the client side only search update to run once this component has been
        // rendered and updated showing the new loading state.
        setTimeout(() => {
          this.$store
            .dispatch('view/grid/updateSearchMatches')
            .then(this.finishedLoading)
        })
      }
    },
    finishedLoading() {
      this.loading = false
    },
  },
}
</script>
