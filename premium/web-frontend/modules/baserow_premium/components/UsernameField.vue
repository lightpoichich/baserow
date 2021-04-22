<template>
  <div class="user-admin-rows__username">
    <div class="user-admin-rows__username--initials">
      {{ firstTwoInitials }}
    </div>
    {{ user.username }}
    <i v-if="user.is_staff" v-tooltip="'is staff'" class="fas fa-users"></i>
    <a
      ref="contextLink"
      class="user-admin-rows__username--menu"
      @click.prevent="
        $refs.context.toggle($refs.contextLink, 'bottom', 'left', 4)
      "
    >
      <i class="fas fa-ellipsis-h"></i>
    </a>
    <Context ref="context">
      <ul class="context__menu">
        <li>
          <a>
            <i class="context__menu-icon fas fa-fw fa-pen"></i>
            Edit
          </a>
        </li>
        <li>
          <a>
            <i class="context__menu-icon fas fa-fw fa-key"></i>
            Change password
          </a>
        </li>
        <li>
          <a v-if="user.is_active" @click.prevent="deactivate">
            <i class="context__menu-icon fas fa-fw fa-times"></i>
            Deactivate
          </a>
          <a v-else @click.prevent="activate">
            <i class="context__menu-icon fas fa-fw fa-check"></i>
            Activate
          </a>
        </li>
        <li>
          <a @click.prevent="showDeleteModal">
            <i class="context__menu-icon fas fa-fw fa-trash-alt"></i>
            Permanently delete
          </a>
        </li>
      </ul>
      <DeleteUserModal
        ref="deleteUserModal"
        :user="user"
        @delete-user="$emit('delete-user', $event)"
      ></DeleteUserModal>
    </Context>
  </div>
</template>

<script>
import UserAdminService from '@baserow_premium/services/userAdmin'
import DeleteUserModal from '@baserow_premium/components/DeleteUserModal'

export default {
  name: 'UsernameField',
  components: { DeleteUserModal },
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
  methods: {
    showDeleteModal() {
      this.$refs.context.hide()
      this.$refs.deleteUserModal.show()
    },
    async activate() {
      const { data: newUser } = await UserAdminService(this.$client).update(
        this.user.id,
        { is_active: true }
      )

      this.$refs.context.hide()
      this.$emit('update', newUser)
    },
    async deactivate() {
      const { data: newUser } = await UserAdminService(this.$client).update(
        this.user.id,
        { is_active: false }
      )
      this.$refs.context.hide()

      this.$emit('update', newUser)
    },
  },
}
</script>
