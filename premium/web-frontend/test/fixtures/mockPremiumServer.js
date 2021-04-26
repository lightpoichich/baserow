import { createUsersForAdmin } from './user'

export default class MockPremiumServer {
  constructor(mock) {
    this.mock = mock
  }

  createUsers(users, page) {
    createUsersForAdmin(this.mock, users, page)
  }
}
