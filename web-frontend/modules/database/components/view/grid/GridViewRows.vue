<template>
  <div
    class="grid-view__rows"
    :style="{ transform: `translateY(${rowsTop}px)` }"
  >
    <!--
    <GridViewRow
      v-for="row in rows"
      :key="'row-' + '-' + row.id"
      :row="row"
      :fields="fields"
      :field-widths="fieldWidths"
      :include-row-details="includeRowDetails"
      @update="$emit('update', $event)"
      @edit="$emit('edit', $event)"
      @select="$emit('select', $event)"
      @unselect="$emit('unselect', $event)"
      @selected="$emit('selected', $event)"
      @unselected="$emit('unselected', $event)"
      @select-next="$emit('selectNext', $event)"
      @row-hover="$emit('row-hover', $event)"
      @row-context="$emit('row-context', $event)"
      @edit-modal="$emit('edit-modal', $event)"
    ></GridViewRow>
    -->
    <!--
    <GridViewRow
      v-for="row in rows"
      :key="'row-' + '-' + row.id"
      :row="row"
      :fields="fields"
      :field-widths="fieldWidths"
      :include-row-details="includeRowDetails"
      v-on="$listeners"
    ></GridViewRow>
    -->
    <GridViewRow
      v-for="slot in buffer"
      :key="'row-' + '-' + slot.id"
      :row="slot.row"
      :fields="fields"
      :field-widths="fieldWidths"
      :include-row-details="includeRowDetails"
      :style="{ top: slot.position * 33 + 'px' }"
      v-show="slot.position != -1"
      v-on="$listeners"
    ></GridViewRow>
  </div>
</template>

<script>
import _ from 'lodash'
import { mapGetters } from 'vuex'

import GridViewRow from '@baserow/modules/database/components/view/grid/GridViewRow'
import { populateRow } from '@baserow/modules/database/store/view/grid'
import gridViewHelpers from '@baserow/modules/database/mixins/gridViewHelpers'

export default {
  name: 'GridViewRows',
  components: { GridViewRow },
  mixins: [gridViewHelpers],
  props: {
    fields: {
      type: Array,
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
    includeRowDetails: {
      type: Boolean,
      required: false,
      default: () => false,
    },
  },
  data() {
    return {
      buffer: [],
      fieldWidths: {},
    }
  },
  computed: {
    ...mapGetters({
      rows: 'view/grid/getRows',
      rowsTop: 'view/grid/getRowsTop',
      rowPadding: 'view/grid/getRowPadding',
    }),
  },
  watch: {
    fieldOptions: {
      deep: true,
      handler() {
        this.updateFieldWidths()
      },
    },
    fields() {
      this.updateFieldWidths()
      this.updateBuffer()
    },
    rows() {
      this.updateBuffer()
    },
  },
  created() {
    this.updateFieldWidths()
    this.updateBuffer()
  },
  methods: {
    updateFieldWidths() {
      this.fields.forEach((field) => {
        this.fieldWidths[field.id] = this.getFieldWidth(field.id)
      })
    },
    selectCell(rowId, fieldId) {
      this.$store.dispatch('view/grid/setSelectedCell', { rowId, fieldId })
    },
    updateBuffer() {
      let min = this.rowPadding * 2 + 1

      // If is appears that the minimum reserved it not for the amount of rows, we
      // need to temporary increase the buffer size.
      if (this.rows.length > min) {
        min = this.rows.length
      }

      // First fill up the buffer with the minimum amount of slots.
      for (let i = this.buffer.length; i < min; i++) {
        this.buffer.push({
          id: i,
          row: populateRow({ id: -1 }),
          position: -1,
        })
      }

      // Remove not needed slots.
      this.buffer = this.buffer.slice(0, min)

      // Check which rows are should not be displayed anymore and clear that slow
      // in the buffer.
      this.buffer.forEach((slot) => {
        const exists = this.rows.findIndex((row) => row.id === slot.row.id) >= 0
        if (!exists) {
          slot.row = populateRow({ id: -1 })
          slot.position = -1
        }
      })

      // Then check which rows should have which position.
      this.rows.forEach((row, position) => {
        // Check if the row is already in the buffer
        const index = this.buffer.findIndex((slot) => slot.row.id === row.id)

        if (index >= 0) {
          // If the row already exists in the buffer, then only update the position.
          _.assign(this.buffer[index].row, row)
          this.buffer[index].position = position
        } else {
          // If the row does not yet exists in the buffer, then we can find the first
          // empty slot and place it there.
          const emptyIndex = this.buffer.findIndex((slot) => slot.row.id === -1)
          this.buffer[emptyIndex].row = row
          this.buffer[emptyIndex].position = position
        }
      })
    },
  },
}
</script>
