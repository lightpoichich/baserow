<template>
  <div class="form-view">
    <FormViewSidebar
      :table="table"
      :view="view"
      :fields="disabledFields"
      :enabled-fields="enabledFields"
      :store-prefix="storePrefix"
    ></FormViewSidebar>
    <FormViewPreview
      :table="table"
      :view="view"
      :fields="enabledFields"
      :store-prefix="storePrefix"
    ></FormViewPreview>
  </div>
</template>

<script>
import { maxPossibleOrderValue } from '@baserow/modules/database/viewTypes'
import formViewHelpers from '@baserow/modules/database/mixins/formViewHelpers'
import FormViewSidebar from '@baserow/modules/database/components/view/form/FormViewSidebar'
import FormViewPreview from '@baserow/modules/database/components/view/form/FormViewPreview'

export default {
  name: 'FormView',
  components: { FormViewSidebar, FormViewPreview },
  mixins: [formViewHelpers],
  props: {
    primary: {
      type: Object,
      required: true,
    },
    fields: {
      type: Array,
      required: true,
    },
    view: {
      type: Object,
      required: true,
    },
    table: {
      type: Object,
      required: true,
    },
    database: {
      type: Object,
      required: true,
    },
    readOnly: {
      type: Boolean,
      required: true,
    },
  },
  computed: {
    sortedFields() {
      const fields = this.fields.slice()
      fields.unshift(this.primary)
      return fields.sort((a, b) => {
        const orderA = this.getFieldOption(a.id, 'order', maxPossibleOrderValue)
        const orderB = this.getFieldOption(b.id, 'order', maxPossibleOrderValue)

        // First by order.
        if (orderA > orderB) {
          return 1
        } else if (orderA < orderB) {
          return -1
        }

        // Then by id.
        if (a.id < b.id) {
          return -1
        } else if (a.id > b.id) {
          return 1
        } else {
          return 0
        }
      })
    },
    disabledFields() {
      return this.sortedFields.filter((field) => {
        return !this.getFieldOption(field.id, 'enabled', false)
      })
    },
    enabledFields() {
      return this.sortedFields.filter((field) => {
        return this.getFieldOption(field.id, 'enabled', false)
      })
    },
  },
  methods: {
    getFieldOption(fieldId, value, fallback) {
      return this.fieldOptions[fieldId]
        ? this.fieldOptions[fieldId][value]
        : fallback
    },
  },
}
</script>
