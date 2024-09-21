<template>
  <div class="timeline-view">
    <TimelineContainer
      :store-prefix="storePrefix"
      :fields="fields"
      :view="view"
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

<style scoped>
.timeline-view {
  position: absolute;
  top: 0;
  width: 100%;
  height: 100%;
}
</style>
