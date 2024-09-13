<template>
  <div class="timeline-container">
    <div
      :style="{ height: `${viewHeaderHeight}px` }"
      class="timeline-container__header"
    >
      <ViewDateIndicator
        v-if="firstVisibleDate"
        :selectedDate="firstVisibleDate"
      />
      <ViewDateSelector
        v-if="firstVisibleDate"
        :selectedDate="firstVisibleDate"
        @date-selected="selectDate"
      />
    </div>
    <div
      ref="gridHeader"
      :style="{ height: `${gridHeaderHeight}px` }"
      class="timeline-container__grid-header"
    >
      <TimelineGridHeader
        :columnsBuffer="columnsBuffer"
        :columnCount="columns.length"
        :columnWidth="columnWidth"
      />
    </div>
    <div
      ref="gridBody"
      :style="{
        height: `calc(100% - ${gridBodyHeightOffset}px)`,
      }"
      class="timeline-container__grid-body"
    >
      <!-- <TimelineSidebar
        ref="sidebar"
        :rowsBuffer="rowsBuffer"
        :rowCount="rowCount"
        :fields="fields"
        :rowHeight="rowHeight"
      /> -->
      <TimelineGrid
        :columnsBuffer="columnsBuffer"
        :columnCount="columns.length"
        :columnWidth="columnWidth"
        :rowsBuffer="rowsBuffer"
        :rowHeight="rowHeight"
        :rowCount="rowCount"
      />
      <TimelineGridOverlay
        v-if="$refs.gridBody"
        :style="{
          left: `${scrollAreaElement?.scrollLeft}px`,
          width: `${gridWidth}px`,
        }"
        :rowsBuffer="rowsBuffer"
        :rowHeight="rowHeight"
        :rowCount="rowCount"
        @goto-start="
          ($event) =>
            scrollHorizontal(
              (dateDiff(firstAvailableDate, $event) - 5) * columnWidth,
              'smooth'
            )
        "
        @goto-end="
          ($event) =>
            scrollHorizontal(
              (dateDiff(firstAvailableDate, $event) -
                this.visibleColumnCount +
                5) *
                columnWidth,
              'smooth'
            )
        "
      />
    </div>
  </div>
</template>
<script>
import Vue from 'vue'
import ResizeObserver from 'resize-observer-polyfill'
import debounce from 'lodash/debounce'
import moment from '@baserow/modules/core/moment'
import {
  recycleSlots,
  orderSlots,
} from '@baserow/modules/database/utils/virtualScrolling'
import ViewDateIndicator from '@baserow_premium/components/views/ViewDateIndicator'
import ViewDateSelector from '@baserow_premium/components/views/ViewDateSelector'
import TimelineSidebar from '@baserow_premium/components/views/timeline/TimelineSidebar.vue'
import TimelineGrid from '@baserow_premium/components/views/timeline/TimelineGrid.vue'
import TimelineGridOverlay from '@baserow_premium/components/views/timeline/TimelineGridOverlay.vue'
import TimelineGridHeader from '@baserow_premium/components/views/timeline/TimelineGridHeader.vue'

export default {
  name: 'TimelineContainer',
  components: {
    TimelineSidebar,
    TimelineGrid,
    TimelineGridHeader,
    TimelineGridOverlay,
    ViewDateIndicator,
    ViewDateSelector,
  },
  props: {
    view: {
      type: Object,
      required: true,
    },
    fields: {
      type: Array,
      required: true,
    },
    storePrefix: {
      type: String,
      required: true,
    },
  },
  data() {
    return {
      rowHeight: 32,
      minColumnWidth: 32,
      columnWidth: 32,
      rowsBuffer: [],
      columnsBuffer: [],
      columns: [],
      prevScrollTop: 0,
      prevScrollLeft: 0,
      sidebarWidth: 240,
      gridWidth: 0,
      gridHeight: 0,
      gridHeaderHeight: 32,
      viewHeaderHeight: 72,
      // monthly view settings
      visibleColumnCount: 31,
      unit: 'day',
      range: 'month',
      firstAvailableDate: moment().subtract(1, 'year').startOf('year'),
      lastAvailableDate: moment().add(1, 'year').endOf('year'),
      firstVisibleDate: null,
    }
  },
  computed: {
    rows() {
      return this.$store.getters[this.storePrefix + 'view/timeline/getRows']
    },
    rowCount() {
      return this.rows.length
    },
    containerHeight() {
      return this.rowsCount * this.rowHeight
    },
    startDateField() {
      return this.fields.find(
        (field) => field.id === this.view.start_date_field
      )
    },
    endDateField() {
      return this.fields.find((field) => field.id === this.view.end_date_field)
    },
    primaryField() {
      return this.fields.find((field) => field.primary)
    },
    scrollAreaElement() {
      return this.$refs.gridBody
    },
    gridBodyHeightOffset() {
      return this.viewHeaderHeight + this.gridHeaderHeight
    },
  },
  mounted() {
    const updateRowsOrderDebounced = debounce(
      this.fetchMissingRowsAndUpdateBuffer,
      100
    )

    this.setupGrid()

    const onScroll = () => {
      const el = this.scrollAreaElement
      if (el.scrollTop !== this.prevScrollTop) {
        this.prevScrollTop = el.scrollTop
        updateRowsOrderDebounced()
      }
      if (el.scrollLeft !== this.prevScrollLeft) {
        this.prevScrollLeft = el.scrollLeft
        this.updateGridColumns()
        this.updateRowsBufferEventFlags()
        this.$refs.gridHeader.scroll({ left: el.scrollLeft })
      }
    }

    const el = this.scrollAreaElement
    el.addEventListener('scroll', onScroll)
    this.$once('hook:beforeDestroy', () => {
      el.removeEventListener('scroll', onScroll)
    })

    const resizeObserver = new ResizeObserver(() => {
      this.setupGrid()
    })
    resizeObserver.observe(el)
    this.$once('hook:beforeDestroy', () => {
      resizeObserver.unobserve(el)
    })
  },
  methods: {
    dateDiff(startDate, endDate, includeEnd = true) {
      return endDate.diff(startDate, this.unit) + (includeEnd ? 1 : 0)
    },
    setupGrid() {
      this.updateGridDimensions()
      this.setupGridColumns()
      this.updateRowsBuffer()
      this.updateRowsBufferEventFlags()
    },
    updateGridDimensions() {
      const el = this.scrollAreaElement
      this.gridWidth = el.clientWidth
      this.gridHeight = Math.max(el.clientHeight, el.scrollHeight)
      this.columnWidth = Math.max(
        this.gridWidth / this.visibleColumnCount,
        this.minColumnWidth
      )
    },
    getVisibleRowsRange() {
      const el = this.scrollAreaElement
      const elHeight = el.clientHeight
      const minRowsToRender = Math.ceil(elHeight / this.rowHeight) + 1
      let startIndex = Math.floor(el.scrollTop / this.rowHeight)
      let endIndex = startIndex + minRowsToRender
      if (endIndex > this.rowsCount) {
        endIndex = this.rowsCount
        startIndex = Math.max(0, endIndex - minRowsToRender)
      }
      return { startIndex, endIndex }
    },
    getVisibleColumnsRange() {
      const el = this.scrollAreaElement
      if (!el) {
        return { startIndex: 0, endIndex: 0 }
      }
      let startIndex = Math.floor(el.scrollLeft / this.columnWidth)
      let endIndex = startIndex + this.visibleColumnCount + 1
      if (endIndex > this.columns.length) {
        endIndex = this.columns.length
        startIndex = Math.max(0, endIndex - this.visibleColumnCount)
      }
      return { startIndex, endIndex }
    },
    async fetchMissingRowsAndUpdateBuffer() {
      this.updateRowsBuffer(false) // Show the loading state for the missing rows.

      const range = this.getVisibleRowsRange()
      await this.$store.dispatch(
        this.storePrefix + 'view/timeline/fetchMissingRowsInNewRange',
        range
      )
      this.updateRowsBuffer()
      this.updateRowsBufferEventFlags()
    },
    getRowDate(row, field) {
      // TODO: use format and proper timezone
      const rowValue = row[`field_${field.id}`]
      return rowValue ? moment(rowValue) : null
    },
    updateRowsBufferEventFlags() {
      // Based on the visible columns, we want to set if we need to show the
      // icon to go the the event start or end date.
      const { startIndex, endIndex } = this.getVisibleColumnsRange()
      this.rowsBuffer.forEach((slot, index) => {
        if (!slot.item) {
          return
        }
        const showGotoStartIcon = slot.item.startIndex < startIndex
        const showGotoEndIcon = slot.item.endIndex > endIndex
        const needsUpdate =
          showGotoStartIcon !== slot.item.showGotoStartIcon ||
          showGotoEndIcon !== slot.item.showGotoEndIcon
        if (needsUpdate) {
          slot.item.showGotoStartIcon = showGotoStartIcon
          slot.item.showGotoEndIcon = showGotoEndIcon
          if (slot.item.id === 8) {
            console.log(
              'updateRowsBufferEventFlags',
              showGotoStartIcon,
              showGotoEndIcon
            )
          }
          // Force a re-render of the slot.
          const item = slot.item
          slot.item = null
          slot.item = item
        }
      })
    },
    setupRowEvent(row) {
      if (row === null) {
        return null
      }
      const startDate = this.getRowDate(row, this.startDateField)
      const startIndex = startDate
        ? this.dateDiff(this.firstAvailableDate, startDate)
        : null
      const startOffset = startIndex ? startIndex * this.columnWidth : null
      const endDate = this.getRowDate(row, this.endDateField)
      const endIndex = endDate
        ? this.dateDiff(this.firstAvailableDate, endDate)
        : null
      const endOffset = endIndex ? endIndex * this.columnWidth : null
      const width =
        endIndex && startIndex ? (endIndex - startIndex) * this.columnWidth : 0
      const title = row[`field_${this.primaryField.id}`]
      return {
        id: row.id,
        title,
        startDate,
        endDate,
        startIndex,
        endIndex,
        startOffset,
        endOffset,
        width,
        row,
      }
    },
    updateRowsBuffer(sort = true) {
      const { startIndex, endIndex } = this.getVisibleRowsRange()
      const visibleRows = this.rows
        .slice(startIndex, endIndex)
        .map(this.setupRowEvent)
      const getPosition = (row, pos) => ({
        top: (startIndex + pos) * this.rowHeight,
        left: row?.startIndex ? row.startIndex * this.columnWidth : -1,
      })
      const rowsToRender = endIndex - startIndex
      recycleSlots(this.rowsBuffer, visibleRows, getPosition, rowsToRender)
      if (sort) {
        orderSlots(this.rowsBuffer, visibleRows)
      }
    },
    setupGridColumns() {
      this.columns = Array.from(
        {
          length: this.dateDiff(
            this.firstAvailableDate,
            this.lastAvailableDate
          ),
        },
        (_, i) => ({
          id: i,
          date: moment(this.firstAvailableDate).add(i, this.unit),
        })
      )

      const firstVisibleDate = moment().startOf(this.range)
      const firstVisibleIndex = this.dateDiff(
        this.firstAvailableDate,
        firstVisibleDate,
        false
      )
      this.$nextTick(() =>
        this.scrollHorizontal(firstVisibleIndex * this.columnWidth)
      )
    },
    updateGridColumns() {
      const { startIndex, endIndex } = this.getVisibleColumnsRange()
      const visibleColumns = this.columns.slice(startIndex, endIndex)
      const getPosition = (col, pos) => ({
        left: (startIndex + pos) * this.columnWidth,
      })
      this.firstVisibleDate = this.firstAvailableDate
        .clone()
        .add(startIndex + 1, this.unit)
      recycleSlots(this.columnsBuffer, visibleColumns, getPosition)
    },
    scrollHorizontal(left, behavior = 'instant') {
      this.scrollAreaElement.scroll({ left, behavior })
      this.$refs.gridHeader.scroll({ left, behavior })
    },
    selectDate(date) {
      const firstVisibleDate = date.startOf(this.range)
      const firstVisibleIndex = this.dateDiff(
        this.firstAvailableDate,
        firstVisibleDate,
        false
      )
      this.scrollHorizontal(firstVisibleIndex * this.columnWidth, 'smooth')
    },
  },
}
</script>

<style>
.timeline-container {
  height: 100%;
  width: 100%;
  background-color: white;
  position: relative;
}

.timeline-container__grid-header {
  width: 100%;
  overflow: hidden;
}

.timeline-container__grid-body {
  width: 100%;
  overflow: auto;
  position: relative;
}

.timeline-container__header {
  display: flex;
  justify-content: space-between;
}
</style>
