<template>
  <div
    class="grid-view__row"
    :class="{
      'grid-view__row--selected': row._.selectedBy.length > 0,
      'grid-view__row--loading': row._.loading,
      'grid-view__row--hover': row._.hover,
      'grid-view__row--warning': !row._.matchFilters || !row._.matchSortings,
    }"
    @mouseover="$emit('row-hover', { row, value: true })"
    @mouseleave="$emit('row-hover', { row, value: false })"
    @contextmenu.prevent="$emit('row-context', { row, event: $event })"
  >
    <template v-if="includeRowDetails">
      <div
        v-if="!row._.matchFilters || !row._.matchSortings"
        class="grid-view__row-warning"
      >
        <template v-if="!row._.matchFilters">
          Row does not match filters
        </template>
        <template v-else-if="!row._.matchSortings">Row has moved</template>
      </div>
      <div class="grid-view__column" :style="{ width: 60 + 'px' }">
        <div class="grid-view__row-info">
          <div class="grid-view__row-count" :title="row.id">
            {{ row.id }}
          </div>
          <a class="grid-view__row-more" @click="$emit('edit-modal', row)">
            <i class="fas fa-expand"></i>
          </a>
        </div>
      </div>
    </template>
    <!--
    Somehow re-declaring all the events instead of using v-on="$listeners" speeds
    everything because the rows don't need to be updated everytime a new one is added.
    -->
    <GridViewCell
      v-for="field in fields"
      :key="'row-field-' + row.id + '-' + field.id"
      :field="field"
      :row="row"
      :state="state"
      :style="{ width: fieldWidths[field.id] + 'px' }"
      @update="$emit('update', $event)"
      @edit="$emit('edit', $event)"
      @select="$emit('select', $event)"
      @unselect="$emit('unselect', $event)"
      @selected="$emit('selected', $event)"
      @unselected="$emit('unselected', $event)"
      @select-next="$emit('select-next', $event)"
    ></GridViewCell>
  </div>
</template>

<script>
import GridViewCell from '@baserow/modules/database/components/view/grid/GridViewCell'
import gridViewHelpers from '@baserow/modules/database/mixins/gridViewHelpers'

export default {
  name: 'GridViewRow',
  components: { GridViewCell },
  mixins: [gridViewHelpers],
  props: {
    row: {
      type: Object,
      required: true,
    },
    fields: {
      type: Array,
      required: true,
    },
    fieldWidths: {
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
      state: {},
      alive: [],
    }
  },
  methods: {
    isCellSelected(fieldId) {
      return this.row._.selected && this.row._.selectedFieldId === fieldId
    },
    selectCell(fieldId, rowId = this.row.id) {
      this.$store.dispatch('view/grid/setSelectedCell', {
        rowId,
        fieldId,
      })
    },
    setState(value) {
      this.state = value
    },
    addKeepAlive(fieldId) {
      if (!this.alive.includes(fieldId)) {
        this.alive.push(fieldId)
      }
    },
    removeKeepAlive(fieldId) {
      const index = this.alive.findIndex((id) => id === fieldId)
      if (index > -1) {
        this.alive.splice(index, 1)
      }
    },
  },
}
</script>
