/**
 * @jest-environment jsdom
 */

import importer from '@baserow/modules/database/mixins/importer'

describe('test file importer', () => {
  test('test field name id is invalid as is reserved by baserow', () => {
    expect(() => importer.methods.makeHeaderUniqueAndValid(['id'])).toThrow(
      'id is a reserved baserow field name and cannot be used.'
    )
  })
  test('test field name order is invalid as is reserved by baserow', () => {
    expect(() => importer.methods.makeHeaderUniqueAndValid(['order'])).toThrow(
      'order is a reserved baserow field name and cannot be used.'
    )
  })
  test('duplicate names are invalid', () => {
    expect(() => importer.methods.makeHeaderUniqueAndValid(['a', 'a'])).toThrow(
      'Field names must be unique.'
    )
  })
  test('blank names are invalid', () => {
    expect(() => importer.methods.makeHeaderUniqueAndValid([''])).toThrow(
      'Blank field names are not allowed.'
    )
  })
  test('a mix of invalid and valid is invalid', () => {
    expect(() =>
      importer.methods.makeHeaderUniqueAndValid(['valid', ''])
    ).toThrow('Blank field names are not allowed.')
    expect(() =>
      importer.methods.makeHeaderUniqueAndValid(['valid', 'id', 'order'])
    ).toThrow('id is a reserved baserow field name and cannot be used.')
    expect(() =>
      importer.methods.makeHeaderUniqueAndValid(['valid', 'a', 'a'])
    ).toThrow('Field names must be unique.')
  })
})
