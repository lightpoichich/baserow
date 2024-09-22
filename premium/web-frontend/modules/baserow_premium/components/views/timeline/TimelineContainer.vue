<template>
  <div class="timeline-container">
    <div
      :style="{ height: `${viewHeaderHeight}px` }"
      class="timeline-container__header"
    >
      <ViewDateIndicator
        v-if="firstVisibleDate"
        :selected-date="firstVisibleDate"
      />
      <ViewDateSelector
        v-if="firstVisibleDate"
        :selected-date="firstVisibleDate"
        @date-selected="selectDate"
      />
    </div>
    <div
      ref="gridHeader"
      :style="{ height: `${gridHeaderHeight}px` }"
      class="timeline-container__grid-header"
    >
      <TimelineGridHeader
        :columns-buffer="columnsBuffer"
        :column-count="columns.length"
        :column-width="columnWidth"
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
        :columns-buffer="columnsBuffer"
        :column-count="columns.length"
        :column-width="columnWidth"
        :rows-buffer="rowsBuffer"
        :row-height="rowHeight"
        :row-count="rowCount"
        :min-height="gridHeight"
        :scroll-left="scrollLeft"
        :scroll-right="scrollRigth"
        :scroll-now="scrollNow"
        @goto-start="scrollToStartDate"
        @goto-end="scrollToEndDate"
        @edit-row="rowClick"
      />
    </div>
    <RowEditModal
      ref="rowEditModal"
      enable-navigation
      :database="database"
      :table="table"
      :view="view"
      :all-fields-in-table="fields"
      :primary-is-sortable="true"
      :visible-fields="visibleFields"
      :hidden-fields="hiddenFields"
      :rows="rows"
      :read-only="
        readOnly ||
        !$hasPermission(
          'database.table.update_row',
          table,
          database.workspace.id
        )
      "
      :show-hidden-fields="showHiddenFieldsInRowModal"
      @hidden="$emit('selected-row', undefined)"
      @toggle-hidden-fields-visibility="
        showHiddenFieldsInRowModal = !showHiddenFieldsInRowModal
      "
      @update="updateValue"
      @order-fields="orderFields"
      @toggle-field-visibility="toggleFieldVisibility"
      @field-updated="$emit('refresh', $event)"
      @field-deleted="$emit('refresh')"
      @field-created="showFieldCreated"
      @field-created-callback-done="afterFieldCreatedUpdateFieldOptions"
      @navigate-previous="$emit('navigate-previous', $event, activeSearchTerm)"
      @navigate-next="$emit('navigate-next', $event, activeSearchTerm)"
      @refresh-row="refreshRow"
    >
    </RowEditModal>
  </div>
</template>
<script>
import { mapGetters } from 'vuex'
import ResizeObserver from 'resize-observer-polyfill'
import debounce from 'lodash/debounce'
import moment from '@baserow/modules/core/moment'
import {
  recycleSlots,
  orderSlots,
} from '@baserow/modules/database/utils/virtualScrolling'
import {
  sortFieldsByOrderAndIdFunction,
  filterVisibleFieldsFunction,
  filterHiddenFieldsFunction,
} from '@baserow/modules/database/utils/view'
import ViewDateIndicator from '@baserow_premium/components/views/ViewDateIndicator'
import ViewDateSelector from '@baserow_premium/components/views/ViewDateSelector'
import TimelineSidebar from '@baserow_premium/components/views/timeline/TimelineSidebar.vue'
import TimelineGrid from '@baserow_premium/components/views/timeline/TimelineGrid.vue'
import TimelineGridHeader from '@baserow_premium/components/views/timeline/TimelineGridHeader.vue'
import RowEditModal from '@baserow/modules/database/components/row/RowEditModal'
import viewHelpers from '@baserow/modules/database/mixins/viewHelpers'
import viewDecoration from '@baserow/modules/database/mixins/viewDecoration'
import { populateRow } from '@baserow/modules/database/store/view/grid'
import { clone } from '@baserow/modules/core/utils/object'
import { notifyIf } from '@baserow/modules/core/utils/error'

export default {
  name: 'TimelineContainer',
  components: {
    TimelineSidebar,
    TimelineGrid,
    TimelineGridHeader,
    ViewDateIndicator,
    ViewDateSelector,
    RowEditModal,
  },
  mixins: [viewHelpers, viewDecoration],
  props: {
    view: {
      type: Object,
      required: true,
    },
    fields: {
      type: Array,
      required: true,
    },
    table: {
      type: Object,
      required: true,
    },
    database: {
      type: Object,
      required: true,
    },
    showRows: {
      type: Boolean,
      required: false,
      default: true,
    },
    readOnly: {
      type: Boolean,
      required: true,
    },
    storePrefix: {
      type: String,
      required: true,
    },
  },
  data() {
    return {
      rowHeight: 38,
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
      gridHeaderHeight: 36,
      viewHeaderHeight: 72,
      scrollLeft: 0,
      scrollRigth: 0,
      scrollNow: 0,
      showHiddenFieldsInRowModal: false,
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
      return this.showRows
        ? this.$store.getters[this.storePrefix + 'view/timeline/getRows']
        : []
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
    visibleFields() {
      const fieldOptions = this.fieldOptions
      return this.fields
        .filter(filterVisibleFieldsFunction(fieldOptions))
        .sort(sortFieldsByOrderAndIdFunction(fieldOptions))
    },
    hiddenFields() {
      const fieldOptions = this.fieldOptions
      return this.fields
        .filter(filterHiddenFieldsFunction(fieldOptions))
        .sort(sortFieldsByOrderAndIdFunction(fieldOptions))
    },
    activeSearchTerm() {
      return this.$store.getters[
        `${this.storePrefix}view/timeline/getActiveSearchTerm`
      ]
    },
    ...mapGetters({
      row: 'rowModalNavigation/getRow',
    }),
  },
  watch: {
    rows() {
      this.$nextTick(() => {
        this.updateRowsBuffer()
        this.updateRowsBufferEventFlags()
      })
    },
    row: {
      deep: true,
      handler(row, oldRow) {
        if (this.$refs.rowEditModal) {
          if (
            (oldRow === null && row !== null) ||
            (oldRow && row && oldRow.id !== row.id)
          ) {
            this.populateAndEditRow(row)
          } else if (oldRow !== null && row === null) {
            // Pass emit=false as argument into the hide function because that will
            // prevent emitting another `hidden` event of the `RowEditModal` which can
            // result in the route changing twice.
            this.$refs.rowEditModal.hide(false)
          }
        }
      },
    },
    visibleFields() {
      this.updateRowsBuffer()
    },
    'view.decorations'() {
      this.updateRowsBuffer()
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
        this.scrollLeft = el.scrollLeft
        this.scrollRigth = el.scrollLeft + this.gridWidth
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

    if (this.row !== null) {
      this.populateAndEditRow(this.row)
    }
  },
  beforeCreate() {
    this.$options.computed = {
      ...(this.$options.computed || {}),
      ...mapGetters({
        fieldOptions:
          this.$options.propsData.storePrefix +
          'view/timeline/getAllFieldOptions',
      }),
    }
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
      this.gridHeight = el.clientHeight
      this.columnWidth = Math.max(
        this.gridWidth / this.visibleColumnCount,
        this.minColumnWidth
      )
      this.scrollLeft = el.scrollLeft
      this.scrollRigth = el.scrollLeft + this.gridWidth
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
      const rowValue = row[`field_${field.id}`]
      if (!rowValue) {
        return null
      }
      const fieldType = this.$registry.get('field', field.type)
      return fieldType.parseInputValue(field, rowValue)
    },
    getRowLabel(row) {
      return this.visibleFields
        .map((f) => {
          const fieldType = this.$registry.get('field', f.type)
          const cellValue = row[`field_${f.id}`]
          return fieldType.toHumanReadableString(f, cellValue)
        })
        .join(' - ')
    },
    updateSlotEventFlags(slot) {
      const { startIndex, endIndex } = this.getVisibleColumnsRange()
      const showGotoStartIcon =
        slot.item.startIndex && slot.item.startIndex < startIndex
      const showGotoEndIcon =
        slot.item.endIndex && slot.item.endIndex > endIndex
      const needsUpdate =
        showGotoStartIcon !== slot.item.showGotoStartIcon ||
        showGotoEndIcon !== slot.item.showGotoEndIcon
      if (needsUpdate) {
        slot.item.showGotoStartIcon = showGotoStartIcon
        slot.item.showGotoEndIcon = showGotoEndIcon
        // Force a re-render of the slot.
        const item = slot.item
        slot.item = null
        slot.item = item
      }
    },
    updateRowsBufferEventFlags() {
      // Based on the visible columns, we want to set if we need to show the
      // icon to go the the event start or end date.
      this.rowsBuffer.forEach((slot, index) => {
        if (!slot.item) {
          return
        }
        this.updateSlotEventFlags(slot)
      })
    },
    setupRowEvent(row) {
      if (row === null) {
        return null
      }
      const event = {
        id: row.id,
        title: row[`field_${this.primaryField.id}`],
        label: this.getRowLabel(row),
        row,
        firstCellDecorations: this.decorationsByPlace?.first_cell || [],
        wrapperDecorations: this.decorationsByPlace?.wrapper || [],
      }
      if (!this.startDateField || !this.endDateField) {
        return event
      }
      const startDate = this.getRowDate(row, this.startDateField)
      const endDate = this.getRowDate(row, this.endDateField)
      if (!startDate || !endDate || startDate.isAfter(endDate)) {
        return event
      }
      const startIndex = this.dateDiff(
        this.firstAvailableDate,
        startDate,
        false
      )
      const startOffset = startIndex * this.columnWidth + 3
      const endIndex = this.dateDiff(this.firstAvailableDate, endDate)
      const endOffset = endIndex * this.columnWidth
      const width = (endIndex - startIndex) * this.columnWidth - 8

      return {
        ...event,
        startDate,
        endDate,
        startIndex,
        startOffset,
        endIndex,
        endOffset,
        width,
        showGotoStartIcon: false,
        showGotoEndIcon: false,
      }
    },
    updateRowsBuffer(sort = true) {
      const { startIndex, endIndex } = this.getVisibleRowsRange()
      const visibleRows = this.rows
        .slice(startIndex, endIndex)
        .map(this.setupRowEvent)
      const getPosition = (row, pos) => ({
        top: (startIndex + pos) * this.rowHeight,
        left: row?.startIndex ? row.startIndex * this.columnWidth : null,
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
        (_, i) => {
          const date = moment(this.firstAvailableDate).add(i, this.unit)
          return {
            id: i,
            date,
            isWeekend: date.isoWeekday() > 5,
          }
        }
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
      this.scrollNow =
        (moment().diff(this.firstAvailableDate, 'hour') / 24) * this.columnWidth
      this.firstVisibleDate = this.firstAvailableDate
        .clone()
        .add(startIndex + 1, this.unit)
      recycleSlots(this.columnsBuffer, visibleColumns, getPosition)
    },
    scrollHorizontal(left, behavior = 'instant') {
      this.scrollAreaElement.scroll({ left, behavior })
      this.$refs.gridHeader.scroll({ left, behavior })
    },
    scrollToStartDate(date) {
      const dateDiff = this.dateDiff(this.firstAvailableDate, date)
      const colIndex = Math.max(0, dateDiff - 2)
      const scrollOffset = colIndex * this.columnWidth
      this.scrollHorizontal(scrollOffset, 'smooth')
    },
    scrollToEndDate(date) {
      const dateDiff = this.dateDiff(this.firstAvailableDate, date)
      const colIndex = Math.min(
        this.columns.length,
        dateDiff - this.visibleColumnCount + 1
      )
      const scrollOffset = colIndex * this.columnWidth
      this.scrollHorizontal(scrollOffset, 'smooth')
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
    async updateValue({ field, row, value, oldValue }) {
      try {
        await this.$store.dispatch(
          this.storePrefix + 'view/timeline/updateRowValue',
          {
            table: this.table,
            view: this.view,
            fields: this.fields,
            row,
            field,
            value,
            oldValue,
          }
        )
      } catch (error) {
        notifyIf(error, 'field')
      }
      // Update also the values needed to propery show the event in the timeline if the
      // row is in the buffer.
      const slot = this.rowsBuffer.find((slot) => slot.item?.id === row.id)
      if (slot) {
        slot.item = this.setupRowEvent(row)
        this.updateSlotEventFlags(slot)
      }
    },
    /**
     * Is called when the user clicks on the card but did not move it to another
     * position.
     */
    rowClick(row) {
      this.$refs.rowEditModal.show(row.id)
      // this.$emit('selected-row', row) // TODO: investigate why is causing some max-recursion error
    },
    /**
     * Calls action in the store to refresh row directly from the backend - f. ex.
     * when editing row from a different table, when editing is complete, we need
     * to refresh the 'main' row that's 'under' the RowEdit modal.
     */
    async refreshRow(row) {
      try {
        await this.$store.dispatch(
          this.storePrefix + 'view/timeline/refreshRowFromBackend',
          { table: this.table, row }
        )
      } catch (error) {
        notifyIf(error, 'row')
      }
    },
    /**
     * Calls the fieldCreated callback and shows the hidden fields section
     * because new fields are hidden by default.
     */
    showFieldCreated({ fetchNeeded, ...context }) {
      this.fieldCreated({ fetchNeeded, ...context })
      this.showHiddenFieldsInRowModal = true
    },
    /**
     * Populates a new row and opens the row edit modal
     * to edit the row.
     */
    populateAndEditRow(row) {
      const rowClone = populateRow(clone(row))
      this.$refs.rowEditModal.show(row.id, rowClone)
    },
  },
}
</script>
