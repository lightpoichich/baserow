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

  const notString = [{}, 5, []]

  const aToZMoreThanOneChar = ['aa', 'Aa', 'bbb', 'BBB']

  const testNumberCases = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
  const testNumberCasesNumber = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

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

  const specialCharacterCases = [...symbolCharacters, ...punctuationCharacters]

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

  test.each(symbolCharacters)(
    'test symbol characters should be true',
    (value) => {
      expect(isUnicodeSymbolCharacter(value)).toBeTruthy()
    }
  )

  test.each(punctuationCharacters)(
    'test punctuation characters should be true',
    (value) => {
      expect(isUnicodePunctuationCharacter(value)).toBeTruthy()
    }
  )

  test.each(aToZLower)(
    'test symbol characters with alphabetic lower characters should be false',
    (value) => {
      expect(isUnicodeSymbolCharacter(value)).toBeFalsy()
    }
  )

  test.each(aToZLower)(
    'test punctuation characters with alphabetic lower characters should be false',
    (value) => {
      expect(isUnicodePunctuationCharacter(value)).toBeFalsy()
    }
  )

  test.each(aToZUpper)(
    'test symbol characters with alphabetic upper characters should be false',
    (value) => {
      expect(isUnicodeSymbolCharacter(value)).toBeFalsy()
    }
  )

  test.each(aToZUpper)(
    'test punctuation characters with alphabetic upper characters should be false',
    (value) => {
      expect(isUnicodePunctuationCharacter(value)).toBeFalsy()
    }
  )

  test.each(testNumberCases)(
    'test symbol characters with number characters should be false',
    (value) => {
      expect(isUnicodeSymbolCharacter(value)).toBeFalsy()
    }
  )

  test.each(testNumberCases)(
    'test punctuation characters with number characters should be false',
    (value) => {
      expect(isUnicodePunctuationCharacter(value)).toBeFalsy()
    }
  )

  test.each(testNumberCasesNumber)(
    'test symbol characters with numbers should be false',
    (value) => {
      expect(isUnicodeSymbolCharacter(value)).toBeFalsy()
    }
  )

  test.each(notString)(
    'test symbol characters with different objects should be false',
    (value) => {
      expect(isUnicodeSymbolCharacter(value)).toBeFalsy()
    }
  )

  test.each(testNumberCasesNumber)(
    'test punctuation characters with numbers should be false',
    (value) => {
      expect(isUnicodePunctuationCharacter(value)).toBeFalsy()
    }
  )

  test.each(notString)(
    'test punctuation characters with different objects should be false',
    (value) => {
      expect(isUnicodePunctuationCharacter(value)).toBeFalsy()
    }
  )
})
