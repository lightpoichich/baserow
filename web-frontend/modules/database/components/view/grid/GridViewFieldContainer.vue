<template functional>
  <div
    ref="wrapper"
    class="grid-view__column"
    :style="data.style"
    @click="$options.methods.select($event, parent, props.row, props.field)"
  >
    <component
      :is="$options.methods.getFunctionalComponent(parent, props)"
      v-if="!$options.methods.isSelected(parent, props)"
      :field="props.field"
      :value="props.row['field_' + props.field.id]"
    />
    <component
      :is="$options.methods.getComponent(parent, props)"
      v-if="$options.methods.isSelected(parent, props)"
      :field="props.field"
      :value="props.row['field_' + props.field.id]"
      @update="(...args) => $options.methods.update(listeners, props, ...args)"
      @edit="(...args) => $options.methods.edit(listeners, props, ...args)"
      @unselect="$options.methods.unselect(parent, props)"
      @selected="$options.methods.selected(listeners, props, $event)"
      @unselected="$options.methods.unselected(listeners, props, $event)"
      @selectPrevious="
        $options.methods.forwardEvent(listeners, 'selectPrevious', $event)
      "
      @selectNext="
        $options.methods.forwardEvent(listeners, 'selectNext', $event)
      "
      @selectAbove="
        $options.methods.forwardEvent(listeners, 'selectAbove', $event)
      "
      @selectBelow="
        $options.methods.forwardEvent(listeners, 'selectBelow', $event)
      "
    />
  </div>
</template>

<script>
export default {
  methods: {
    /**
     * If the grid field component emits an update event this method will be called
     * which will actually update the value via the store.
     */
    update(listeners, props, value, oldValue) {
      if (listeners.update) {
        listeners.update({
          row: props.row,
          field: props.field,
          value,
          oldValue,
        })
      }
    },
    /**
     * If the grid field components emits an edit event then the user has changed the
     * value without saving it yet. This is for example used to check in real time if
     * the value still matches the filters.
     */
    edit(listeners, props, value, oldValue) {
      if (listeners.edit) {
        listeners.edit({
          row: props.row,
          field: props.field,
          value,
          oldValue,
        })
      }
    },
    getFunctionalComponent(parent, props) {
      return parent.$registry
        .get('field', props.field.type)
        .getFunctionalGridViewFieldComponent()
    },
    getComponent(parent, props) {
      return parent.$registry
        .get('field', props.field.type)
        .getGridViewFieldComponent()
    },
    isSelected(parent, props) {
      return parent.isGridViewFieldSelected(props.row.id, props.field.id)
    },
    select(event, parent, row, field) {
      event.preventFieldCellUnselect = true
      parent.selectGridViewField(row.id, field.id)
    },
    unselect(parent, props) {
      if (this.isSelected(parent, props)) {
        parent.gridViewFieldSelected.rowId = -1
        parent.gridViewFieldSelected.fieldId = -1
      }
    },
    selected(listeners, props, event) {
      if (listeners.selected) {
        event.row = props.row
        event.field = props.field
        listeners.selected(event)
      }
    },
    unselected(listeners, props, event) {
      if (listeners.unselected) {
        event.row = props.row
        event.field = props.field
        listeners.unselected(event)
      }
    },
    forwardEvent(listeners, name, event) {
      if (listeners[name]) {
        listeners[name](event)
      }
    },
  },
}
</script>
