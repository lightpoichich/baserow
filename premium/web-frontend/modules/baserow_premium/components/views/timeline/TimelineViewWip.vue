<template>
  <div class="timeline-view">
    <InitTimelineViewSettings
      v-if="!view.start_date_field"
      ref="selectDateFieldModal"
      :view="view"
      :fields="fields"
      @refresh="$emit('refresh', $event)"
    >
    </InitTimelineViewSettings>
    <div class="calendar-month">
      <div class="calendar-month-wrapper timeline">
        <div class="calendar-month__header">
          <!-- <CalendarDateIndicator
            :selected-date="selectedDate(fields)"
            class="calendar-month__header-selected-month"
          />
          <CalendarDateSelector
            :selected-date="selectedDate(fields)"
            :current-date="today"
            @date-selected="selectDate"
          /> -->
        </div>
      </div>
      <div :style="{ height: '100%', maxWidth: '100%', display: 'flex' }">
        <!-- <TimelineContainer
          :start-date-field-id="view.start_date_field"
          :end-date-field-id="view.end_date_field"
          :store-prefix="storePrefix"
        />-->
        <div :style="{ display: 'flex', flexDirection: 'column' }">
          <div :style="{ minHeight: px(50) }"></div>
          <VirtualList
            class="list"
            ref="vl"
            :data-key="'id'"
            :data-sources="rows"
            :data-component="itemComponent"
            :item-class="'list-item-fixed'"
            :estimate-size="rowHeightPx"
            @scroll="onScroll"
            :keeps="keepsRows"
          />
        </div>
        <div
          v-scroll="scroll"
          :style="{
            height: '100%',
            width: 'calc(100% - 300px)',
            display: 'flex',
            flexDirection: 'column',
          }"
        >
          <VirtualList
            class="header"
            v-scroll="scroll"
            ref="hhl"
            :data-key="'id'"
            :data-sources="columns"
            :data-component="dayHeaderComponent"
            :estimate-size="colSizePx"
            :item-style="{ width: px(colSizePx) }"
            :wrap-class="'days-wrapper'"
            :wrap-style="{ height: px(50) }"
            :direction="'horizontal'"
            :keeps="100"
          ></VirtualList>
          <div
            :style="{
              height: 'calc(100% - 50px)',
              width: '100%',
              position: 'relative',
              display: 'flex',
              flexDirection: 'column',
            }"
          >
            <VirtualList
              class="days"
              ref="hl"
              :data-key="'id'"
              :data-sources="columns"
              :data-component="dayComponent"
              :wrap-class="'days-wrapper'"
              :wrap-style="{ height: px(rowHeightPx * rowsCount) }"
              :estimate-size="colSizePx"
              :item-style="{ width: px(colSizePx) }"
              :direction="'horizontal'"
              @scroll="onScrollH"
              :keeps="100"
            >
            </VirtualList>
            <div
              ref="hle"
              :style="{
                position: 'absolute',
                top: '0',
                left: '0',
                width: '100%',
                height: '100%',
                overflow: 'hidden',
              }"
            >
              <div
                :style="{
                  position: 'relative',
                  width: px(colSizePx * columns.length),
                  height: px(rowsCount * rowHeightPx),
                }"
              >
                <div
                  :style="{
                    position: 'absolute',
                    top: '0',
                    left: px(colSizePx),
                    width: px(colSizePx * 2),
                    height: px(rowHeightPx),
                    background: 'rgba(0, 0, 0, 0.1)',
                  }"
                ></div>
              </div>
            </div>
            <Scrollbars
              ref="scrollbars"
              :vertical="getVerticalScrollbarElement"
              :horizontal="getHorizontalScrollbarElement"
              @vertical="verticalScroll"
              @horizontal="horizontalScroll"
            />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
<script>
import moment from '@baserow/modules/core/moment'
import {
  filterHiddenFieldsFunction,
  filterVisibleFieldsFunction,
  sortFieldsByOrderAndIdFunction,
} from '@baserow/modules/database/utils/view'
import { notifyIf } from '@baserow/modules/core/utils/error'
import viewHelpers from '@baserow/modules/database/mixins/viewHelpers'
import RowEditModal from '@baserow/modules/database/components/row/RowEditModal.vue'
import { populateRow } from '@baserow/modules/database/store/view/grid'
import { clone } from '@baserow/modules/core/utils/object'
import RowCreateModal from '@baserow/modules/database/components/row/RowCreateModal.vue'
import CalendarDateIndicator from '@baserow_premium/components/views/calendar/CalendarDateIndicator'
import CalendarDateSelector from '@baserow_premium/components/views/calendar/CalendarDateSelector'
import InitTimelineViewSettings from '@baserow_premium/components/views/timeline/InitTimelineViewSettings'
import { v4 as uuidv4 } from 'uuid'

import TimelineContainer from './TimelineContainer'
import Item from './Item'
import Day from './Day'
import DayHeader from './DayHeader'
import temp from 'temp'

export default {
  name: 'TimelineView',
  components: {
    CalendarDateIndicator,
    CalendarDateSelector,
    TimelineContainer,
    RowEditModal,
    RowCreateModal,
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
  data() {
    return {
      nCols: 31,
      unit: 'day',
      minColSizePx: 32,
      rowHeightPx: 40,
      firstVisibleIndex: 0,
      lastVisibleIndex: 0,
      columns: [],
      elemWidth: 0,
      elemHeight: 0,
      colSizePx: 32,
      // TODO: fix below
      i: 100,
      itemComponent: Item,
      dayComponent: Day,
      dayHeaderComponent: DayHeader,

    }
  },
  computed: {
    // visibleCardFields() {
    //   return this.fields
    //     .filter(filterVisibleFieldsFunction(this.fieldOptions))
    //     .sort(sortFieldsByOrderAndIdFunction(this.fieldOptions))
    // },
    // hiddenFields() {
    //   return this.fields
    //     .filter(filterHiddenFieldsFunction(this.fieldOptions))
    //     .sort(sortFieldsByOrderAndIdFunction(this.fieldOptions))
    // },
    rows() {
      return this.$store.getters[this.storePrefix + 'view/timeline/getRows'].map(
        (row) => {
          return row !== null ? row : { id: uuidv4(), loading: true }
        }
      )
    },
    rowsCount() {
      return this.rows.length
    },
    keepsRows() {
      return Math.min(this.rowsCount, 50)
    },
  },
  watch: {
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
    rows: {
      handler() {
        this.$refs.vl.reset()
      },
    },
  },
  beforeDestroy() {
    window.removeEventListener('resize', this.updateElemDimensions)
  },
  mounted() {
    const firstAvailableDate = moment().subtract(1, 'year').startOf('year')
    const lastAvailableDate = moment().add(2, 'year').startOf('year')
    const firstVisibleDate = moment().startOf('month')
    const lastVisibleDate = moment().add(1, 'month').startOf('month')
    this.setupColumns(
      firstAvailableDate,
      firstVisibleDate,
      lastVisibleDate,
      lastAvailableDate
    )
    this.updateElemDimensions()

    this.$nextTick(() => {
      this.$refs.hl.reset()
      this.$refs.hhl.reset()
      this.$nextTick(() => {
        this.$refs.scrollbars.update()
        this.horizontalScroll(this.firstVisibleIndex * this.colSizePx)
      })
      window.addEventListener('resize', this.updateElemDimensions)
    })
  },
  methods: {
    uuid() {
      return uuidv4()
    },
    px(n) {
      return `${n}px`
    },
    updateElemDimensions() {
      this.elemWidth = this.$refs.hle.clientWidth
      this.elemHeight = Math.max(
        this.$refs.hle.clientHeight,
        this.$refs.hle.scrollHeight
      )
      this.colSizePx = Math.max(this.elemWidth / this.nCols, this.minColSizePx)
    },
    setupColumns(
      firstAvailableDate,
      firstVisibleDate,
      lastVisibleDate,
      lastAvailableDate
    ) {
      this.columns = Array.from(
        { length: lastAvailableDate.diff(firstAvailableDate, this.unit) },
        (_, i) => ({
          id: i,
          value: moment(firstAvailableDate).add(i, this.unit),
        })
      )
      this.firstVisibleIndex = firstVisibleDate.diff(
        firstAvailableDate,
        this.unit
      )
      this.lastVisibleIndex = lastVisibleDate.diff(
        firstAvailableDate,
        this.unit
      )
    },
    onScroll(event, range) {
      this.$refs.hl.$el.scroll({ top: event.target.scrollTop })
      this.$store.dispatch(
          this.storePrefix + 'view/timeline/fetchMissingRowsInNewRange',
          {
            startIndex: range.start,
            endIndex: range.end,
          }
        )
    },
    onScrollH(event, range) {
      this.$refs.scrollbars.update()
    },
    scroll(pixelY, pixelX) {
      const $rightBody = this.$refs.hl.$el
      const $right = this.$refs.hl.$el

      const top = $rightBody.scrollTop + pixelY
      const left = $right.scrollLeft + pixelX

      this.verticalScroll(top)
      this.horizontalScroll(left)

      this.$refs.scrollbars.update()
    },
    verticalScroll(top) {
      this.$refs.hl.$el.scroll({ top })
      this.$refs.vl.$el.scroll({ top })
      this.$refs.hle.scroll({ top })
    },
    horizontalScroll(left) {
      this.$refs.hl.$el.scroll({ left })
      this.$refs.hhl.$el.scroll({ left })
      this.$refs.hle.scroll({ left })
    },
    getHorizontalScrollbarElement() {
      return this.$refs.hl.$el
    },
    getVerticalScrollbarElement() {
      return this.$refs.hl.$el
    },
    scrollForward() {
      this.i += 10
      this.$refs.vl.scrollToIndex(this.i)
    },
    async updateValue({ field, row, value, oldValue }) {
      try {
        await this.$store.dispatch(
          this.storePrefix + 'view/calendar/updateRowValue',
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
    },
    /**
     * When the row edit modal is opened we notifiy
     * the Table component that a new row has been selected,
     * such that we can update the path to include the row id.
     */
    openRowEditModal(row) {
      this.$refs.rowEditModal.show(row.id)
      this.$emit('selected-row', row)
    },
    /**
     * Populates a new row and opens the row edit modal
     * to edit the row.
     */
    populateAndEditRow(row) {
      const rowClone = populateRow(clone(row))
      this.$store.dispatch(this.storePrefix + 'view/calendar/selectRow', {
        row: rowClone,
        fields: this.fields,
      })

      this.$refs.rowEditModal.show(row.id, rowClone)
    },
    async createRow({ row, callback }) {
      try {
        await this.$store.dispatch(
          this.storePrefix + 'view/calendar/createNewRow',
          {
            view: this.view,
            table: this.table,
            fields: this.fields,
            values: row,
          }
        )
        callback()
      } catch (error) {
        callback(error)
      }
    },

    openCreateRowModal(event) {
      const defaults = {}
      const dateField = this.getDateField(this.fields)
      if (!dateField) {
        // Cannot create a row without a proper date field
        return
      }
      const fieldType = this.$registry.get('field', dateField.type)
      if (event?.day?.date != null && dateField && !fieldType.getIsReadOnly()) {
        const name = `field_${dateField.id}`
        if (dateField.date_include_time) {
          defaults[name] = event.day.date.toISOString()
        } else {
          defaults[name] = event.day.date.format('YYYY-MM-DD')
        }
      }
      this.$refs.rowCreateModal.show(defaults)
    },
  },
}
</script>

<style>
.days-wrapper {
  display: flex;
  flex-direction: row;
  height: 100%;
}
</style>

<style scoped>
.list {
  width: 300px;
  height: 100%;
  border: 2px solid;
  border-radius: 3px;
  overflow-y: hidden;
  border-color: dimgray;
}

.days,
.header {
  width: 100%;
  height: 100%;
  overflow: hidden;
  border-color: dimgray;
  display: flex;
}

.header {
  min-height: 50px;
}

.list-item-fixed {
  display: flex;
  align-items: center;
  padding: 0 1em;
  height: 60px;
  border-bottom: 1px solid;
  border-color: lightgray;
}

.myevent {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: lightblue;
}

.timeline-view {
  height: 100%;
}

.calendar-month-wrapper.timeline {
  height: revert;
}
</style>
