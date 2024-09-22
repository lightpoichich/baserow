<template>
  <div class="timeline-view">
    <div v-if="needsDateFields && canChooseDateField">
      <InitTimelineViewSettings
        :fields="fields"
        :view="view"
        :read-only="readOnly"
        :store-prefix="storePrefix"
      />
    </div>
    <TimelineContainer
      v-else
      :fields="fields"
      :view="view"
      :table="table"
      :database="database"
      :read-only="readOnly"
      :show-rows="!needsDateFields"
      :store-prefix="storePrefix"
      @selected-row="$emit('selected-row', $event)"
      @refresh="$emit('refresh', $event)"
      @navigate-previous="$emit('navigate-previous', $event)"
      @navigate-next="$emit('navigate-next', $event)"
    />
  </div>
</template>
<script>
import viewHelpers from '@baserow/modules/database/mixins/viewHelpers'
import InitTimelineViewSettings from '@baserow_premium/components/views/timeline/InitTimelineViewSettings'
import TimelineContainer from '@baserow_premium/components/views/timeline/TimelineContainer.vue'

export default {
  name: 'TimelineView',
  components: {
    TimelineContainer,
    InitTimelineViewSettings,
  },
  mixins: [viewHelpers],
  props: {
    database: {
      type: Object,
      required: true,
    },
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
    readOnly: {
      type: Boolean,
      required: true,
    },
    loading: {
      type: Boolean,
      required: true,
    },
    storePrefix: {
      type: String,
      required: true,
    },
  },
  computed: {
    canChooseDateField() {
      return (
        !this.readOnly &&
        this.$hasPermission(
          'database.table.view.update',
          this.view,
          this.database.workspace.id
        )
      )
    },
    needsDateFields() {
      const startDatefield = this.fields.find(
        (f) => f.id === this.view.start_date_field
      )
      const endDatefield = this.fields.find(
        (f) => f.id === this.view.start_date_field
      )
      if (!startDatefield || !endDatefield) {
        return true
      } else {
        const startDateType = this.$registry.get('field', startDatefield.type)
        const endDateType = this.$registry.get('field', endDatefield.type)
        return (
          !startDateType.canRepresentDate(startDatefield) ||
          !endDateType.canRepresentDate(endDatefield)
        )
      }
    },
  },
}
</script>
