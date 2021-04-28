<template>
  <div>
    <a
      ref="contextLink"
      class="crud-header__link"
      :class="{
        'active--primary': headerSearchTerm.length > 0,
      }"
      @click="$refs.context.toggle($refs.contextLink, 'bottom', 'right', 4)"
    >
      <i class="fas fa-search"></i>
      {{ headerSearchTerm }}
    </a>
    <CrudTableSearchContext
      ref="context"
      :loading="loading"
      @search-changed="searchChanged"
    ></CrudTableSearchContext>
  </div>
</template>

<script>
import debounce from 'lodash/debounce'
import CrudTableSearchContext from '@baserow_premium/components/crud_table/CrudTableSearchContext'

export default {
  name: 'CrudTableSearch',
  components: { CrudTableSearchContext },
  props: {
    loading: {
      type: Boolean,
      required: true,
    },
  },
  data: () => {
    return {
      headerSearchTerm: '',
    }
  },
  methods: {
    searchChanged(newSearch) {
      this.headerSearchTerm = newSearch
      this.debounceEmit()
    },
    debounceEmit: debounce(function () {
      this.$emit('search-changed', this.headerSearchTerm)
    }, 400),
  },
}
</script>
