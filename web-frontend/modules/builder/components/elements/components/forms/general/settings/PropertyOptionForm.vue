<template>
  <div>
    <p class="margin-bottom-2">
      {{ $t('propertyOptionForm.formDescription') }}
    </p>
    <BaserowTable class="property-option-table" :fields="fields" :rows="rows">
      <template #cell-content="{ rowIndex, value, field }">
        <td v-if="field.isOption" :key="field.name" class="baserow-table__cell">
          <Checkbox
            v-tooltip="
              optionIsDisabled(rows[rowIndex], field.name)
                ? $t('propertyOptionForm.optionUnavailable')
                : null
            "
            tooltip-position="top"
            :checked="value"
            :disabled="optionIsDisabled(rows[rowIndex], field.name)"
            @input="onOptionChange(rows[rowIndex], field.property, $event)"
          ></Checkbox>
        </td>
        <td v-else :key="field.name" class="baserow-table__cell">
          <template v-if="value.length > 15">
            <span :title="value">{{ value.slice(0, 15) + '...' }}</span>
          </template>
          <template v-else>{{ value }}</template>
        </td>
      </template>
    </BaserowTable>
  </div>
</template>

<script>
import BaserowTable from '@baserow/modules/builder/components/elements/components/BaserowTable'

export default {
  name: 'PropertyOptionForm',
  components: { BaserowTable },
  inject: ['page'],
  props: {
    element: {
      type: Object,
      required: true,
    },
    schema: {
      type: Object,
      required: true,
    },
  },
  computed: {
    /**
     * Returns an object with schema properties as keys and their corresponding
     * property options as values. It's a convenience computed method to easily
     * access property options by schema property.
     * @returns {object} - The grouped property options.
     */
    propertyGroupedOptions() {
      return Object.fromEntries(
        this.element.property_options.map((po) => [po.schema_property, po])
      )
    },
    /**
     * Returns an array of objects that represent the table fields.
     * Each field is flagged as `isOption` if it represents a user
     * configurable property option.
     * @returns {Array} - The table fields.
     */
    fields() {
      return [
        { name: 'Field', property: null, isOption: false },
        { name: 'Filter', property: 'filterable', isOption: true },
        { name: 'Sort', property: 'sortable', isOption: true },
        { name: 'Search', property: 'searchable', isOption: true },
      ]
    },
    rows() {
      return Object.entries(this.schema.properties)
        .filter(
          ([_, propertyValues]) =>
            propertyValues.sortable ||
            propertyValues.filterable ||
            propertyValues.searchable
        )
        .map(([schemaProperty, propertyValues]) => ({
          schemaProperty,
          propertyValues,
          Field: propertyValues.title,
          Filter: this.getOptionValue(
            schemaProperty,
            propertyValues,
            'filterable'
          ),
          Sort: this.getOptionValue(schemaProperty, propertyValues, 'sortable'),
          Search: this.getOptionValue(
            schemaProperty,
            propertyValues,
            'searchable'
          ),
        }))
    },
  },
  methods: {
    /**
     * A convenience method which returns whether a particular option name
     * (e.g. Filter, Sort, Search) is disabled for a given row. This would
     * happen if the schema property specifies that the option is not ever
     * available for this property.
     *
     * @param row - The row object.
     * @param optionName - The option name to check.
     * @returns {boolean} - Whether the option is disabled.
     */
    optionIsDisabled(row, optionName) {
      return row[optionName] === null
    },
    getOptionValue(schemaProperty, propertyValues, optionName) {
      if (!propertyValues[optionName]) {
        // The schema has specified that this property is not
        // filterable/sortable/searchable. We return null to inform
        // the template that the checkbox should be disabled.
        return null
      }
      // If we have an existing property option for this property,
      // return whether it's filterable/sortable/searchable. If it hasn't
      // been configured, we default to false for this `optionName`.
      return this.propertyGroupedOptions[schemaProperty]
        ? this.propertyGroupedOptions[schemaProperty][optionName]
        : false
    },
    /**
     * Updates the property option of a schema property.
     *
     * @param row - The row object.
     * @param optionProperty - The property option to update.
     * @param value - The new value for the property option.
     */
    onOptionChange(row, optionProperty, value) {
      let newOptions
      const existingOption = this.element.property_options.find((po) => {
        return po.schema_property === row.schemaProperty
      })
      if (existingOption) {
        newOptions = this.element.property_options.map((propOption) => {
          if (propOption.schema_property === row.schemaProperty) {
            return { ...propOption, ...{ [optionProperty]: value } }
          }
          return propOption
        })
      } else {
        newOptions = [
          ...this.element.property_options,
          { schema_property: row.schemaProperty, [optionProperty]: value },
        ]
      }
      this.$store.dispatch('element/update', {
        page: this.page,
        element: this.element,
        values: { property_options: newOptions },
      })
    },
  },
}
</script>
