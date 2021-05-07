<template>
  <Modal>
    <h2 class="box__title">Change password for {{ user.username }}</h2>
    <Error :error="error"></Error>
    <div>
      <form @submit.prevent="changePassword">
        <div class="control">
          <label class="control__label">New Password</label>
          <div class="control__elements">
            <input
              v-model="account.password"
              :class="{ 'input--error': $v.account.password.$error }"
              type="password"
              class="input input--large"
              @blur="$v.account.password.$touch()"
            />
            <div
              v-if="$v.account.password.$error && !$v.account.password.required"
              class="error"
            >
              A password is required.
            </div>
            <div
              v-if="
                $v.account.password.$error && !$v.account.password.maxLength
              "
              class="error"
            >
              A maximum of
              {{ $v.account.password.$params.maxLength.max }} characters is
              allowed here.
            </div>
            <div
              v-if="
                $v.account.password.$error && !$v.account.password.minLength
              "
              class="error"
            >
              A minimum of
              {{ $v.account.password.$params.minLength.min }} characters is
              required here.
            </div>
          </div>
        </div>
        <div class="control">
          <label class="control__label">Repeat password</label>
          <div class="control__elements">
            <input
              v-model="account.passwordConfirm"
              :class="{ 'input--error': $v.account.passwordConfirm.$error }"
              type="password"
              class="input input--large"
              @blur="$v.account.passwordConfirm.$touch()"
            />
            <div v-if="$v.account.passwordConfirm.$error" class="error">
              This field must match your password field.
            </div>
          </div>
        </div>
        <div class="actions">
          <div class="align-right">
            <button
              class="button button--large button--primary"
              :class="{ 'button--loading': loading }"
              :disabled="loading"
            >
              Change password
            </button>
          </div>
        </div>
      </form>
    </div>
  </Modal>
</template>

<script>
import modal from '@baserow/modules/core/mixins/modal'
import error from '@baserow/modules/core/mixins/error'
import UserAdminService from '@baserow_premium/services/userAdmin'
import {
  maxLength,
  minLength,
  required,
  sameAs,
} from 'vuelidate/lib/validators'

export default {
  name: 'ChangePasswordModal',
  mixins: [modal, error],
  props: {
    editUserEvent: {
      type: Object,
      required: true,
    },
  },
  data() {
    return {
      loading: false,
      account: {
        password: '',
        passwordConfirm: '',
      },
    }
  },
  computed: {
    user() {
      return this.editUserEvent.user
    },
  },
  watch: {
    // Reset the form if the user prop changes to a new user.
    editUserEvent() {
      this.hideError()
      this.account.password = ''
      this.account.passwordConfirm = ''
    },
  },
  methods: {
    async changePassword() {
      this.$v.$touch()
      if (this.$v.$invalid) {
        return
      }
      this.loading = true
      this.hideError()

      try {
        await UserAdminService(this.$client).update(this.user.id, {
          password: this.account.password,
        })
        this.loading = false
        this.hide()
      } catch (error) {
        this.loading = false
        this.handleError(error, 'application')
      }
    },
  },
  validations: {
    account: {
      password: {
        required,
        maxLength: maxLength(256),
        minLength: minLength(8),
      },
      passwordConfirm: {
        sameAsPassword: sameAs('password'),
      },
    },
  },
}
</script>
