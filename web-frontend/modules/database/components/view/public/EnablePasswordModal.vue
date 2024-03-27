<template>
  <Modal small>
    <h2 class="modal__title">{{ $t(titleText) }}</h2>

    <div class="modal__content">
      <Error :error="error"></Error>
      <form ref="form" @submit.prevent="setPassword">
        <p>{{ $t(descriptionText) }}</p>
        <FormGroup :error="fieldHasErrors('password')">
          <PasswordInput
            v-model="values.password"
            :validation-state="$v.values.password"
            :show-password-icon="true"
            :disabled="loading"
          />
        </FormGroup>
      </form>
    </div>

    <div class="modal__footer">
      <Button type="secondary" :disabled="loading" @click.prevent="hide()">
        {{ $t('action.cancel') }}
      </Button>
      <Button
        type="primary"
        :loading="loading"
        :disabled="loading || $v.$invalid"
        @click="setPassword()"
      >
        {{ $t(saveText) }}
      </Button>
    </div>
  </Modal>
</template>

<script>
import form from '@baserow/modules/core/mixins/form'
import modal from '@baserow/modules/core/mixins/modal'
import error from '@baserow/modules/core/mixins/error'
import { passwordValidation } from '@baserow/modules/core/validators'
import PasswordInput from '@baserow/modules/core/components/helpers/PasswordInput'

export default {
  name: 'ShareViewPasswordModal',
  components: { PasswordInput },
  mixins: [form, modal, error],
  props: {
    view: {
      type: Object,
      required: true,
    },
  },
  data() {
    return {
      loading: false,
      allowedValues: ['password'],
      values: {
        password: '',
      },
    }
  },
  computed: {
    change() {
      return this.view.public_view_has_password
    },
    titleText() {
      return this.change
        ? 'shareViewEnablePasswordModal.changePasswordTitle'
        : 'shareViewEnablePasswordModal.newPasswordTitle'
    },
    descriptionText() {
      return this.change
        ? 'shareViewEnablePasswordModal.changePasswordDescription'
        : 'shareViewEnablePasswordModal.newPasswordDescription'
    },
    saveText() {
      return this.change
        ? 'shareViewEnablePasswordModal.changePasswordSave'
        : 'shareViewEnablePasswordModal.newPasswordSave'
    },
  },
  methods: {
    clearInput() {
      this.values.password = ''
      this.$v.$reset()
    },
    show() {
      this.clearInput()
      modal.methods.show.bind(this)()
      this.$nextTick(() => {
        this.$el.querySelector('input')?.focus()
      })
    },
    async setPassword() {
      this.hideError()
      this.loading = true

      const view = this.view
      try {
        await this.$store.dispatch('view/update', {
          view,
          values: { public_view_password: this.values.password },
        })

        this.hide()
      } catch (error) {
        this.handleError(error, 'table')
      }

      this.loading = false
    },
  },
  validations: {
    values: {
      password: passwordValidation,
    },
  },
}
</script>
