<template>
  <a
    class="filters__value-link-row"
    :class="{ 'filters__value-link-row--disabled': readOnly }"
    @click.prevent="!readOnly && $refs.selectModal.show()"
  >
    <div v-if="loading" class="loading-absolute-center"></div>
    <div v-else-if="!valid" class="filters__value-link-row-choose">
      Choose row
    </div>
    <template v-else>
      {{ name || `unnamed row ${value}` }}
    </template>
    <SelectRowModal
      v-if="!readOnly"
      ref="selectModal"
      :table-id="field.link_row_table"
      @selected="setValue"
    ></SelectRowModal>
  </a>
</template>

<script>
import SelectRowModal from '@baserow/modules/database/components/row/SelectRowModal'

export default {
  name: 'ViewFilterTypeLinkRow',
  components: { SelectRowModal },
  props: {
    value: {
      type: String,
      required: true,
    },
    fieldId: {
      type: Number,
      required: true,
    },
    primary: {
      type: Object,
      required: true,
    },
    fields: {
      type: Array,
      required: true,
    },
    preloadValues: {
      type: Object,
      required: true,
    },
    readOnly: {
      type: Boolean,
      required: true,
    },
  },
  data() {
    return {
      name: '',
      loading: false,
    }
  },
  computed: {
    field() {
      return this.primary.id === this.fieldId
        ? this.primary
        : this.fields.find((f) => f.id === this.fieldId)
    },
    valid() {
      return this.isValidValue(this.value)
    },
  },
  watch: {
    preloadValues(value) {
      this.setNameFromPreloadValues(value)
    },
  },
  mounted() {
    this.setNameFromPreloadValues(this.preloadValues)
  },
  methods: {
    setNameFromRow(row, primary) {
      this.name = this.$registry
        .get('field', primary.type)
        .toHumanReadableString(primary, row[`field_${primary.id}`])
    },
    setNameFromPreloadValues(values) {
      const displayName = values.display_name
      this.name = displayName || ''
    },
    isValidValue() {
      if (isNaN(parseInt(this.value))) {
        return false
      }

      return true
    },
    setValue({ row, primary }) {
      this.setNameFromRow(row, primary)
      this.$emit('input', row.id.toString())
    },
  },
}
</script>
