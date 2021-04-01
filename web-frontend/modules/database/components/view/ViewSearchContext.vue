<template>
  <Context
    :class="{ 'context--loading-overlay': view._.loading }"
    @shown="focus"
  >
    <form class="context__form" @submit.prevent="searchIfChanged">
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
              @keyup="searchIfChanged"
            />
            <i class="fas fa-search"></i>
          </div>
        </div>
      </div>
      <div class="control control--align-right margin-bottom-0">
        <SwitchInput
          v-model="hideRowsNotMatchingSearch"
          @input="searchIfChanged"
        >
          hide not matching rows
        </SwitchInput>
      </div>
    </form>
  </Context>
</template>

<script>
import debounce from 'lodash/debounce'

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
    searchIfChanged() {
      this.$emit('search-changed', this.activeSearchTerm)
      if (
        this.lastSearch === this.activeSearchTerm &&
        this.lastHide === this.hideRowsNotMatchingSearch
      ) {
        return
      }

      this.search()

      this.lastSearch = this.activeSearchTerm
      this.lastHide = this.hideRowsNotMatchingSearch
    },
    search() {
      this.loading = true

      this.$store.commit('view/grid/SET_SEARCH', {
        activeSearchTerm: this.activeSearchTerm,
        hideRowsNotMatchingSearch: this.hideRowsNotMatchingSearch,
      })

      // When the user toggles from hiding rows to not hiding rows we still
      // need to refresh as we need to fetch the un-searched rows from the server first.
      if (this.hideRowsNotMatchingSearch || this.lastHide) {
        // noinspection JSValidateTypes
        this.debouncedServerSearchRefresh()
      } else {
        // noinspection JSValidateTypes
        this.debouncedClientSideSearchRefresh()
      }
    },
    debouncedServerSearchRefresh: debounce(function () {
      this.$emit('refresh', {
        callback: this.finishedLoading,
      })
    }, 400),
    // Debounce even the client side only refreshes as otherwise spamming the keyboard
    // can cause many refreshes to queue up quickly bogging down the UI.
    debouncedClientSideSearchRefresh: debounce(function () {
      this.$store
        .dispatch('view/grid/updateSearchMatches')
        .then(this.finishedLoading)
    }, 10),
    finishedLoading() {
      this.loading = false
    },
  },
}
</script>
