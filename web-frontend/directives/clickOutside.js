import { isElement } from '@/utils/dom'

/**
 * This directive calls a custom method if the user clicks outside of the
 * element.
 */
export default {
  bind: (el, binding, vnode) => {
    el.clickOutsideEvent = event => {
      if (!isElement(el, event.target)) {
        vnode.context[binding.expression](event)
      }
    }
    document.body.addEventListener('click', el.clickOutsideEvent)
  },
  unbind: el => {
    document.body.removeEventListener('click', el.clickOutsideEvent)
  }
}
