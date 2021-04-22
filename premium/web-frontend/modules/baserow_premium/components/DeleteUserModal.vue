<template>
  <Modal>
    <h2 class="box__title">Delete {{ user.username }}</h2>
    <Error :error="error"></Error>
    <div>
      <p>
        Are you sure you want to delete the user
        <strong>{{ user.username }}</strong
        >?
      </p>
      <p>
        The user account will be deleted, however the groups that user is a
        member of will continue existing. If the user is the only member of the
        group said group will still not be deleted. Deleting the last user in a
        group prevents anyone being able to access that group.
      </p>
      <p>
        After deleting a user it is possible for a new user to sign up again
        using the deleted users email address. To ensure they cannot sign up
        again instead deactivate the user and do not delete them.
      </p>
      <div class="actions">
        <div class="align-right">
          <button
            class="button button--large button--error"
            :class="{ 'button--loading': loading }"
            :disabled="loading"
            @click="deleteUser()"
          >
            Delete user {{ user.username }}
          </button>
        </div>
      </div>
    </div>
  </Modal>
</template>

<script>
import modal from '@baserow/modules/core/mixins/modal'
import error from '@baserow/modules/core/mixins/error'
import UserAdminService from '@baserow_premium/services/userAdmin'

export default {
  name: 'DeleteUserModal',
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
    async deleteUser() {
      this.hideError()
      this.loading = true

      try {
        await UserAdminService(this.$client).delete(this.user.id)
        this.$emit('delete-user', this.user.id)
        this.hide()
      } catch (error) {
        this.handleError(error, 'application')
      }

      this.loading = false
    },
  },
}
</script>
