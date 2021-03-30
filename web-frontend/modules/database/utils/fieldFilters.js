export function filenameContainsFilter(rowValue, filterValue) {
  filterValue = filterValue.toString().toLowerCase().trim()

  if (filterValue === '') {
    return true
  }

  for (let i = 0; i < rowValue.length; i++) {
    const visibleName = rowValue[i].visible_name.toString().toLowerCase().trim()

    if (visibleName.includes(filterValue)) {
      return true
    }
  }

  return false
}

function _rowValueContainsFilterValue(rowValue, filterValue, field, fieldType) {
  rowValue = fieldType.toHumanReadableString(field, rowValue)
  rowValue = rowValue.toString().toLowerCase().trim()
  filterValue = filterValue.toString().toLowerCase().trim()
  return rowValue.includes(filterValue)
}
export function humanReadableStringContainsFilter(
  rowValue,
  filterValue,
  field,
  fieldType
) {
  return (
    filterValue === '' ||
    _rowValueContainsFilterValue(rowValue, filterValue, field, fieldType)
  )
}

export function humanReadableStringNotContainsFilter(
  rowValue,
  filterValue,
  field,
  fieldType
) {
  return (
    filterValue === '' ||
    !_rowValueContainsFilterValue(rowValue, filterValue, field, fieldType)
  )
}
