/**
 * @jest-environment jsdom
 */

import importer from '@baserow/modules/database/mixins/importer'

describe('test file importer', () => {
  test('test field name id is invalid as is reserved by baserow', () => {
    expect(() => importer.methods.validateHeader(['id'])).toThrow(
      'id is a reserved baserow field name and cannot be used.'
    )
  })
  test('test field name order is invalid as is reserved by baserow', () => {
    expect(() => importer.methods.validateHeader(['order'])).toThrow(
      'order is a reserved baserow field name and cannot be used.'
    )
  })
  test('duplicate names are invalid', () => {
    expect(() => importer.methods.validateHeader(['a', 'a'])).toThrow(
      'Field names must be unique.'
    )
  })
  test('blank names are invalid', () => {
    expect(() => importer.methods.validateHeader([''])).toThrow(
      'Blank field names are not allowed.'
    )
  })
  test('a mix of invalid and valid is invalid', () => {
    expect(() => importer.methods.validateHeader(['valid', ''])).toThrow(
      'Blank field names are not allowed.'
    )
    expect(() =>
      importer.methods.validateHeader(['valid', 'id', 'order'])
    ).toThrow('id is a reserved baserow field name and cannot be used.')
    expect(() => importer.methods.validateHeader(['valid', 'a', 'a'])).toThrow(
      'Field names must be unique.'
    )
  })
})
