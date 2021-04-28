<template>
  <CrudTable :columns="columns" :service="service">
    <template slot="header">
      <strong>User Settings</strong>
    </template>
  </CrudTable>
</template>

<script>
import UserAdminService from '@baserow_premium/services/userAdmin'
import UsernameField from '@baserow_premium/components/admin/user/UsernameField'
import UserGroupsField from '@baserow_premium/components/admin/user/UserGroupsField'
import CrudTable from '@baserow_premium/components/crud_table/CrudTable'
import SimpleCell from '@baserow_premium/components/crud_table/SimpleCell'
import LocalDateField from '@baserow_premium/components/crud_table/LocalDateField'
import ActiveField from '@baserow_premium/components/admin/user/ActiveField'

export default {
  name: 'UsersAdminContent',
  components: {
    CrudTable,
  },
  data() {
    this.columns = [
      {
        key: 'id',
        header: 'ID',
        isInLeftSection: true,
        hasRightBar: false,
        cellComponent: SimpleCell,
        minWidth: 'min-content',
        maxWidth: 'max-content',
      },
      {
        key: 'username',
        header: 'Username',
        icon: 'fa-sort-down',
        isInLeftSection: true,
        hasRightBar: true,
        cellComponent: UsernameField,
        minWidth: '100px',
        maxWidth: '300px',
      },
      {
        key: 'full_name',
        header: 'Full Name',
        isInLeftSection: false,
        hasRightBar: false,
        cellComponent: SimpleCell,
        minWidth: '100px',
        maxWidth: '200px',
      },
      {
        key: 'groups',
        header: 'Groups',
        isInLeftSection: false,
        hasRightBar: false,
        cellComponent: UserGroupsField,
        minWidth: '100px',
        maxWidth: '500px',
      },
      {
        key: 'last_login',
        header: 'Last Login',
        isInLeftSection: false,
        hasRightBar: false,
        cellComponent: LocalDateField,
        minWidth: 'min-content',
        maxWidth: '200px',
      },
      {
        key: 'date_joined',
        header: 'Signed Up',
        isInLeftSection: false,
        hasRightBar: false,
        cellComponent: LocalDateField,
        minWidth: 'min-content',
        maxWidth: '200px',
      },
      {
        key: 'is_active',
        header: 'Active',
        isInLeftSection: false,
        hasRightBar: false,
        cellComponent: ActiveField,
        minWidth: 'min-content',
        maxWidth: '200px',
      },
    ]
    this.service = UserAdminService(this.$client)
    return {}
  },
}
</script>
