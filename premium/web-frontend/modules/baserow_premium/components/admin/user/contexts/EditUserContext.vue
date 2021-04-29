<template>
  <Context v-if="selectedUser">
    <ul class="context__menu">
      <li>
        <a @click.prevent="showEditModal">
          <i class="context__menu-icon fas fa-fw fa-pen"></i>
          Edit
        </a>
      </li>
      <li>
        <a @click.prevent="showChangePasswordModal">
          <i class="context__menu-icon fas fa-fw fa-key"></i>
          Change password
        </a>
      </li>
      <li>
        <a v-if="selectedUser.user.is_active" @click.prevent="deactivate">
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
      :user="selectedUser.user"
      @delete-user="$emit('delete-user', $event)"
    ></DeleteUserModal>
    <EditUserModal
      ref="editUserModal"
      :user="selectedUser.user"
      @update="$emit('update', $event)"
      @switch-to-delete="showDeleteModal"
    >
    </EditUserModal>
    <ChangePasswordModal ref="changePasswordModal" :user="selectedUser.user">
    </ChangePasswordModal>
  </Context>
</template>

<script>
import ChangePasswordModal from '@baserow_premium/components/admin/user/modals/ChangeUserPasswordModal'
import context from '@baserow/modules/core/mixins/context'
import DeleteUserModal from '@baserow_premium/components/admin/user/modals/DeleteUserModal'
import EditUserModal from '@baserow_premium/components/admin/user/modals/EditUserModal'
import UserAdminService from '@baserow_premium/services/userAdmin'
import { notifyIf } from '@baserow/modules/core/utils/error'

export default {
  name: 'EditUserContext',
  components: {
    ChangePasswordModal,
    DeleteUserModal,
    EditUserModal,
  },
  mixins: [context],
  props: {
    selectedUser: {
      required: true,
      validator: (prop) => typeof prop === 'object' || prop === null,
    },
  },
  watch: {
    selectedUser(selectedUser) {
      if (selectedUser) {
        this.$nextTick(function () {
          this.hide()
          this.show(selectedUser.contextLink, 'bottom', 'left', 4)
        })
      }
    },
  },
  methods: {
    showChangePasswordModal() {
      this.hide()
      this.$refs.changePasswordModal.show()
    },
    showDeleteModal() {
      this.hide()
      this.$refs.deleteUserModal.show()
    },
    showEditModal() {
      this.hide()
      this.$refs.editUserModal.show()
    },
    async changeIsActive(isActive) {
      try {
        const { data: newUser } = await UserAdminService(
          this.$client
        ).update(this.selectedUser.user.id, { is_active: isActive })

        this.hide()
        this.$emit('update', newUser)
      } catch (error) {
        notifyIf(error, 'settings')
      }
    },
    async activate() {
      await this.changeIsActive(true)
    },
    async deactivate() {
      await this.changeIsActive(false)
    },
  },
}
</script>
