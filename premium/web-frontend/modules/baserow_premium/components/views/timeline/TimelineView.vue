<template>
  <div class="timeline-view">
    <div class="calendar-month">
      <div class="calendar-month-wrapper timeline">
        <div class="calendar-month__header">
          <CalendarDateIndicator
            :selected-date="selectedDate(fields)"
            class="calendar-month__header-selected-month"
          />
          <CalendarDateSelector
            :selected-date="selectedDate(fields)"
            :current-date="today"
            @date-selected="selectDate"
          />
        </div>
      </div>
      <div :style="{ height: '100%', width: '100%' }">
        <Timeline :events="events" year="2024" month="6" />
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
import { mapGetters } from 'vuex'
import { notifyIf } from '@baserow/modules/core/utils/error'
import viewHelpers from '@baserow/modules/database/mixins/viewHelpers'
import RowEditModal from '@baserow/modules/database/components/row/RowEditModal.vue'
import { populateRow } from '@baserow/modules/database/store/view/grid'
import { clone } from '@baserow/modules/core/utils/object'
import RowCreateModal from '@baserow/modules/database/components/row/RowCreateModal.vue'
import CalendarDateIndicator from '@baserow_premium/components/views/calendar/CalendarDateIndicator'
import CalendarDateSelector from '@baserow_premium/components/views/calendar/CalendarDateSelector'

import Timeline from './Timeline'

export default {
  name: 'TimelineView',
  components: {
    CalendarDateIndicator,
    CalendarDateSelector,
    Timeline,
    RowEditModal,
    RowCreateModal,
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
      events: [
        { id: 1, label: 'Event 1', start: new Date(2024, 5, 1), end: new Date(2024, 5, 8) },
        { id: 2, label: 'Event 2', start: new Date(2024, 5, 3), end: new Date(2024, 5, 12) },
        { id: 3, label: 'Event 3', start: new Date(2024, 5, 7), end: new Date(2024, 5, 17) },
      ],
      list: [
        {
          id: 'internalId',
          width: 80,
          header: {
            content: '# ID',
          },
        },
        {
          id: 'name',
          width: 200,
          header: {
            content: 'Resurce name',
          },
        },
      ],

      from: +(+new Date()) - 2 * 24 * 60 * 60 * 1000,
      to: moment().startOf('day').add(1, 'months'),

      rows: [
        {
          id: 1,
          internalId: '#1',
          name: 'First',
        },
        {
          id: 2,
          internalId: '#2',
          name: 'Second',
        },
      ],

      items: [
        {
          rowId: 1,
          label: `Some task`,
          style: { background: '#24abf2' },
          time: {
            start: +(+new Date()) - 1.2 * 24 * 60 * 60 * 1000,
            end: +(+new Date()) + 1 * 24 * 60 * 60 * 1000,
          },
        },
        {
          rowId: 2,
          label: `Other task`,
          style: { background: '#abf224' },
          time: {
            start: moment().add(12, 'hours'),
            end: moment().add(2, 'days').add(4, 'hours'),
          },
        },
      ],
    }
  },
  // data() {
  //   return {
  //     showHiddenFieldsInRowModal: false,
  //   }
  // },
  computed: {
    visibleCardFields() {
      return this.fields
        .filter(filterVisibleFieldsFunction(this.fieldOptions))
        .sort(sortFieldsByOrderAndIdFunction(this.fieldOptions))
    },
    hiddenFields() {
      return this.fields
        .filter(filterHiddenFieldsFunction(this.fieldOptions))
        .sort(sortFieldsByOrderAndIdFunction(this.fieldOptions))
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
  },
  mounted() {
    if (this.row !== null) {
      this.populateAndEditRow(this.row)
    }
  },
  beforeCreate() {
    this.$options.computed = {
      ...(this.$options.computed || {}),
      ...mapGetters({
        row: 'rowModalNavigation/getRow',
        allRows:
          this.$options.propsData.storePrefix + 'view/calendar/getAllRows',
        fieldOptions:
          this.$options.propsData.storePrefix +
          'view/calendar/getAllFieldOptions',
        getDateField:
          this.$options.propsData.storePrefix + 'view/calendar/getDateField',
      }),
    }
  },
  methods: {
    selectDate() {},
    selectedDate() {
      return moment().startOf('day')
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


<style scoped>
.timeline-view {
    height: 100%;
  }

  .calendar-month-wrapper.timeline {
    height: revert;
  }
</style>