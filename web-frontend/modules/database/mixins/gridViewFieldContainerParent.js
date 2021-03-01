/**
 * @TODO docs.
 */
export default {
  data() {
    return {
      gridViewFieldSelected: {
        rowId: -1,
        fieldId: -1,
      },
    }
  },
  methods: {
    isGridViewFieldSelected(rowId, fieldId) {
      return (
        this.gridViewFieldSelected.rowId === rowId &&
        this.gridViewFieldSelected.fieldId === fieldId
      )
    },
    selectGridViewField(rowId, fieldId) {
      this.gridViewFieldSelected.rowId = rowId
      this.gridViewFieldSelected.fieldId = fieldId
    },
  },
}
