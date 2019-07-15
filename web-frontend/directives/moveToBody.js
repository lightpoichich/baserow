/**
 * This directive moves the whole element to the document body so that it can be
 * positioned over another element.
 */
export default {
  inserted: el => {
    const body = document.body

    // The element is added as first child in the body so that child contexts
    // are being shown on top of their parent.
    body.insertBefore(el, body.firstChild)
  },
  unbind: el => {
    if (el.parentNode) {
      el.parentNode.removeChild(el)
    }
  }
}
