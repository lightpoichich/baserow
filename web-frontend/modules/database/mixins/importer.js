/**
 * Mixin that introduces helper methods for the importer form component.
 */
import { RESERVED_BASEROW_FIELD_NAMES } from '@baserow/modules/database/utils/constants'

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
      } else {
        head = fill(head, columns)
        head = this.makeHeaderUniqueAndValid(head)
      }

      rows.map((row) => fill(row, columns))

      return { columns, head, rows, remaining }
    },
    findNextFreeName(originalColumnName, nextFreeIndexMap, startingIndex) {
      let i = nextFreeIndexMap.get(originalColumnName) || startingIndex
      while (true) {
        const nextColumnNameToCheck = `${originalColumnName} ${i}`
        if (!nextFreeIndexMap.has(nextColumnNameToCheck)) {
          nextFreeIndexMap.set(originalColumnName, i + 1)
          return nextColumnNameToCheck
        }
        i++
      }
    },
    makeColumnNameUniqueAndValidIfNotAlready(column, nextFreeIndexMap) {
      if (column === '') {
        return this.findNextFreeName('Field', nextFreeIndexMap, 1)
      } else if (RESERVED_BASEROW_FIELD_NAMES.includes(column)) {
        return this.findNextFreeName(column, nextFreeIndexMap, 2)
      } else if (nextFreeIndexMap.get(column) > 0) {
        return this.findNextFreeName(column, nextFreeIndexMap, 2)
      } else {
        nextFreeIndexMap.set(column, 2)
        return column
      }
    },
    /**
     * Ensures that the uploaded field names are unique, non blank and don't use any
     * reserved Baserow field names.
     * @param {*[]} head An array of field names to be checked.
     * @return A new array of field names which are guaranteed to be unique and valid.
     */
    makeHeaderUniqueAndValid(head) {
      const nextFreeIndexMap = new Map()
      for (let i = 0; i < head.length; i++) {
        nextFreeIndexMap.set(head[i], 0)
      }
      const uniqueAndValidHeader = []
      for (let i = 0; i < head.length; i++) {
        const column = head[i]
        const trimmedColumn = column.trim()
        const uniqueValidName = this.makeColumnNameUniqueAndValidIfNotAlready(
          trimmedColumn,
          nextFreeIndexMap
        )
        uniqueAndValidHeader.push(uniqueValidName)
      }
      return uniqueAndValidHeader
    },
  },
}
