export function createMockApplication(mock, { applicationId = 1 }) {
  mock.onGet('/applications/').reply(200, [
    {
      id: applicationId,
      name: "Nigel's company",
      order: 1,
      type: 'database',
      group: {
        id: 1,
        name: "Nigel's group",
      },
      tables: [
        {
          id: 1,
          name: 'Customers',
          order: 1,
          database_id: 1,
        },
        {
          id: 2,
          name: 'Projects',
          order: 2,
          database_id: 1,
        },
      ],
    },
  ])
}
