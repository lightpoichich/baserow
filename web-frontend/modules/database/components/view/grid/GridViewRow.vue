<template>
  <div
    class="grid-view__row"
    :class="{
      'grid-view__row--selected': row._.selectedBy.length > 0,
      'grid-view__row--loading': row._.loading,
      'grid-view__row--hover': row._.hover,
      'grid-view__row--warning': !row._.matchFilters || !row._.matchSortings,
    }"
    @mouseover="$parent.setRowHover(row, true)"
    @mouseleave="$parent.setRowHover(row, false)"
    @contextmenu.prevent="$parent.showRowContext($event, row)"
  >
    <GridViewFieldContainer
      v-for="field in visibleFields"
      :key="'grid-view-row-field-' + row.id + '-' + field.id"
      :field="field"
      :row="row"
      :style="{ width: widths.fields[field.id] + 'px' }"
      @selected="$parent.selectedField(field, $event)"
      @unselected="$parent.unselectedField(field, $event)"
      @selectPrevious="
        $parent.selectNextField(row, field, fields, primary, 'previous')
      "
      @selectNext="$parent.selectNextField(row, field, fields, primary)"
      @selectAbove="
        $parent.selectNextField(row, field, fields, primary, 'above')
      "
      @selectBelow="
        $parent.selectNextField(row, field, fields, primary, 'below')
      "
      @update="$parent.updateValue"
      @edit="$parent.editValue"
    ></GridViewFieldContainer>
  </div>
</template>

<script>
import GridViewFieldContainer from '@baserow/modules/database/components/view/grid/GridViewFieldContainer'

export default {
  name: 'GridViewRow',
  components: { GridViewFieldContainer },
  props: {
    row: {
      type: Object,
      required: true,
    },
    visibleFields: {
      type: Array,
      required: true,
    },
    fields: {
      type: Array,
      required: true,
    },
    primary: {
      type: Object,
      required: true,
    },
    widths: {
      type: Object,
      required: true,
    },
  },
  methods: {
    isGridViewFieldSelected(...args) {
      return this.$parent.isGridViewFieldSelected(...args)
    },
  },
}
</script>
