<template>
  <CrudTable :columns="columns" :service="service">
    <template slot="header">
      <strong>User Settings</strong>
    </template>
  </CrudTable>
</template>

<script>
import UserAdminService from '@baserow_premium/services/userAdmin'
import UsernameField from '@baserow_premium/components/admin/user/fields/UsernameField'
import UserGroupsField from '@baserow_premium/components/admin/user/fields/UserGroupsField'
import CrudTable from '@baserow_premium/components/crud_table/CrudTable'
import SimpleField from '@baserow_premium/components/crud_table/fields/SimpleField'
import LocalDateField from '@baserow_premium/components/crud_table/fields/LocalDateField'
import ActiveField from '@baserow_premium/components/admin/user/fields/ActiveField'

export default {
  name: 'UserAdminTable',
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
        cellComponent: SimpleField,
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
        minWidth: '200px',
        maxWidth: 'max-content',
      },
      {
        key: 'full_name',
        header: 'Full Name',
        isInLeftSection: false,
        hasRightBar: false,
        cellComponent: SimpleField,
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
