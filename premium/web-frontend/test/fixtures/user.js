export function createUsersForAdmin(mock, users, page) {
  mock.onGet(`/premium/admin/user/`, { params: { page } }).reply(200, {
    count: users.length,
    results: users,
  })
}
