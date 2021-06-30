<template>
  <div class="form-view__sidebar">
    <div class="form-view__sidebar-fields">
      <div class="form-view__sidebar-fields-head">
        <div class="form-view__sidebar-fields-title">Fields</div>
        <ul class="form-view__sidebar-fields-actions">
          <li v-show="fields.length > 0">
            <a @click="updateFieldOptionsOfAllFields(view, { enabled: true })"
              >add all</a
            >
          </li>
          <li v-show="enabledFields.length > 0">
            <a @click="updateFieldOptionsOfAllFields(view, { enabled: false })"
              >remove all</a
            >
          </li>
        </ul>
      </div>
      <div v-if="fields.length > 0" class="form-view__sidebar-fields-list">
        <div
          v-for="field in fields"
          :key="field.id"
          v-sortable="{
            id: field.id,
            update: order,
          }"
          class="form-view__sidebar-fields-item-wrapper"
        >
          <a
            class="form-view__sidebar-fields-item"
            @click="updateFieldOptionsOfField(view, field, { enabled: true })"
          >
            <i
              class="form-view__sidebar-fields-icon fas"
              :class="'fa-' + field._.type.iconClass"
            ></i>
            <div class="form-view__sidebar-fields-name">
              {{ field.name }}
            </div>
          </a>
        </div>
      </div>
      <p v-else class="form-view__sidebar-fields-description">
        All the fields are in the form.
      </p>
      <div>
        <a
          ref="createFieldContextLink"
          @click="$refs.createFieldContext.toggle($refs.createFieldContextLink)"
        >
          <i class="fas fa-plus"></i>
          Create new field
        </a>
        <CreateFieldContext
          ref="createFieldContext"
          :table="table"
        ></CreateFieldContext>
      </div>
    </div>
  </div>
</template>

<script>
import CreateFieldContext from '@baserow/modules/database/components/field/CreateFieldContext'
import formViewHelpers from '@baserow/modules/database/mixins/formViewHelpers'

export default {
  name: 'FormViewSidebar',
  components: { CreateFieldContext },
  mixins: [formViewHelpers],
  props: {
    table: {
      type: Object,
      required: true,
    },
    view: {
      type: Object,
      required: true,
    },
    fields: {
      type: Array,
      required: true,
    },
    enabledFields: {
      type: Array,
      required: true,
    },
  },
  methods: {
    order(order) {
      this.$emit('ordered-fields', order)
    },
  },
}
</script>
