<template>
  <div class="collection-element__menu">
    <component
      :is="serviceType.collectionElementMenuComponent"
      v-if="dataSource"
      :element="element"
      :data-source="dataSource"
      @refinements-changed="$emit('refinements-changed', $event)"
    />
  </div>
</template>

<script>
export default {
  components: {},
  inject: ['page'],
  props: {
    element: {
      type: Object,
      required: true,
    },
  },
  computed: {
    elementType() {
      return this.$registry.get('element', this.element.type)
    },
    dataSource() {
      return this.$store.getters['dataSource/getPageDataSourceById'](
        this.page,
        this.element.data_source_id
      )
    },
    serviceType() {
      return this.$registry.get('service', this.dataSource?.type)
    },
  },
}
</script>
