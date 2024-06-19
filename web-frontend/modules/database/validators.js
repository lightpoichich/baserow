import { decimal, required } from 'vuelidate/lib/validators'
import { COMBINED_FILTER_VALUE_SEPARATOR } from '@baserow/modules/database/constants'

/**
 * Checks whether the provided string is in number range format.
 * Number range format is two decimals separated by COMBINED_FILTER_VALUE_SEPARATOR.
 * Examples assuming '?' separator: 1?10, .1?.9, -100?-50
 * @param {String} value The string to check
 * @returns true if the string is in number range format
 */
export const numberRangeValidator = (value) => {
    const parts = value.split(COMBINED_FILTER_VALUE_SEPARATOR)
    if (parts.length !== 2) return false

    const low = parts[0].trim()
    const high = parts[1].trim()
    return required(low) && decimal(low) && required(high) && decimal(high)
}
