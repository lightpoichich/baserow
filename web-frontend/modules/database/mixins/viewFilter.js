export default {
  props: {
    filter: {
      type: Object,
      required: true,
    },
    primary: {
      type: Object,
      required: true,
    },
    fields: {
      type: Array,
      required: true,
    },
    readOnly: {
      type: Boolean,
      required: true,
    },
  },
  computed: {
    field() {
      return this.primary.id === this.filter.field
        ? this.primary
        : this.fields.find((f) => f.id === this.filter.field)
    },
  },
}
