export function isAlphabeticCharacter(str) {
  /*
  This function determines whether the pressed key is a alphabetic character
   */
  const charRegex = /^[A-Za-z]$/
  if (charRegex.test(str)) {
    return true
  }
  return false
}

export function isNumberCharacter(str) {
  /*
  This function determines whether the pressed key is a number
   */
  const numberRegex = /^\d$/
  if (numberRegex.test(str)) {
    return true
  }
  return false
}

export function isSpecialCharacter(str) {
  /*
  This function determines whether the pressed key is a special character
   */
  const specialCharRegex = /^[<>{}"/|;:.,~!?@#$%=&*§[\]\\´`+'\-_€^]$/
  if (specialCharRegex.test(str)) {
    return true
  }
  return false
}

export function isPrintableCharacterKeyPress(event) {
  /*
  This function is a helper which determines whether the pressed key
  is either a
    CharacterKey or
    NumberKey or
    SpecialCharacter
  hereby defined as a 'printable character'
   */
  const { key } = event
  const isPrintableCharacter =
    isAlphabeticCharacter(key) ||
    isNumberCharacter(key) ||
    isSpecialCharacter(key)

  return isPrintableCharacter
}
