<template>
  <h2 class="box__title">
    {{
      selectedApplication === null
        ? selectedGroup.name
        : selectedApplication.name
    }}
  </h2>
</template>

<script>
export default {
  name: 'TrashContents',
  props: {
    selectedGroup: {
      type: Object,
      required: true,
    },
    selectedApplication: {
      type: Object,
      required: false,
      default: null,
    },
  },
  methods: {},
}
</script>
