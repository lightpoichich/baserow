<template>
  <Modal>
    <h2 class="box__title">Edit {{ user.username }}</h2>
    <Error :error="error"></Error>
    <div>
      <form @submit.prevent="editUser">
        <div class="control">
          <label class="control__label">Full name</label>
          <div class="control__elements">
            <input
              ref="name"
              v-model="formUser.name"
              :class="{ 'input--error': $v.formUser.name.$error }"
              type="text"
              class="input input--large"
              :disabled="loading"
              @blur="$v.formUser.name.$touch()"
            />
            <div v-if="$v.formUser.name.$error" class="error">
              Please enter a valid full name, it must be longer than 2 letters
              and less than 30.
            </div>
          </div>
        </div>
        <label class="control__label">Email</label>
        <div class="control">
          <div class="control__elements">
            <input
              ref="email"
              v-model="formUser.username"
              :class="{ 'input--error': $v.formUser.username.$error }"
              type="text"
              class="input input--large"
              :disabled="loading"
              @blur="$v.formUser.username.$touch()"
            />
            <div v-show="$v.formUser.username.$error" class="error">
              Please enter a valid e-mail address.
            </div>
            <div v-show="formUser.username !== user.username" class="warning">
              Changing this users email address means when they sign in they
              must use the new email address to do so. This must be communicated
              with that user.
            </div>
          </div>
        </div>
        <label class="control__label">Is active</label>
        <div class="control">
          <div class="control__elements">
            <Checkbox
              v-model="formUser.isActive"
              :disabled="loading"
            ></Checkbox>
          </div>
          <div v-show="!formUser.isActive" class="warning">
            When a user is marked as inactive they are prevented from signing
            in.
          </div>
        </div>
        <label class="control__label">Is staff</label>
        <div class="control">
          <div class="control__elements">
            <Checkbox v-model="formUser.isStaff" :disabled="loading"></Checkbox>
          </div>
          <div v-show="formUser.isStaff" class="warning">
            Making the user staff gives them admin access to all users, all
            groups and the ability to revoke your own staff permissions.
          </div>
        </div>
        <div class="actions">
          <div class="align-left">
            <a class="button button--large button--error" @click="deleteUser()">
              Delete User
            </a>
          </div>
          <div class="align-right">
            <button
              class="button button--large button--primary"
              :class="{ 'button--loading': loading }"
              :disabled="loading"
            >
              Save
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
import { email, maxLength, minLength, required } from 'vuelidate/lib/validators'

export default {
  name: 'EditUserModal',
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
      formUser: {
        username: this.editUserEvent.user.username,
        name: this.editUserEvent.user.name,
        isActive: this.editUserEvent.user.is_active,
        isStaff: this.editUserEvent.user.is_staff,
      },
    }
  },
  computed: {
    user() {
      return this.editUserEvent.user
    },
  },
  watch: {
    editUserEvent(editUserEvent) {
      // Reset the form if the user prop changes to a new user.
      this.formUser.username = editUserEvent.user.username
      this.formUser.name = editUserEvent.user.name
      this.formUser.isActive = editUserEvent.user.is_active
      this.formUser.isStaff = editUserEvent.user.is_staff
    },
  },
  methods: {
    deleteUser() {
      this.$emit('switch-to-delete')
    },
    async editUser() {
      this.$v.$touch()
      if (this.$v.$invalid) {
        return
      }
      this.loading = true
      this.hideError()

      try {
        const { data: userData } = await UserAdminService(this.$client).update(
          this.user.id,
          {
            is_staff: this.formUser.isStaff,
            is_active: this.formUser.isActive,
            username: this.formUser.username,
            name: this.formUser.name,
          }
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
  validations: {
    formUser: {
      name: { required, minLength: minLength(2), maxLength: maxLength(30) },
      username: { required, email },
    },
  },
}
</script>
