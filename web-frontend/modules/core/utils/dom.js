/**
 * Checks if the target is the same as the provided element of that the element
 * contains the target. Returns true is this is the case.
 *
 * @returns boolean
 */
export const isElement = (element, target) => {
  return element !== null && (element === target || element.contains(target))
}

/**
 * Checks if the provided object is an html dom element.
 *
 * @returns boolean
 */
export const isDomElement = (obj) => {
  try {
    return obj instanceof HTMLElement
  } catch (e) {
    return (
      typeof obj === 'object' &&
      obj.nodeType === 1 &&
      typeof obj.style === 'object' &&
      typeof obj.ownerDocument === 'object'
    )
  }
}

/**
 * This function will focus a contenteditable and place the cursor at the end.
 *
 * @param element
 */
export const focusEnd = (element) => {
  element.focus()

  if (
    typeof window.getSelection !== 'undefined' &&
    typeof document.createRange !== 'undefined'
  ) {
    const range = document.createRange()
    range.selectNodeContents(element)
    range.collapse(false)
    const sel = window.getSelection()
    sel.removeAllRanges()
    sel.addRange(range)
  } else if (typeof document.body.createTextRange !== 'undefined') {
    const textRange = document.body.createTextRange()
    textRange.moveToElementText(element)
    textRange.collapse(false)
    textRange.select()
  }
}
