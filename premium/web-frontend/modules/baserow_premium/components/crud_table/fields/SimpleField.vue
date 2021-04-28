<template functional>
  <div
    v-tooltip="props.row[props.column.key]"
    :class="[data.staticClass, data.class]"
  >
    {{ props.row[props.column.key] }}
  </div>
</template>

<script>
export default {
  name: 'SimpleField',
  functional: true,
  props: {
    row: {
      required: true,
      type: Object,
    },
    column: {
      required: true,
      type: Object,
    },
  },
}
</script>
