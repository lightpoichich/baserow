<template>
  <div>
    <div v-if="row[column.key]">
      <i class="fas fa-fw fa-check user-admin-rows__active-icon"></i>
      Active
    </div>
    <div v-else>
      <i class="fas fa-fw fa-times user-admin-rows__deactive-icon"></i>
      Deactivated
    </div>
  </div>
</template>

<script>
export default {
  name: 'ActiveField',
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
