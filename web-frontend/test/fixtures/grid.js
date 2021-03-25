export function createMockRowsInGridView(
  mock,
  { gridId = 1, rows = 1, numFields = 4 }
) {
  const fieldOptions = {}
  for (let i = 1; i < numFields; i++) {
    fieldOptions[i] = {
      width: 200,
      hidden: false,
      order: i,
    }
  }
  mock.onGet(`/database/views/grid/${gridId}/`).reply(200, {
    count: rows.length,
    results: rows,
    field_options: fieldOptions,
  })
}
