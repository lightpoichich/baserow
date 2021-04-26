import { TestApp } from '@baserow/test/helpers/testApp'
import UsersAdminContent from '@baserow_premium/components/admin/user/UsersAdminContent'
import MockPremiumServer from '@baserow_premium/../../test/fixtures/mockPremiumServer'

// Mock out debounce so we dont have to wait or simulate waiting for the various
// debounces in the search functionality.
jest.mock('lodash/debounce', () => jest.fn((fn) => fn))

describe('User Admin Component Tests', () => {
  let testApp = null
  let mockPremiumServer = null

  beforeAll(() => {
    testApp = new TestApp()
    mockPremiumServer = new MockPremiumServer(testApp.mock)
  })

  afterEach(() => testApp.afterEach())

  test('Adding a row to a table increases the row count', async () => {
    mockPremiumServer.createUsers(
      [
        {
          id: 1,
          username: 'user@baserow.io',
          full_name: 'user',
          groups: [
            {
              id: 4,
              name: "users's group",
              permissions: 'ADMIN',
            },
            {
              id: 65,
              name: 'other_group',
            },
          ],
          last_login: '2021-04-26T07:50:45.643059Z',
          date_joined: '2021-04-21T12:04:27.379781Z',
          is_active: true,
          is_staff: true,
        },
      ],
      1
    )

    const userAdmin = await testApp.mount(UsersAdminContent, {})

    expect(userAdmin.html()).toContain('user@baserow.io')
  })
})
