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
          transform: `translateX(${slot.position.left}px)`,
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
        v-tooltip="rowTooltip(slot)"
        :style="{
          transform: `translateY(${slot.position.top}px) translateX(${
            slot.item?.startOffset || 0
          }px)`,
          height: `${rowHeight}px`,
          width: `${slot.item?.width}px`,
        }"
        class="timeline-grid__row"
        tooltip-position="bottom-cursor"
      >
        <div
          v-show="slot.item"
          class="timeline-grid__row-event"
          @click="$emit('edit-row', slot.item)"
        >
          <RecursiveWrapper
            :components="wrapperComponent(slot)"
            first-component-class="timeline-grid__row-event-label-decoration"
          >
            <component
              :is="dec.component"
              v-for="dec in slot.item?.firstCellDecorations"
              :key="dec.decoration.id"
              v-bind="dec.propsFn(slot.item.row)"
            />
            <div
              :ref="`label-${slot.id}`"
              class="timeline-grid__row-event-label"
              :style="{
                transform: `translateX(${getLabelOffset(slot)}px)`,
              }"
            >
              {{ slot.item?.label }}
            </div>
          </RecursiveWrapper>
        </div>

        <div
          v-if="slot.item?.showGotoStartIcon"
          v-tooltip="slot.item.startDate.format('ll')"
          tooltip-position="bottom-right"
          :style="{
            transform: `translateX(${scrollLeft - slot.item.startOffset}px)`,
          }"
          class="timeline-grid__row-goto-start"
          @click="
            scrollLeft > slot.item.endOffset &&
            slot.item.width >= scrollRight - scrollLeft
              ? $emit('goto-end', slot.item.endDate)
              : $emit('goto-start', slot.item.startDate)
          "
        >
          <i class="iconoir-arrow-left"></i>
        </div>

        <div
          v-if="slot.item && (!slot.item?.startDate || !slot.item?.endDate)"
          v-tooltip="slot.item.title"
          tooltip-position="bottom-right"
          :style="{
            transform: `translateX(${scrollLeft}px)`,
          }"
          class="timeline-grid__row-expand"
          @click="$emit('edit-row', slot.item)"
        >
          <i class="iconoir-expand"></i>
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
          @click="
            scrollRight < slot.item.startOffset &&
            slot.item.width >= scrollRight - scrollLeft
              ? $emit('goto-start', slot.item.startDate)
              : $emit('goto-end', slot.item.endDate)
          "
        >
          <i class="iconoir-arrow-right"></i>
        </div>
      </div>
    </template>

    <div
      v-if="scrollNow > 0"
      :style="{
        transform: `translateX(${scrollNow}px)`,
        height: `${gridHeight}px`,
      }"
      class="timeline-grid__now-cursor"
    ></div>
  </div>
</template>

<script>
import moment from '@baserow/modules/core/moment'
import RecursiveWrapper from '@baserow/modules/database/components/RecursiveWrapper'
import EmptyEventWrapper from '@baserow_premium/components/views/timeline/EmptyEventWrapper'

export default {
  name: 'TimelineGrid',
  components: { RecursiveWrapper },
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
    scrollNow: {
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
    minHeight: {
      type: Number,
      required: true,
    },
  },
  computed: {
    gridHeight() {
      return Math.max(this.rowHeight * this.rowCount, this.minHeight)
    },
    gridWidth() {
      return this.columnCount * this.columnWidth
    },
  },
  methods: {
    wrapperComponent(slot) {
      const decoration = slot.item?.wrapperDecorations.map((comp) => ({
        ...comp,
        props: comp.propsFn(slot.item?.row),
      }))
      return decoration?.length
        ? decoration
        : [{ component: EmptyEventWrapper }]
    },
    formatDate(date, format) {
      return moment(date).format(format)
    },
    getLabelOffset(slot) {
      const label = this.$refs[`label-${slot.id}`]
      if (!label || !slot.item?.showGotoStartIcon) {
        return 0
      }
      const offset = this.scrollLeft - slot.item.startOffset
      const padding = 30
      if (offset > slot.item.width - label[0].clientWidth - 2 * padding) {
        return 0
      }
      return offset + padding
    },
    rowTooltip(slot) {
      if (!slot.item || !slot.item.startDate || !slot.item.endDate) {
        return ''
      }

      const sameYear = slot.item.startDate.year() === slot.item.endDate.year()
      const format = sameYear ? 'MMM D' : 'MMM D, YYYY'
      const startDate = slot.item.startDate.format(format)
      const endDate = slot.item.endDate.format(format)
      const duration = slot.item.endDate.diff(slot.item.startDate, 'days') + 1
      return `${startDate} -> ${endDate} (${duration} days)`
    },
  },
}
</script>
