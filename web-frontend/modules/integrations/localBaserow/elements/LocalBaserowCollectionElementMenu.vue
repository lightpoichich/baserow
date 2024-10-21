<template>
  <div>
    <ul class="header__filter">
      <li class="header__filter-item">
        <ViewFilter
          v-if="filterableFields.length"
          read-only
          :view="view"
          :fields="filterableFields"
          :disable-filter="disableFilters"
          @changed="handleFilterChange"
        ></ViewFilter>
      </li>
    </ul>
  </div>
</template>

<script>
import ViewFilter from '@baserow/modules/database/components/view/ViewFilter'

export default {
  components: { ViewFilter },
  props: {
    element: {
      type: Object,
      required: true,
    },
    dataSource: {
      type: Object,
      required: true,
    },
  },
  data() {
    return {
      view: {
        filters: [],
        filter_groups: [],
        filter_type: 'AND',
        _: { loading: false },
      },
      disableFilters: false,
    }
  },
  computed: {
    serviceType() {
      return this.$registry.get('service', this.dataSource?.type)
    },
    dataSourceFields() {
      const schema = this.serviceType.getDataSchema(this.dataSource)
      if (!schema) {
        return []
      }
      const schemaProperties =
        schema.type === 'array' ? schema.items.properties : schema.properties
      return Object.values(schemaProperties)
        .filter(({ metadata }) => metadata)
        .map((prop) => prop.metadata)
    },
    filterableFields() {
      return this.dataSourceFields.filter((field) => {
        const options = this.element.property_options.find((option) => {
          return option.schema_property === `field_${field.id}`
        })
        // TODO: I should re-check the data source property as well, just
        // in case it's changed since the page designer set an option.
        return options ? options.filterable : false
      })
    },
  },
  methods: {
    handleFilterChange(value) {
      this.$emit(
        'refinements-changed',
        this.serviceType.collectionElementMenuPostProcessor(this.view)
      )
    },
  },
}
</script>
