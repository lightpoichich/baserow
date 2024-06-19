import { decimal, required } from 'vuelidate/lib/validators'
import { COMBINED_FILTER_VALUE_SEPARATOR } from '@baserow/modules/database/constants'

/**
 * Checks whether the provided string is in number range format.
 * Number range format is two decimals separated by a delimiter.
 * Examples assuming '?' delimiter: 1?10, .1?.9, -100?-50
 * @param {String} value The string to check
 * @param {String} separator The string to use as a delimiter
 * @returns true if the string is in number range format
 */
export const numberRangeValidator = (value, separator = COMBINED_FILTER_VALUE_SEPARATOR) => {
    const parts = value.split(separator)
    if (parts.length !== 2) return false

    const low = parts[0].trim()
    const high = parts[1].trim()
    return required(low) && decimal(low) && required(high) && decimal(high)
}
