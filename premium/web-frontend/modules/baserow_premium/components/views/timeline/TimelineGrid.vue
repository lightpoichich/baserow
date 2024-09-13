<template>
  <div
    class="timeline-grid"
    :style="{
      height: `${gridHeight}px`,
      width: `${gridWidth}px`,
    }"
  >
    <template v-for="slot in columnsBuffer">
      <div
        :key="'c' + slot.id"
        :style="{
          transform: `translateX(${slot.position.left || 0}px)`,
          width: `${columnWidth}px`,
          height: `${gridHeight}px`,
        }"
        class="timeline-grid__column"
        v-show="slot.item !== undefined"
      ></div>
    </template>
    <template v-for="slot in rowsBuffer">
      <div
        :key="'r' + slot.id"
        :style="{
          transform: `translateY(${slot.position.top || 0}px) translateX(${
            slot.item?.startOffset || 0
          }px)`,
          height: `${rowHeight}px`,
          width: `${slot.item?.width || 0}px`,
        }"
        class="timeline-grid__row"
        v-show="slot.item !== undefined"
      >
        <div v-if="slot.item" class="timeline-grid__row-event">
          <div>{{ slot.item.title }}</div>
        </div>
      </div>
    </template>
  </div>
</template>

<script>
import moment from '@baserow/modules/core/moment'

export default {
  name: 'TimelineGrid',
  props: {
    columnsBuffer: {
      type: Array,
      required: true,
    },
    columnWidth: {
      type: Number,
      required: true,
    },
    columnCount: {
      type: Number,
      required: true,
    },
    rowsBuffer: {
      type: Array,
      required: true,
    },
    rowHeight: {
      type: Number,
      required: true,
    },
    rowCount: {
      type: Number,
      required: true,
    },
  },
  computed: {
    gridHeight() {
      return this.rowHeight * this.rowCount
    },
    gridWidth() {
      return this.columnCount * this.columnWidth
    },
  },
  methods: {
    formatDate(date, format) {
      return moment(date).format(format)
    },
  },
}
</script>
