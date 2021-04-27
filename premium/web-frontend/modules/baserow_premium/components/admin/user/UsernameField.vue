<template>
  <div class="user-admin-rows__username">
    <div class="user-admin-rows__username--initials">
      {{ firstTwoInitials }}
    </div>
    {{ user.username }}
    <i
      v-if="user.is_staff"
      v-tooltip="'is staff'"
      class="user-admin-rows__username--icon fas fa-users"
    ></i>
    <a
      ref="contextLink"
      class="user-admin-rows__username--menu"
      @click.prevent="
        $refs.context.toggle($refs.contextLink, 'bottom', 'left', 4)
      "
    >
      <i class="fas fa-ellipsis-h"></i>
    </a>
    <EditUserContext
      ref="context"
      :user="user"
      @delete-user="$emit('delete-user', $event)"
      @update="$emit('update', $event)"
    >
    </EditUserContext>
  </div>
</template>

<script>
import EditUserContext from '@baserow_premium/components/admin/user/EditUserContext'

export default {
  name: 'UsernameField',
  components: {
    EditUserContext,
  },
  props: {
    user: {
      required: true,
      type: Object,
    },
  },
  computed: {
    firstTwoInitials() {
      return this.user.full_name
        .split(' ')
        .map((s) => s.slice(0, 1))
        .join('')
        .slice(0, 2)
        .toUpperCase()
    },
  },
}
</script>
