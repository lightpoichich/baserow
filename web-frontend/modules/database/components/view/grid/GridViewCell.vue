<template functional>
  <div
    ref="wrapper"
    class="grid-view__column"
    :style="data.style"
    @click="$options.methods.select($event, parent, props.field.id)"
  >
    <component
      :is="$options.methods.getFunctionalComponent(parent, props)"
      v-if="
        !parent.isCellSelected(props.field.id) &&
        !parent.alive.includes(props.field.id)
      "
      ref="unselectedField"
      :field="props.field"
      :value="props.row['field_' + props.field.id]"
      :state="props.state"
    />
    <component
      :is="$options.methods.getComponent(parent, props)"
      v-else
      ref="selectedField"
      :field="props.field"
      :value="props.row['field_' + props.field.id]"
      :selected="parent.isCellSelected(props.field.id)"
      @update="(...args) => $options.methods.update(listeners, props, ...args)"
      @edit="(...args) => $options.methods.edit(listeners, props, ...args)"
      @unselect="$options.methods.unselect(parent, props)"
      @selected="$options.methods.selected(listeners, props, $event)"
      @unselected="$options.methods.unselected(listeners, props, $event)"
      @selectPrevious="
        $options.methods.selectNext(listeners, props, 'previous')
      "
      @selectNext="$options.methods.selectNext(listeners, props, 'next')"
      @selectAbove="$options.methods.selectNext(listeners, props, 'above')"
      @selectBelow="$options.methods.selectNext(listeners, props, 'below')"
      @add-keep-alive="parent.addKeepAlive(props.field.id)"
      @remove-keep-alive="parent.removeKeepAlive(props.field.id)"
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
    select(event, parent, fieldId) {
      event.preventFieldCellUnselect = true
      parent.selectCell(fieldId)
    },
    unselect(parent, props) {
      if (parent.isCellSelected(props.field.id)) {
        parent.selectCell(-1, -1)
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
    selectNext(listeners, props, direction) {
      if (listeners['select-next']) {
        listeners['select-next']({
          row: props.row,
          field: props.field,
          direction,
        })
      }
    },
  },
}
</script>
