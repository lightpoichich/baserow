/**
 * Mixin that introduces helper methods for the importer form component.
 */
export default {
  methods: {
    /**
     * Generates an object that can used to render a quick preview of the provided
     * data. Can be used in combination with the TableImporterPreview component.
     */
    getPreview(data, firstRowHeader) {
      let head = data[0]
      let rows = data.slice(1, 4)
      let remaining = data.length - rows.length - 1
      const columns = Math.max(...data.map((entry) => entry.length))

      /**
       * Fills the row with a minimum amount of empty columns.
       */
      const fill = (row, columns) => {
        for (let i = row.length; i < columns; i++) {
          row.push('')
        }
        return row
      }

      // If the first row is not the header, a header containing columns named
      // 'Column N' needs to be generated.
      if (!firstRowHeader) {
        head = []
        for (let i = 1; i <= columns; i++) {
          head.push(`Column ${i}`)
        }
        rows = data.slice(0, 3)
        remaining = data.length - rows.length
      }

      const headSet = new Set()
      for (const column of head) {
        const trimmedColumn = column.trim()
        if (trimmedColumn === '') {
          throw new Error('Blank field names are not allowed.')
        }
        if (['id', 'order'].includes(trimmedColumn)) {
          throw new Error(
            `${column} is a reserved baserow field name and cannot be used.`
          )
        }
        headSet.add(trimmedColumn)
      }
      if (headSet.size !== head.length) {
        throw new Error('Field names must be unique.')
      }

      head = fill(head, columns)
      rows.map((row) => fill(row, columns))

      return { columns, head, rows, remaining }
    },
  },
}
