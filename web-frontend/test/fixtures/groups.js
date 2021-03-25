export function createMockGroup(mock, { groupId = 1 }) {
  mock.onGet('/groups/').reply(200, [
    {
      order: 1,
      permissions: 'ADMIN',
      id: groupId,
      name: `group_${groupId}`,
    },
  ])
}
