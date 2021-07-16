<template>
  <form @submit.prevent="submit">
    <div class="control">
      <PasswordInput
        ref="password"
        label="New Password"
        name="password"
        :password-value="values.password"
        @inputChange="handleChange"
      />
    </div>
    <div class="control">
      <label class="control__label">Repeat password</label>
      <div class="control__elements">
        <input
          v-model="values.passwordConfirm"
          :class="{ 'input--error': $v.values.passwordConfirm.$error }"
          type="password"
          class="input input--large"
          @blur="$v.values.passwordConfirm.$touch()"
        />
        <div v-if="$v.values.passwordConfirm.$error" class="error">
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
</template>

<script>
import { sameAs } from 'vuelidate/lib/validators'
import PasswordInput from '@baserow/modules/core/components/helpers/PasswordInput'

import form from '@baserow/modules/core/mixins/form'

export default {
  name: 'ChangePasswordForm',
  components: { PasswordInput },
  mixins: [form],
  props: {
    loading: {
      type: Boolean,
      required: true,
    },
  },
  data() {
    return {
      allowedValues: ['password', 'passwordConfirm'],
      values: {
        password: '',
        passwordConfirm: '',
      },
    }
  },
  methods: {
    handleChange(event) {
      const { value, name } = event.target
      this.values[name] = value
    },
  },
  validations: {
    values: {
      passwordConfirm: {
        sameAsPassword: sameAs('password'),
      },
    },
  },
}
</script>
