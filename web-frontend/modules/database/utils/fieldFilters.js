function _rowValueContainsFilterValue(rowValue, filterValue) {
  if (rowValue === null) {
    rowValue = ''
  } else if (typeof rowValue === 'object' && 'value' in rowValue) {
    rowValue = rowValue.value
  }
  rowValue = rowValue.toString().toLowerCase().trim()
  filterValue = filterValue.toString().toLowerCase().trim()
  return rowValue.includes(filterValue)
}

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

export function genericContainsFilter(rowValue, filterValue) {
  return (
    filterValue === '' || _rowValueContainsFilterValue(rowValue, filterValue)
  )
}

export function genericNotContainsFilter(rowValue, filterValue) {
  return (
    filterValue === '' || !_rowValueContainsFilterValue(rowValue, filterValue)
  )
}
