<template>
  <div>{{ row[column.key] }}</div>
</template>

<script>
export default {
  name: 'SimpleCell',
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
