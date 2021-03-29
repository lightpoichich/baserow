import { firstBy } from 'thenby'
import BigNumber from 'bignumber.js'

/**
 * Generates a sort function based on the provided sortings.
 */
export function getRowSortFunction(
  $registry,
  sortings,
  fields,
  primary = null
) {
  let sortFunction = firstBy()

  sortings.forEach((sort) => {
    // Find the field that is related to the sort.
    let field = fields.find((f) => f.id === sort.field)
    if (field === undefined && primary !== null && primary.id === sort.field) {
      field = primary
    }

    if (field !== undefined) {
      const fieldName = `field_${field.id}`
      const fieldType = $registry.get('field', field.type)
      const fieldSortFunction = fieldType.getSort(fieldName, sort.order)
      sortFunction = sortFunction.thenBy(fieldSortFunction)
    }
  })

  sortFunction = sortFunction.thenBy((a, b) =>
    new BigNumber(a.order).minus(new BigNumber(b.order))
  )
  sortFunction = sortFunction.thenBy((a, b) => a.id - b.id)
  return sortFunction
}

/**
 * A helper function that checks if the provided row values match the provided view
 * filters. Returning false indicates that the row should not be visible for that
 * view.
 */
export const matchSearchFilters = ($registry, filterType, filters, values) => {
  // If there aren't any filters then it is not possible to check if the row
  // matches any of the filters, so we can mark it as valid.
  if (filters.length === 0) {
    return true
  }

  for (const i in filters) {
    const filterValue = filters[i].value
    const rowValue = values[`field_${filters[i].field}`]
    const matches = $registry
      .get('viewFilter', filters[i].type)
      .matches(rowValue, filterValue)
    if (filterType === 'AND' && !matches) {
      // With an `AND` filter type, the row must match all the filters, so if
      // one of the filters doesn't match we can mark it as isvalid.
      return false
    } else if (filterType === 'OR' && matches) {
      // With an 'OR' filter type, the row only has to match one of the filters,
      // that is the case here so we can mark it as valid.
      return true
    }
  }

  if (filterType === 'AND') {
    // When this point has been reached with an `AND` filter type it means that
    // the row matches all the filters and therefore we can mark it as valid.
    return true
  } else if (filterType === 'OR') {
    // When this point has been reached with an `OR` filter type it means that
    // the row matches none of the filters and therefore we can mark it as invalid.
    return false
  }
}

function _findFieldsInRowMatchingSearch(
  row,
  activeSearchTerm,
  fields,
  overrides,
  registry
) {
  const fieldTypeToFilter = {
    text: 'contains',
    long_text: 'contains',
    url: 'contains',
    email: 'contains',
    number: 'contains',
    date: 'contains',
    file: 'filename_contains',
    single_select: 'contains',
    phone_number: 'contains',
  }
  const fieldSearchMatches = []
  if (row.id.toString().includes(activeSearchTerm)) {
    fieldSearchMatches.push('row_id')
  }
  for (const field of fields) {
    const fieldName = `field_${field.id}`
    if (fieldTypeToFilter[field.type]) {
      const rowValue =
        fieldName in overrides ? overrides[fieldName] : row[fieldName]
      if (rowValue) {
        const doesMatch = registry
          .get('viewFilter', fieldTypeToFilter[field.type])
          .matches(rowValue, activeSearchTerm)
        if (doesMatch) {
          fieldSearchMatches.push(field.id)
        }
      }
    }
  }
  return fieldSearchMatches
}

/**
 * Helper function which calculates which rows and fields inside the rows match a
 * given search term.
 */
export const calculateRowSearchMatches = (
  fields,
  rows,
  activeSearchTerm,
  hideRowsNotMatchingSearch,
  overrides,
  registry
) => {
  const values = []
  for (const row of rows) {
    const searchIsBlank = activeSearchTerm === ''
    const fieldSearchMatches = searchIsBlank
      ? []
      : _findFieldsInRowMatchingSearch(
          row,
          activeSearchTerm,
          fields,
          overrides,
          registry
        )

    const matchSearch =
      !hideRowsNotMatchingSearch ||
      searchIsBlank ||
      fieldSearchMatches.length > 0

    values.push({ row, matchSearch, fieldSearchMatches })
  }
  return values
}
