import {
  isUnicodeLetterCharacter,
  isUnicodeNumberCharacter,
  isUnicodePunctuationCharacter,
  isUnicodeSymbolCharacter,
} from '@baserow/modules/core/utils/events'

describe('test key press event helpers', () => {
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
  ]

  const notString = [{}, 5, []]

  const aToZMoreThanOneChar = ['aa', 'Aa', 'bbb', 'BBB']

  const testNumberCases = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
  const testNumberCasesNumber = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

  const specialCharacterCases = [
    '<',
    '>',
    '{',
    '}',
    '"',
    '/',
    '|',
    ';',
    ':',
    '.',
    ',',
    '~',
    '!',
    '?',
    '@',
    '#',
    '$',
    '%',
    '=',
    '&',
    '*',
    '§',
    '[',
    ']',
    '\\',
    '`',
    '´',
    '+',
    "'",
    '-',
    '_',
    '€',
    '^',
  ]

  // Tests for isAlphabeticCharacter function

  test.each(aToZLower)(
    'test letter character lower should be true',
    (value) => {
      expect(isUnicodeLetterCharacter(value)).toBeTruthy()
    }
  )

  test.each(aToZUpper)(
    'test letter character upper should be true',
    (value) => {
      expect(isUnicodeLetterCharacter(value)).toBeTruthy()
    }
  )

  test.each(notString)(
    'test letter character wrong type should be false',
    (value) => {
      expect(isUnicodeLetterCharacter(value)).toBeFalsy()
    }
  )

  test.each(testNumberCases)(
    'test letter character numbers should be false',
    (value) => {
      expect(isUnicodeLetterCharacter(value)).toBeFalsy()
    }
  )

  test.each(specialCharacterCases)(
    'test letter character special characters should be false',
    (value) => {
      expect(isUnicodeLetterCharacter(value)).toBeFalsy()
    }
  )

  test.each(aToZMoreThanOneChar)(
    'test letter character with more than one characters should be false',
    (value) => {
      expect(isUnicodeLetterCharacter(value)).toBeFalsy()
    }
  )

  // Tests for isNumberCharacter function

  test.each(testNumberCases)(
    'test number character should be true',
    (value) => {
      expect(isUnicodeNumberCharacter(value)).toBeTruthy()
    }
  )

  test.each(testNumberCasesNumber)(
    'test number character with number type should be true',
    (value) => {
      expect(isUnicodeNumberCharacter(value)).toBeTruthy()
    }
  )

  test.each(aToZLower)(
    'test number character with alphabetic lower character strings should be false',
    (value) => {
      expect(isUnicodeNumberCharacter(value)).toBeFalsy()
    }
  )

  test.each(aToZUpper)(
    'test number character with alphabetic upper character strings should be false',
    (value) => {
      expect(isUnicodeNumberCharacter(value)).toBeFalsy()
    }
  )

  // Tests for isSpecialCharacter function

  test.each(specialCharacterCases)(
    'test special characters should be true',
    (value) => {
      const result =
        isUnicodeSymbolCharacter(value) || isUnicodePunctuationCharacter(value)
      expect(result).toBeTruthy()
    }
  )

  test.each(aToZLower)(
    'test special characters with alphabetic lower characters should be false',
    (value) => {
      const result =
        isUnicodeSymbolCharacter(value) || isUnicodePunctuationCharacter(value)
      expect(result).toBeFalsy()
    }
  )

  test.each(aToZUpper)(
    'test special characters with alphabetic upper characters should be false',
    (value) => {
      const result =
        isUnicodeSymbolCharacter(value) || isUnicodePunctuationCharacter(value)
      expect(result).toBeFalsy()
    }
  )

  test.each(testNumberCases)(
    'test special characters with number characters should be false',
    (value) => {
      const result =
        isUnicodeSymbolCharacter(value) || isUnicodePunctuationCharacter(value)
      expect(result).toBeFalsy()
    }
  )

  test.each(testNumberCasesNumber)(
    'test special characters with numbers should be false',
    (value) => {
      const result =
        isUnicodeSymbolCharacter(value) || isUnicodePunctuationCharacter(value)
      expect(result).toBeFalsy()
    }
  )

  test.each(notString)(
    'test special characters with different objects should be false',
    (value) => {
      const result =
        isUnicodeSymbolCharacter(value) || isUnicodePunctuationCharacter(value)
      expect(result).toBeFalsy()
    }
  )
})
