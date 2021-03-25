import { createMockRowsInGridView } from '@baserow/test/fixtures/grid'
import { createMockGridView } from '@baserow/test/fixtures/view'
import { createMockGroup } from '@baserow/test/fixtures/groups'
import { createMockApplication } from '@baserow/test/fixtures/applications'
import { createMockFields } from '@baserow/test/fixtures/fields'
import { TestApp } from '@baserow/test/helpers/testApp'
import Table from '@baserow/modules/database/pages/table'

let mock
let store

describe('Table Component Tests', () => {
  let testApp = null

  beforeAll(() => {
    testApp = new TestApp()
    mock = testApp.mock
    store = testApp.store
  })

  afterEach(() => {
    testApp.afterEach()
  })

  async function givenASingleSimpleTableInTheServer() {
    createMockApplication(mock, {})
    createMockGridView(mock, {})
    createMockGroup(mock, {})
    createMockFields(mock, {})
    createMockRowsInGridView(mock, {
      rows: [
        {
          id: 1,
          order: 0,
          field_1: 'name',
          field_2: 'last_name',
          field_3: 'notes',
          field_4: false,
        },
      ],
    })
    await store.dispatch('group/fetchAll')
    await store.dispatch('application/fetchAll')
  }

  function expectServerCalledToCreateRow(tableId) {
    mock.onPost(`/database/rows/table/${tableId}/`).reply(200, {
      id: 2,
      order: '2.00000000000000000000',
      field_1: '',
      field_2: '',
      field_3: '',
      field_4: false,
    })
  }

  test('Add a row to a simple table increases the row count', async () => {
    await givenASingleSimpleTableInTheServer()

    const table = await testApp.mount(Table, {
      asyncDataParams: {
        databaseId: '1',
        tableId: '1',
        viewId: '1',
      },
    })

    expect(table.html()).toContain('1 rows')

    expectServerCalledToCreateRow(1)

    const button = table.find('.grid-view__add-row')
    await button.trigger('click')

    expect(table.html()).toContain('2 rows')
    expect(true).toBeTruthy()
  })
})
