<template>
<div class="timeline-event">{{ title }}</div>
</template>

<script>
export default {
  name: 'TimelineEvent',
  props: {
    row: {
      type: Object,
      required: true,
    },
    fields: {
      type: Array,
      required: true,
    },
  },
  computed: {
    title() {
      const primaryField = this.fields.find((field) => field.primary)
      return this.row[`field_${primaryField.id}`]
    },
  },
}
</script>

<style scoped>
.timeline-event {
    border-radius: 0px 4px 4px 0px;
    border: 1px solid var(--Static-Divider-Strong, #D7D8D9);
    background: var(--Static-Background-Standard, #FFF);

    box-shadow: 0px 1px 2px 0px rgba(7, 8, 16, 0.10);
}
</style>