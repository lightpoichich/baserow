<template>
  <div class="user-admin-rows">
    <div class="user-admin-rows__left">
      <div class="user-admin-rows__head">
        <div class="user-admin-rows__field user-admin-rows__field--first">
          <div>ID</div>
        </div>
        <div class="user-admin-rows__field">
          <i class="fas user-admin-rows__field-icon"></i>
          Username
        </div>
      </div>
      <div class="user-admin-rows__body">
        <div
          v-for="row in rows"
          :key="'left-select-row-' + row.id"
          class="user-admin-rows__row"
        >
          <div class="user-admin-rows__cell user-admin-rows__cell--first">
            {{ row.id }}
          </div>
        </div>
      </div>
      <div class="user-admin-rows__foot">
        <div class="user-admin-rows__pagination">
          <div class="user-admin-rows__pagination-name">page</div>
          <div class="user-admin-rows__pagination-group">
            <a
              class="user-admin-rows__pagination-button"
              :class="{
                'user-admin-rows__pagination-button--disabled': page === 1,
              }"
              @click="fetch(page - 1)"
            >
              <i class="fas fa-caret-left"></i>
            </a>
            <input
              v-model="visiblePage"
              class="input user-admin-rows__pagination-page-input"
              type="number"
              @keypress.enter="fetch(visiblePage)"
            />
            <div class="user-admin-rows__pagination-count">
              of {{ totalPages }}
            </div>
            <a
              class="user-admin-rows__pagination-button"
              :class="{
                'user-admin-rows__pagination-button--disabled':
                  page === totalPages,
              }"
              @click="fetch(page + 1)"
            >
              <i class="fas fa-caret-right"></i>
            </a>
          </div>
        </div>
      </div>
    </div>
    <div ref="right" class="user-admin-rows__right">
      <div class="user-admin-rows__head">
        <div>
          <i class="fas user-admin-rows__field-icon"></i>
          Fields
        </div>
      </div>
      <div class="user-admin-rows__body">
        <div
          v-for="row in rows"
          :key="'right-select-row-' + row.id"
          class="user-admin-rows__row"
        >
          Fields
        </div>
      </div>
      <div class="user-admin-rows__foot"></div>
    </div>
  </div>
</template>

<script>
import { notifyIf } from '@baserow/modules/core/utils/error'

export default {
  name: 'UsersAdminContent',
  props: {},
  data() {
    return {
      loading: false,
      loaded: false,
      rows: [{ name: 'test', id: 1 }],
      search: '',
      visibleSearch: '',
      page: 1,
      visiblePage: 1,
      totalPages: null,
    }
  },
  methods: {
    /**
     * Returns the scrollable element for the scrollbar.
     */
    /**
     * Fetches all the fields of the given table id. We need the fields so that we can
     * show the data in the correct format.
     */
    async fetchFields(tableId) {
      try {
        await true
        // const { data } = await FieldService(this.$client).fetchAll(tableId)
        // data.forEach((part, index, d) => {
        //   populateField(data[index], this.$registry)
        // })
        // const primaryIndex = data.findIndex((item) => item.primary === true)
        // this.primary =
        //   primaryIndex !== -1 ? data.splice(primaryIndex, 1)[0] : null
        // this.fields = data
      } catch (error) {
        this.loading = false
        notifyIf(error, 'row')
      }
    },
    /**
     * Does a row search in the table related to the state. It will also reset the
     * pagination.
     */
    async doSearch(query) {
      this.search = query
      this.totalPages = null
      await this.fetch(1)
    },
    /**
     * Fetches the rows of a given page and adds them to the state. If a search query
     * has been stored in the state then that will be remembered.
     */
    async fetch(page) {},
    /**
     * Called when the user selects a row.
     */
  },
}
</script>
