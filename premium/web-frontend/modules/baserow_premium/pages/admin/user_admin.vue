<template>
  <UsersAdminContent></UsersAdminContent>
</template>

<script>
import UsersAdminContent from '@baserow_premium/components/admin/user/UsersAdminContent'

export default {
  components: { UsersAdminContent },
  layout: 'app',
  middleware: 'staff',
}
</script>
