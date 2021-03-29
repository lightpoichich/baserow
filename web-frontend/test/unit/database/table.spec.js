import { TestApp } from '@baserow/test/helpers/testApp'
import Table from '@baserow/modules/database/pages/table'
import flushPromises from 'flush-promises'

describe('Table Component Tests', () => {
  let testApp = null
  let mock = null
  let mockServer = null

  beforeAll(() => {
    testApp = new TestApp()
    mock = testApp.mock
    mockServer = testApp.mockServer
  })

  afterEach(() => {
    testApp.afterEach()
  })

  async function givenASingleSimpleTableInTheServer() {
    const table = mockServer.createTable()
    const { application } = await mockServer.createAppAndGroup(table)
    const gridView = mockServer.createGridView(application, table)
    const fields = mockServer.createFields(application, table, [
      {
        name: 'Name',
        type: 'text',
        primary: true,
      },
      {
        name: 'Last name',
        type: 'text',
      },
      {
        name: 'Notes',
        type: 'long_text',
      },
      {
        name: 'Active',
        type: 'boolean',
      },
    ])

    mockServer.createRows(gridView, fields, [
      {
        id: 1,
        order: 0,
        field_1: 'name',
        field_2: 'last_name',
        field_3: 'notes',
        field_4: false,
      },
    ])
    return { application, table, gridView }
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
    const {
      application,
      table,
      gridView,
    } = await givenASingleSimpleTableInTheServer()

    const tableComponent = await testApp.mount(Table, {
      asyncDataParams: {
        databaseId: application.id,
        tableId: table.id,
        viewId: gridView.id,
      },
    })

    expect(tableComponent.html()).toContain('1 rows')

    expectServerCalledToCreateRow(table.id)

    const button = tableComponent.find('.grid-view__add-row')
    await button.trigger('click')

    expect(tableComponent.html()).toContain('2 rows')
    expect(true).toBeTruthy()
  })

  test('Searching for a cells value highlights it', async () => {
    const {
      application,
      table,
      gridView,
    } = await givenASingleSimpleTableInTheServer()

    const tableComponent = await testApp.mount(Table, {
      asyncDataParams: {
        databaseId: application.id,
        tableId: table.id,
        viewId: gridView.id,
      },
    })

    mock
      .onGet(`/database/views/grid/1/`, {
        params: { limit: 120, offset: 0, search: 'last_name' },
      })
      .reply(200, {
        count: 1,
        next: null,
        previous: null,
        results: [
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

    const searchBox = tableComponent.get(
      'input[placeholder*="Search in all rows"]'
    )
    await searchBox.setValue('last_name')
    await searchBox.trigger('submit')
    await flushPromises()
    expect(
      tableComponent
        .findAll('.grid-view__cell--searched')
        .filter((w) => w.html().includes('last_name')).length
    ).toBe(1)
  })
})
