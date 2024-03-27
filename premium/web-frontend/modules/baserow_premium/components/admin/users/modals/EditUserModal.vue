<template>
  <Modal @hidden="$refs.form && $refs.form.reset()">
    <h2 class="modal__title">
      {{ $t('editUserModal.edit', { username: user.username }) }}
    </h2>
    <div class="modal__content">
      <Error :error="error"></Error>
      <UserForm
        ref="form"
        :user="user"
        :loading="loading"
        :default-values="user"
        @submitted="editUser"
      >
      </UserForm>
    </div>

    <div class="modal__footer">
      <Button type="danger" @click="$refs.deleteUserModal.show()">
        {{ $t('editUserModal.delete') }}
      </Button>

      <Button
        type="primary"
        :disabled="loading"
        :loading="loading"
        @click="$refs.form.submit()"
      >
        {{ $t('action.save') }}</Button
      >
    </div>
    <DeleteUserModal
      ref="deleteUserModal"
      :user="user"
      @delete-user="$emit('delete-user', $event)"
    ></DeleteUserModal>
  </Modal>
</template>

<script>
import modal from '@baserow/modules/core/mixins/modal'
import error from '@baserow/modules/core/mixins/error'
import UserAdminService from '@baserow_premium/services/admin/users'
import UserForm from '@baserow_premium/components/admin/users/forms/UserForm'
import DeleteUserModal from '@baserow_premium/components/admin/users/modals/DeleteUserModal'

export default {
  name: 'EditUserModal',
  components: { DeleteUserModal, UserForm },
  mixins: [modal, error],
  props: {
    user: {
      type: Object,
      required: true,
    },
  },
  data() {
    return {
      loading: false,
    }
  },
  methods: {
    async editUser(values) {
      this.loading = true
      this.hideError()

      try {
        const { data: userData } = await UserAdminService(this.$client).update(
          this.user.id,
          values
        )
        this.$emit('update', userData)
        this.loading = false
        this.hide()
      } catch (error) {
        this.loading = false
        this.handleError(error, 'application')
      }
    },
  },
}
</script>
