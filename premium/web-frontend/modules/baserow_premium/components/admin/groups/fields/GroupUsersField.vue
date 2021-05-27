<script>
import UserGroupsField from '@baserow_premium/components/admin/users/fields/UserGroupsField'

export default {
  name: 'GroupUsersField',
  extends: UserGroupsField,
  data() {
    return {
      eventName: 'show-hidden-users',
      nameKey: 'email',
    }
  },
}
</script>
