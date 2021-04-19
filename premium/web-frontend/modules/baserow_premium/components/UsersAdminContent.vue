<template>
  <div class="user-admin-wrapper">
    <div v-if="!loaded" class="user-admin-rows__initial-loading"></div>
    <div
      v-if="loaded"
      :class="{ 'user-admin-rows__loading': loading }"
      class="user-admin-wrapper"
    >
      <header class="admin_header">
        <b>User Settings</b>
        <a
          ref="contextLink"
          class="admin-header__link"
          @click="$refs.context.toggle($refs.contextLink, 'bottom', 'right', 4)"
        >
          <i class="fas fa-search"></i>
        </a>
      </header>
      <div class="user-admin-rows">
        <div class="user-admin-rows__field user-admin-rows__field-sticky">
          ID
        </div>
        <div class="user-admin-rows__field user-admin-rows__field-right">
          <i class="fas user-admin-rows__field-icon"></i>
          Username
        </div>
        <div class="user-admin-rows__field">Full Name</div>
        <div class="user-admin-rows__field">Groups</div>
        <div class="user-admin-rows__field">Last Login</div>
        <div class="user-admin-rows__field">Signed Up</div>
        <div class="user-admin-rows__field">Active</div>
        <div
          v-for="cell in cells"
          :key="'admin-row-' + cell.row_id + '-' + cell.cell_id"
          :class="{
            'user-admin-rows__cell-right': cell.cell_id === 2,
            'user-admin-rows__cell-sticky': cell.cell_id <= 2,
          }"
          class="user-admin-rows__cell"
        >
          {{ cell.content }}
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
              @click="fetchPage(page - 1)"
            >
              <i class="fas fa-caret-left"></i>
            </a>
            <input
              v-model="visiblePage"
              class="input user-admin-rows__pagination-page-input"
              type="number"
              @keypress.enter="fetchPage(visiblePage)"
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
              @click="fetchPage(page + 1)"
            >
              <i class="fas fa-caret-right"></i>
            </a>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import UserAdminService from '@baserow_premium/services/userAdmin'
import { notifyIf } from '@baserow/modules/core/utils/error'

export default {
  name: 'UsersAdminContent',
  props: {},
  data() {
    return {
      loading: false,
      loaded: false,
      search: '',
      visibleSearch: '',
      page: 1,
      visiblePage: 1,
      totalPages: null,
      cells: [],
    }
  },
  async fetch() {
    await this.fetchPage(1)
  },
  methods: {
    async doSearch(query) {
      this.search = query
      this.totalPages = null
      await this.fetch(1)
    },
    /**
     * Fetches the rows of a given page and adds them to the state. If a search query
     * has been stored in the state then that will be remembered.
     */
    async fetchPage(page) {
      if (
        this.totalPages !== null &&
        this.totalPages !== 0 &&
        (page > this.totalPages || page < 1)
      ) {
        console.log('SOME DUBM SHIT')
        this.visiblePage = this.page
        return
      }

      this.loading = true
      this.loaded = false

      try {
        const { data: userData } = await UserAdminService(
          this.$client
        ).fetchPage(page)
        const newCells = []
        for (const user of userData.results) {
          const attrs = [
            user.id,
            user.username,
            user.full_name,
            user.groups.map((e) => e.name).join(', '),
            user.last_login,
            user.date_joined,
            user.is_active,
          ]
          let i = 1
          for (const attr of attrs) {
            newCells.push({
              row_id: user.id,
              cell_id: i++,
              content: attr,
            })
          }
        }
        this.page = page
        this.visiblePage = page
        this.totalPages = Math.ceil(userData.count / 100)
        this.loaded = true
        this.cells = newCells
      } catch (error) {
        notifyIf(error, 'row')
        this.loaded = false
      }

      this.loading = false
    },
  },
}
</script>
