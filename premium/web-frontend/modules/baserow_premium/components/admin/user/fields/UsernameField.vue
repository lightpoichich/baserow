<template>
  <div class="user-admin-username">
    <div class="user-admin-username__initials">
      {{ firstTwoInitials }}
    </div>
    <div class="user-admin-username__name">
      {{ row.username }}
    </div>
    <i
      v-if="row.is_staff"
      v-tooltip="'is staff'"
      class="user-admin-username__icon fas fa-users"
    ></i>
    <a
      ref="contextLink"
      class="user-admin-username__menu"
      @click.prevent="
        $refs.context.toggle($refs.contextLink, 'bottom', 'left', 4)
      "
    >
      <i class="fas fa-ellipsis-h"></i>
    </a>
    <EditUserContext
      ref="context"
      :user="row"
      @delete-user="$emit('row-delete', $event)"
      @update="$emit('row-update', $event)"
    >
    </EditUserContext>
  </div>
</template>

<script>
import EditUserContext from '@baserow_premium/components/admin/user/fields/EditUserContext'

export default {
  name: 'UsernameField',
  components: {
    EditUserContext,
  },
  props: {
    row: {
      required: true,
      type: Object,
    },
  },
  computed: {
    firstTwoInitials() {
      return this.row.full_name
        .split(' ')
        .map((s) => s.slice(0, 1))
        .join('')
        .slice(0, 2)
        .toUpperCase()
    },
  },
}
</script>
