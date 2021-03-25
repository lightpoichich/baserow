export function createFile(visibleName) {
  return {
    url: 'some_url',
    thumbnails: {},
    visible_name: visibleName,
    name: `actual_name_for_${visibleName}`,
    size: 10,
    mime_type: 'text/plain',
    is_image: false,
    image_width: 0,
    image_height: 0,
    uploaded_at: '2019-08-24T14:15:22Z',
  }
}

export function createMockFields(mock, { applicationId = 1 }) {
  mock.onGet('/database/fields/table/1/').reply(200, [
    {
      id: 1,
      table_id: 1,
      name: 'Name',
      order: 0,
      type: 'text',
      primary: true,
      text_default: '',
    },
    {
      id: 2,
      table_id: 1,
      name: 'Last name',
      order: 1,
      type: 'text',
      primary: false,
      text_default: '',
    },
    {
      id: 3,
      table_id: 1,
      name: 'Notes',
      order: 2,
      type: 'long_text',
      primary: false,
    },
    {
      id: 4,
      table_id: 1,
      name: 'Active',
      order: 3,
      type: 'boolean',
      primary: false,
    },
  ])
}
