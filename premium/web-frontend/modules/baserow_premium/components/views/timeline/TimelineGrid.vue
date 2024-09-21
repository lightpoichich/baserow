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
        v-show="slot.item !== undefined"
        :key="'c' + slot.id"
        :style="{
          transform: `translateX(${slot.position.left || 0}px)`,
          width: `${columnWidth}px`,
          height: `${gridHeight}px`,
        }"
        class="timeline-grid__column"
        :class="{ 'timeline-grid__column--weekend': slot.item?.isWeekend }"
      ></div>
    </template>
    <template v-for="slot in rowsBuffer">
      <div
        v-show="slot.item !== undefined"
        :key="'r' + slot.id"
        v-tooltip="
          `${slot.item?.startDate?.format(
            'll'
          )} -> ${slot.item?.endDate?.format('ll')}`
        "
        :style="{
          transform: `translateY(${slot.position.top || 0}px) translateX(${
            slot.item?.startOffset || 0
          }px)`,
          height: `${rowHeight}px`,
          width: `${slot.item?.width || 0}px`,
        }"
        class="timeline-grid__row"
        tooltip-position="bottom-cursor"
      >
        <div v-if="slot.item" class="timeline-grid__row-event">
          <div>{{ slot.item.title }}</div>
        </div>

        <div
          v-if="slot.item?.showGotoStartIcon"
          v-tooltip="slot.item.startDate.format('ll')"
          tooltip-position="bottom-right"
          :style="{
            transform: `translateX(${scrollLeft - slot.item.startOffset}px)`,
          }"
          class="timeline-grid__row-goto-start"
          @click="$emit('goto-start', slot.item.startDate)"
        >
          <i class="iconoir-arrow-left"></i>
        </div>

        <div
          v-if="slot.item?.showGotoEndIcon"
          v-tooltip="slot.item.endDate.format('ll')"
          tooltip-position="bottom-left"
          :style="{
            transform: `translateX(${
              scrollRight - slot.item.startOffset - 22
            }px)`,
          }"
          class="timeline-grid__row-goto-end"
          @click="$emit('goto-end', slot.item.endDate)"
        >
          <i class="iconoir-arrow-right"></i>
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
    scrollLeft: {
      type: Number,
      required: true,
    },
    scrollRight: {
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
