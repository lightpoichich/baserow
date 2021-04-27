<template>
  <div>
    <a
      ref="contextLink"
      class="admin-header__link"
      :class="{
        'active--primary': headerSearchTerm.length > 0,
      }"
      @click="$refs.context.toggle($refs.contextLink, 'bottom', 'right', 4)"
    >
      <i class="fas fa-search"></i>
      {{ headerSearchTerm }}
    </a>
    <UserSearchContext
      ref="context"
      :loading="loading"
      @search-changed="searchChanged"
    ></UserSearchContext>
  </div>
</template>

<script>
import debounce from 'lodash/debounce'
import UserSearchContext from '@baserow_premium/components/admin/user/UserSearchContext'

export default {
  name: 'UserSearch',
  components: { UserSearchContext },
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
