<template>
  <div class="timeline-sidebar" :style="{height: `${rowHeight * rowCount}px`}">
    <template v-for="slot in rowsBuffer" >
      <div
        :key="slot.id"
        :style="{ transform: `translateY(${rowsBuffer[0]?.position.top || 0}px)`, height: `${rowHeight}px` }"
        class="timeline-sidebar__event"
        v-show="slot.item !== undefined"
      >
        <div v-if="slot.item">
          {{ getRowTitle(slot.item) }}
        </div>
        <div v-else>Loading...</div>
      </div>
    </template>
  </div>
</template>

<script>
export default {
  name: 'TimelineSidebar',
  props: {
    rowsBuffer: {
      type: Array,
      required: true,
    },
    fields: {
      type: Array,
      required: true,
    },
    rowCount: {
      type: Number,
      required: true,
    },
    rowHeight: {
      type: Number,
      required: true,
    },
  },
  methods: {
    getRowTitle(row) {
      const primaryField = this.fields.find((field) => field.primary)
      return row[`field_${primaryField.id}`]
    },
  },
}
</script>

<style scoped>
.timeline-sidebar {
  position: absolute;
  top: 0;
  height: 100%;
  width: 200px;
}

.timeline-sidebar__event {  
  width: 100%;
  border: 1px solid grey;
}
</style>
