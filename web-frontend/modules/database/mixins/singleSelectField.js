import FieldSingleSelectDropdown from '@baserow/modules/database/components/field/FieldSingleSelectDropdown'

export default {
  components: { FieldSingleSelectDropdown },
  computed: {
    valueId() {
      return this.value !== null ? this.value.id : null
    },
  },
  methods: {
    /**
     * Checks if the new value is the same as the old value and if not it will be
     * updated.
     */
    updateValue(newId, oldValue) {
      const newValue =
        this.field.select_options.find((option) => option.id === newId) || null
      const oldId = oldValue !== null ? oldValue.id : null

      if (newId !== oldId) {
        this.$emit('update', newValue, oldValue)
      }
    },
  },
}
