import { createApplication } from '@baserow/test/fixtures/applications'
import { createGroup } from '@baserow/test/fixtures/groups'
import { createGridView } from '@baserow/test/fixtures/view'
import { createFields } from '@baserow/test/fixtures/fields'
import { createRows } from '@baserow/test/fixtures/grid'

export class MockServer {
  constructor(mock, store) {
    this.mock = mock
    this.store = store
  }

  async createAppAndGroup(table) {
    const group = createGroup(this.mock, {})
    const application = createApplication(this.mock, {
      groupId: group.id,
      tables: [table],
    })
    await this.store.dispatch('group/fetchAll')
    await this.store.dispatch('application/fetchAll')
    return { application, group }
  }

  createTable() {
    return { id: 1, name: 'Test Table 1' }
  }

  createGridView(application, table, filters = []) {
    return createGridView(this.mock, application, table, {
      filters,
    })
  }

  createFields(application, table, fields) {
    return createFields(this.mock, application, table, fields)
  }

  createRows(gridView, fields, rows) {
    return createRows(this.mock, gridView, fields, rows)
  }
}
