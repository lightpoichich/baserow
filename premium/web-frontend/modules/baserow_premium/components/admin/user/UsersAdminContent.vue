<template>
  <div class="user-admin-wrapper">
    <header class="admin_header">
      <strong>User Settings</strong>
      <UserSearch :loading="loading" @search-changed="doSearch" />
    </header>
    <div
      :class="{ 'user-admin-rows__loading': loading }"
      class="user-admin-rows"
    >
      <div class="user-admin-rows__field user-admin-rows__field-sticky">ID</div>
      <div class="user-admin-rows__field user-admin-rows__field-right">
        <i class="fas user-admin-rows__field-icon"></i>
        Username
      </div>
      <div class="user-admin-rows__field">Full Name</div>
      <div ref="groupsHeader" class="user-admin-rows__field">Groups</div>
      <div class="user-admin-rows__field">Last Login</div>
      <div class="user-admin-rows__field">Signed Up</div>
      <div class="user-admin-rows__field">Active</div>
      <template v-for="user in users">
        <div
          :key="'admin-row-' + user.id + '-1'"
          class="user-admin-rows__cell-sticky user-admin-rows__cell"
        >
          {{ user.id }}
        </div>
        <div
          :key="'admin-row-' + user.id + '-2'"
          class="user-admin-rows__cell-sticky user-admin-rows__cell-right user-admin-rows__cell"
        >
          <UsernameField
            :user="user"
            @update="onUserChange"
            @delete-user="onDeleteUser"
          ></UsernameField>
        </div>
        <div :key="'admin-row-' + user.id + '-3'" class="user-admin-rows__cell">
          {{ user.full_name }}
        </div>
        <div :key="'admin-row-' + user.id + '-4'" class="user-admin-rows__cell">
          <UserGroupsField
            :groups="user.groups"
            :user-id="user.id"
            :parent-width="groupWidth"
          />
        </div>
        <div :key="'admin-row-' + user.id + '-5'" class="user-admin-rows__cell">
          {{ toLocal(user.last_login) }}
        </div>
        <div :key="'admin-row-' + user.id + '-6'" class="user-admin-rows__cell">
          {{ toLocal(user.date_joined) }}
        </div>
        <div :key="'admin-row-' + user.id + '-7'" class="user-admin-rows__cell">
          <div v-if="user.is_active">
            <i class="fas fa-fw fa-check user-admin-rows__active-icon"></i>
            Active
          </div>
          <div v-else>
            <i class="fas fa-fw fa-times user-admin-rows__deactive-icon"></i>
            Deactivated
          </div>
        </div>
      </template>
    </div>
    <div class="user-admin-rows__foot">
      <Paginator
        :total-pages="totalPages"
        :page="page"
        @change-page="fetchPage"
      ></Paginator>
    </div>
  </div>
</template>

<script>
import UserAdminService from '@baserow_premium/services/userAdmin'
import { notifyIf } from '@baserow/modules/core/utils/error'
import UsernameField from '@baserow_premium/components/admin/user/UsernameField'
import moment from 'moment'
import UserGroupsField from '@baserow_premium/components/admin/user/UserGroupsField'
import ResizeObserver from 'resize-observer-polyfill'
import UserSearch from '@baserow_premium/components/admin/user/UserSearch'
import Paginator from '@baserow/modules/core/components/Paginator'

export default {
  name: 'UsersAdminContent',
  components: { UserSearch, UserGroupsField, UsernameField, Paginator },
  props: {},
  data() {
    return {
      loading: false,
      page: 1,
      totalPages: null,
      users: [],
      groupWidth: 0,
    }
  },
  async fetch() {
    await this.fetchPage(1)
  },
  mounted() {
    this.$el.resizeObserver = new ResizeObserver(this.onResize)
    this.$el.resizeObserver.observe(this.$el)
  },
  beforeDestroy() {
    this.$el.resizeObserver.unobserve(this.$el)
  },
  methods: {
    onResize() {
      this.$nextTick(() => {
        if (this.$refs.groupsHeader) {
          this.groupWidth = this.$refs.groupsHeader.clientWidth
        }
      })
    },
    toLocal(date) {
      return moment.utc(date).local().format('L LT')
    },
    async doSearch(searchQuery) {
      this.totalPages = null
      await this.fetchPage(1, { searchQuery })
    },
    /**
     * Fetches the rows of a given page and adds them to the state. If a search query
     * has been stored in the state then that will be remembered.
     */
    async fetchPage(page, { searchQuery = '' } = {}) {
      this.loading = true

      try {
        const { data: userData } = await UserAdminService(
          this.$client
        ).fetchPage(page, searchQuery)
        this.page = page
        this.visiblePage = page
        this.totalPages = Math.ceil(userData.count / 100)
        this.users = userData.results
        this.onResize()
      } catch (error) {
        notifyIf(error, 'row')
      }

      this.loading = false
    },
    onUserChange(newUser) {
      const i = this.users.findIndex((u) => u.id === newUser.id)
      this.users.splice(i, 1, newUser)
    },
    onDeleteUser(userId) {
      const i = this.users.findIndex((u) => u.id === userId)
      this.users.splice(i, 1)
    },
  },
}
</script>
