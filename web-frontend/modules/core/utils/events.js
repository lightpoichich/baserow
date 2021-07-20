export function isUnicodeLetterCharacter(str) {
  /*
  This function determines whether the pressed key is a alphabetic character
  if (charRegex.test(str)) {
    return true
  }
  return false
   */
  const charRegex = /^\p{L}\p{M}*$/iu
  return charRegex.test(str)
}

export function isUnicodeNumberCharacter(str) {
  /*
  This function determines whether the pressed key is a number
   */
  const numberRegex = /^\p{N}$/iu
  if (numberRegex.test(str)) {
    return true
  }
  return false
}

export function isUnicodeSymbolCharacter(str) {
  /*
  This function determines whether the pressed key is a math symbol, currency sign, etc.
   */
  const symbolRegex = /^\p{S}$/iu
  if (symbolRegex.test(str)) {
    return true
  }
  return false
}

export function isUnicodePunctuationCharacter(str) {
  /*
  This function determines whether the pressed key is a punctuation character
   */
  const punctuationRegex = /^\p{P}$/iu
  if (punctuationRegex.test(str)) {
    return true
  }
  return false
}

export function isPrintableUnicodeCharacterKeyPress(event) {
  /*
  This function is a helper which determines whether the pressed key
  is either a
    UnicodeLetterCharacter or
    UnicodeNumberCharacter or
    UnicodeSymbolCharacter or
    UnicodePunctuationCharacter
  hereby defined as a 'printable character'
   */
  const { key } = event
  const isPrintableCharacter =
    isUnicodeLetterCharacter(key) ||
    isUnicodeNumberCharacter(key) ||
    isUnicodeSymbolCharacter(key) ||
    isUnicodePunctuationCharacter(key)

  return isPrintableCharacter
}
