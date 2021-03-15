/**
 * This mixin contains some method overrides for validating and formatting the
 * phone number field. This mixin is used in both the GridViewFieldPhoneNumber and
 * RowEditFieldPhoneNumber components.
 */
export default {
  methods: {
    /**
     * Generates a human readable error for the user if something is wrong.
     */
    getError() {
      if (this.copy === null || this.copy === '') {
        return null
      }
      // TODO Do validation
      return null
    },
    isValid() {
      return this.getError() === null
    },
  },
}
