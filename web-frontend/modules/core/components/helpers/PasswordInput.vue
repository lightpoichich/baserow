<!--
This component can be used in a form which requires password validation.
The password requirements for baserow are encapsulated in this component.

In order to use this component in another component/form it needs a passwordValue
prop. That means the state for the passwordValue always lives in a parent component.
The parent component needs to provide a function in order to update the state.
When the input is changed this component emits an 'inputChange' event with the event.

In order to access the validation of this component in the parent component a 'ref'
needs to be added to the component. With that the vuelidate instance can be accessed:

e.g. this.$refs.REFNAME.$v

Example Usage:

<PasswordInput
   ref="password"
   label="New Password"
   name="password"
   :password-value="PASSWORDSTATE"
   @inputChange="handleChange"
/>

-->
<template>
  <div>
    <label class="control__label">{{ label }}</label>
    <div class="control__elements">
      <input
        :class="{ 'input--error': $v.passwordValue.$error }"
        :name="name"
        :value="passwordValue"
        type="password"
        class="input input--large"
        @blur="$v.passwordValue.$touch()"
        @input="(event) => this.$emit('inputChange', event)"
      />
      <div
        v-if="$v.passwordValue.$error && !$v.passwordValue.required"
        class="error"
      >
        Input is required.
      </div>
      <div
        v-if="$v.passwordValue.$error && !$v.passwordValue.maxLength"
        class="error"
      >
        A maximum of
        {{ $v.passwordValue.$params.maxLength.max }} characters is allowed here.
      </div>
      <div
        v-if="$v.passwordValue.$error && !$v.passwordValue.minLength"
        class="error"
      >
        A minimum of
        {{ $v.passwordValue.$params.minLength.min }} characters is required
        here.
      </div>
    </div>
  </div>
</template>

<script>
import { maxLength, minLength, required } from 'vuelidate/lib/validators'

export default {
  name: 'PasswordInput',
  props: {
    label: {
      type: String,
      required: true,
    },
    passwordValue: {
      type: String,
      required: true,
    },
    name: {
      type: String,
      required: true,
    },
  },
  methods: {
    isFormValid() {
      this.$v.passwordValue.$touch()
      return !this.$v.$invalid
    },
  },
  validations: {
    passwordValue: {
      required,
      maxLength: maxLength(256),
      minLength: minLength(8),
    },
  },
}
</script>
