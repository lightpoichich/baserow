<template>
  <div class="timeline-view">
    <TimelineContainer
      :fields="fields"
      :view="view"
      :table="table"
      :database="database"
      :read-only="readOnly"
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
import TimelineContainer from './TimelineContainer.vue'

export default {
  name: 'TimelineView',
  components: {
    TimelineContainer,
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
}
</script>
