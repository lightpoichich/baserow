export function aUser({
  id = 1,
  username = 'user@baserow.io',
  fullName = 'user_name',
  groups = [
    {
      id: 1,
      name: 'some_group',
      permissions: 'ADMIN',
    },
  ],
  lastLogin = '2021-04-26T07:50:45.643059Z',
  dateJoined = '2021-04-21T12:04:27.379781Z',
  isActive = true,
  isStaff = true,
}) {
  return {
    id,
    username,
    full_name: fullName,
    groups,
    last_login: lastLogin,
    date_joined: dateJoined,
    is_active: isActive,
    is_staff: isStaff,
  }
}

export function createUsersForAdmin(
  mock,
  users,
  page,
  { count = null, search = null }
) {
  const params = { page }
  if (search !== null) {
    params.search = search
  }
  mock.onGet(`/premium/admin/user/`, { params }).reply(200, {
    count: count === null ? users.length : count,
    results: users,
  })
}

export function expectUserDeleted(mock, userId) {
  mock.onDelete(`/premium/admin/user/${userId}/`).reply(200)
}

export function expectUserUpdated(mock, user, changes) {
  changes.id = user.id
  mock
    .onPatch(`/premium/admin/user/${user.id}/`, changes)
    .reply(200, Object.assign({}, user, changes))
}

export function expectUserUpdatedRespondsWithError(mock, user, error) {
  mock.onPatch(`/premium/admin/user/${user.id}/`).reply(500, error)
}
