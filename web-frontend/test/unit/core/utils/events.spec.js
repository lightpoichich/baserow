import { isPrintableUnicodeCharacterKeyPress } from '@baserow/modules/core/utils/events'

describe('test key press event helper', () => {
  const aToZLower = [
    'a',
    'b',
    'c',
    'd',
    'e',
    'f',
    'g',
    'h',
    'i',
    'j',
    'k',
    'l',
    'm',
    'n',
    'o',
    'p',
    'q',
    'r',
    's',
    't',
    'u',
    'v',
    'w',
    'x',
    'y',
    'z',
    'µ',
    'ß',
    'à',
    'ã',
    'ø',
    'ğ',
    'ń',
  ]

  const aToZUpper = [
    'A',
    'B',
    'C',
    'D',
    'E',
    'F',
    'G',
    'H',
    'I',
    'J',
    'K',
    'L',
    'M',
    'N',
    'O',
    'P',
    'Q',
    'R',
    'S',
    'T',
    'U',
    'V',
    'W',
    'X',
    'Y',
    'Z',
    'Æ',
    'Ģ',
    'Ň',
    'Ź',
  ]

  const notString = [{}, [], null, undefined]

  const aToZMoreThanOneChar = ['aa', 'Aa', 'bbb', 'BBB']

  const numberStrings = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
  const numbers = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

  const symbolCharacters = [
    '<',
    '>',
    '|',
    '~',
    '$',
    '=',
    '`',
    '´',
    '+',
    '€',
    '^',
    '£',
    '¢',
    '¥',
  ]

  const punctuationCharacters = [
    '{',
    '}',
    '%',
    '"',
    "'",
    '/',
    ';',
    ':',
    '.',
    ',',
    '!',
    '?',
    '@',
    '#',
    '&',
    '§',
    '[',
    ']',
    '\\',
    '-',
    '_',
    '*',
  ]

  const separatorCharacters = [
    ' ',
    ' ',
    ' ',
    ' ',
    ' ',
    ' ',
    ' ',
    ' ',
    ' ',
    ' ',
    ' ',
    ' ',
    ' ',
    ' ',
    ' ',
    ' ',
    '　',
  ]

  const controlCodes = [
    0x0000, 0x0001, 0x0002, 0x0003, 0x0004, 0x0005, 0x0006, 0x0007, 0x0008,
    0x0009, 0x000a, 0x000b, 0x000c, 0x000d, 0x000e, 0x000f, 0x0010, 0x0011,
    0x0012, 0x0013, 0x0014, 0x0015, 0x0016, 0x0017, 0x0018, 0x001a, 0x001b,
    0x001c, 0x001d, 0x001e, 0x001f, 0x007f, 0x0019, 0x0080, 0x0081, 0x0082,
    0x0083, 0x0084, 0x0085, 0x0086, 0x0087, 0x0088, 0x0089, 0x0090, 0x0091,
    0x0092, 0x0093, 0x0094, 0x0095, 0x0096, 0x008a, 0x008b, 0x008c, 0x008d,
    0x008e, 0x008f, 0x0097, 0x0098, 0x0099, 0x009a, 0x009b, 0x009c, 0x009d,
    0x009e, 0x009f,
  ]

  const allCharacters = [
    ...aToZLower,
    ...aToZUpper,
    ...numberStrings,
    ...numbers,
    ...symbolCharacters,
    ...punctuationCharacters,
    ...separatorCharacters,
  ]

  test.each(allCharacters)('non control keys should return true', (value) => {
    const event = {
      key: value,
    }
    expect(isPrintableUnicodeCharacterKeyPress(event)).toBeTruthy()
  })

  test('passing string instead of event should return false', () => {
    const charWithoutEvent = 'a'
    expect(isPrintableUnicodeCharacterKeyPress(charWithoutEvent)).toBeFalsy()
  })

  test('passing null or undefinded should return false', () => {
    expect(isPrintableUnicodeCharacterKeyPress(null)).toBeFalsy()
    expect(isPrintableUnicodeCharacterKeyPress(undefined)).toBeFalsy()
  })

  test.each(notString)('non string objects should return false', (value) => {
    const event = {
      key: value,
    }
    expect(isPrintableUnicodeCharacterKeyPress(event)).toBeFalsy()
  })

  test.each(aToZMoreThanOneChar)(
    'more than one character should return false',
    (value) => {
      const event = {
        key: value,
      }
      expect(isPrintableUnicodeCharacterKeyPress(event)).toBeFalsy()
    }
  )

  test.each(controlCodes)('control keys should return false', (value) => {
    const event = {
      key: String.fromCharCode(value),
    }
    expect(isPrintableUnicodeCharacterKeyPress(event)).toBeFalsy()
  })
})
