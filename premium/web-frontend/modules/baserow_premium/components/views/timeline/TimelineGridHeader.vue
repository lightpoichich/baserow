<template>
  <div
    class="timeline-grid-header"
    :style="{
      height: `${headerHeight}px`,
      width: `${gridWidth}px`,
    }"
  >
    <template v-for="slot in columnsBuffer">
      <div
        :key="'h' + slot.id"
        :style="{
          transform: `translateX(${slot.position.left || 0}px)`,
          width: `${columnWidth}px`,
          height: `${headerHeight}px`,
        }"
        class="timeline-grid-header__column"
        v-show="slot.item !== undefined"
      >
        <div>{{ formatDate(slot.item.date, 'D') }}</div>
      </div>
    </template>
  </div>
</template>

<script>
import moment from '@baserow/modules/core/moment'

export default {
  name: 'TimelineGridHeader',
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
    headerHeight: {
      type: Number,
      default: 32,
    },
  },
  computed: {
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