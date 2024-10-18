<template>
  <form @submit.prevent>
    <div class="row">
      <div class="col col-12">
        <LocalBaserowTableSelector
          v-model="fakeTableId"
          :databases="databases"
          :view-id.sync="values.view_id"
        ></LocalBaserowTableSelector>
      </div>
    </div>
    <div class="row">
      <div class="col col-6">
        <FormGroup
          small-label
          :label="$t('localBaserowAggregateRowsForm.aggregationFieldLabel')"
          required
        >
          <Dropdown v-model="values.field_id" :disabled="fields.length === 0">
            <DropdownItem
              v-for="field in fields"
              :key="field.id"
              :name="field.name"
              :value="field.id"
            >
            </DropdownItem>
          </Dropdown>
        </FormGroup>
      </div>
      <div class="col col-6">
        <FormGroup
          small-label
          :label="$t('localBaserowAggregateRowsForm.aggregationTypeLabel')"
          required
        >
          <Dropdown
            v-model="values.aggregation_type"
            :disabled="!values.field_id"
          >
            <DropdownItem
              v-for="viewAggregation in viewAggregationTypes"
              :key="viewAggregation.getType()"
              :name="viewAggregation.getName()"
              :value="viewAggregation.getType()"
            >
            </DropdownItem>
          </Dropdown>
        </FormGroup>
      </div>
    </div>
    <div class="margin-top-2 row">
      <div class="col col-12">
        <Tabs>
          <Tab
            :title="$t('localBaserowAggregateRowsForm.filterTabTitle')"
            class="data-source-form__condition-form-tab"
          >
            <LocalBaserowTableServiceConditionalForm
              v-if="values.table_id && values.field_id && dataSource.schema"
              v-model="dataSourceFilters"
              :schema="dataSource.schema"
              :table-loading="tableLoading"
              :filter-type.sync="values.filter_type"
            >
            </LocalBaserowTableServiceConditionalForm>
            <p v-if="!values.table_id || !values.field_id">
              {{
                $t(
                  'localBaserowAggregateRowsForm.noTableOrFieldChosenForFiltering'
                )
              }}
            </p>
          </Tab>
          <Tab
            :title="$t('localBaserowAggregateRowsForm.searchTabTitle')"
            class="data-source-form__search-form-tab"
          >
            <InjectedFormulaInput
              v-model="values.search_query"
              small
              :placeholder="
                $t('localBaserowAggregateRowsForm.searchFieldPlaceHolder')
              "
            />
          </Tab>
        </Tabs>
      </div>
    </div>
  </form>
</template>

<script>
import form from '@baserow/modules/core/mixins/form'
import LocalBaserowTableSelector from '@baserow/modules/integrations/localBaserow/components/services/LocalBaserowTableSelector'
import LocalBaserowTableServiceConditionalForm from '@baserow/modules/integrations/localBaserow/components/services/LocalBaserowTableServiceConditionalForm'
import InjectedFormulaInput from '@baserow/modules/core/components/formula/InjectedFormulaInput'

export default {
  components: {
    InjectedFormulaInput,
    LocalBaserowTableSelector,
    LocalBaserowTableServiceConditionalForm,
  },
  mixins: [form],
  inject: ['page'],
  props: {
    builder: {
      type: Object,
      required: true,
    },
    contextData: { type: Object, required: true },
    dataSource: {
      type: Object,
      required: true,
    },
  },
  data() {
    return {
      allowedValues: [
        'table_id',
        'view_id',
        'field_id',
        'search_query',
        'filters',
        'filter_type',
        'aggregation_type',
      ],
      values: {
        table_id: null,
        view_id: null,
        field_id: null,
        search_query: '',
        filters: [],
        filter_type: 'AND',
        aggregation_type: 'sum',
      },
      tableLoading: false,
    }
  },
  computed: {
    viewAggregationTypes() {
      const selectedField = this.fields.find(
        (field) => field.id === this.values.field_id
      )
      if (!selectedField) return []
      return this.$registry
        .getOrderedList('viewAggregation')
        .filter((agg) => agg.fieldIsCompatible(selectedField))
    },
    dataSourceLoading() {
      return this.$store.getters['dataSource/getLoading'](this.page)
    },
    dataSourceFilters: {
      get() {
        return this.excludeTrashedFields(this.values.filters)
      },
      set(newValue) {
        this.values.filters = newValue
      },
    },
    fakeTableId: {
      get() {
        return this.values.table_id
      },
      set(newValue) {
        // If we currently have a `table_id` selected, and the `newValue`
        // is different to the current `table_id`, then reset the `filters`
        // a blank array, and `view_id` to `null`.
        if (this.values.table_id && this.values.table_id !== newValue) {
          this.values.filters = []
          this.values.view_id = null
        }
        this.values.table_id = newValue
      },
    },
    databases() {
      return this.contextData?.databases || []
    },
    table() {
      return this.databases
        .find((db) => db.tables.some((tbl) => tbl.id === this.values.table_id))
        ?.tables.find((tbl) => tbl.id === this.values.table_id)
    },
    fields() {
      return this.table?.fields || []
    },
  },
  watch: {
    'values.table_id'(newValue, oldValue) {
      if (oldValue && newValue !== oldValue) {
        this.tableLoading = true
      }
    },
    dataSourceLoading: {
      handler() {
        this.tableLoading = false
      },
      immediate: true,
    },
  },
  methods: {
    /**
     * Given an array of objects containing a `field` property (e.g. the data
     * source filters array), this method will return a new array
     * containing only the objects where the field is part of the schema, so,
     * untrashed.
     *
     * @param {Array} value - The array of objects to filter.
     * @returns {Array} - The filtered array.
     */
    excludeTrashedFields(value) {
      const schema = this.dataSource.schema
      const schemaProperties =
        schema.type === 'array' ? schema.items.properties : schema.properties
      const localBaserowFieldIds = Object.values(schemaProperties)
        .filter(({ metadata }) => metadata)
        .map((prop) => prop.metadata.id)
      return value.filter(({ field }) => localBaserowFieldIds.includes(field))
    },
  },
}
</script>
