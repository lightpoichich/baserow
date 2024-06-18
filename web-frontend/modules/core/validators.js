/*
  In case the password validation rules change the PasswordInput component
  needs to be updated as well in order to display possible new error messages
  
  modules/core/components/helpers/PasswordInput.vue
*/
import { decimal, maxLength, minLength, required } from 'vuelidate/lib/validators'

export const passwordValidation = {
  required,
  maxLength: maxLength(256),
  minLength: minLength(8),
}

/**
 * Checks whether the provided string is in number range format.
 * Number range format is two decimals separated by a question mark.
 * Examples: 1?10, .1?.9, -100?-50
 * @param {String} value The string to check
 * @returns true if the string is in number range format
 */
export const numberRangeValidation = (value) => {
  const parts = value.split("?")
  if (parts.length !== 2) return false

  const low = parts[0].trim()
  const high = parts[1].trim()
  return required(low) && decimal(low) && required(high) && decimal(high)
}
