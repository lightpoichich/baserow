<template>
  <Modal>
    <h2 class="modal__title">
      {{ $t('changeUserPasswordModal.changePassword', user) }}
    </h2>
    <div class="modal__content">
      <Error :error="error"></Error>
      <ChangePasswordForm
        ref="form"
        :loading="loading"
        @submitted="changePassword"
      />
    </div>

    <div class="modal__footer">
      <Button
        type="primary"
        :disabled="loading"
        :loading="loading"
        @click="$refs.form.submit()"
      >
        {{ $t('changePasswordForm.changePassword') }}</Button
      >
    </div>
  </Modal>
</template>

<script>
import modal from '@baserow/modules/core/mixins/modal'
import error from '@baserow/modules/core/mixins/error'
import UserAdminService from '@baserow_premium/services/admin/users'
import ChangePasswordForm from '@baserow_premium/components/admin/users/forms/ChangePasswordForm'

export default {
  name: 'ChangePasswordModal',
  components: { ChangePasswordForm },
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
    async changePassword(values) {
      this.loading = true
      this.hideError()

      try {
        await UserAdminService(this.$client).update(this.user.id, {
          password: values.password,
        })
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
