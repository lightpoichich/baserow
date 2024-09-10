import MoveToBody from '@baserow/modules/core/mixins/moveToBody'

export default {
  mixins: [MoveToBody],
  data() {
    return {
      open: false,
      // Firefox and Chrome both can both have a different `target` element on `click`
      // when you release the mouse at different coordinates. Therefore we expect this
      // variable to be set on mousedown to be consistent.
      downElement: null,
      headerHeight: 0,
      footerHeight: 0,
      originalHeight: 0,
    }
  },
  mounted() {
    this.$bus.$on('close-modals', this.hide)
  },
  beforeDestroy() {
    this.$bus.$off('close-modals', this.hide)
    window.removeEventListener('resize', this.setModalHeight)
    if (this.observer) this.observer.disconnect()
  },
  destroyed() {
    window.removeEventListener('keyup', this.keyup)
  },
  computed: {
    nonFullHeightModal() {
      return !this.fullHeight && this.size !== 'fullscreen'
    },
  },
  methods: {
    /**
     * Toggle the open state of the modal.
     */
    toggle(value) {
      if (value === undefined) {
        value = !this.open
      }

      if (value) {
        this.show()
      } else {
        this.hide()
      }
    },
    /**
     * Returns if the modal is open or not.
     */
    isOpen() {
      return this.open
    },
    /**
     * Show the modal.
     */
    show() {
      this.open = true
      this.$emit('show')
      window.addEventListener('keyup', this.keyup)

      document.body.classList.add('prevent-scroll')
      const mouseDownEvent = (event) => {
        this.downElement = event.target
      }
      document.body.addEventListener('mousedown', mouseDownEvent)

      this.$nextTick(() => {
        if (this.nonFullHeightModal) {
          this.setOriginalHeight()
          this.setModalHeight()
          window.addEventListener('resize', this.setModalHeight)
          this.initObserver()
        }

        this.$once('hidden', () => {
          document.body.removeEventListener('mousedown', mouseDownEvent)
          document.body.classList.remove('prevent-scroll')
          window.removeEventListener('keyup', this.keyup)
        })
      })
    },
    /**
     * Hide the modal.
     */
    hide(emit = true) {
      if (!this.open) return

      // This is a temporary fix. What happens is the modal is opened by a context menu
      // item and the user closes the modal, the element is first deleted and then the
      // click outside event of the context is fired. It then checks if the click was
      // inside one of his children, but because the modal element doesn't exists
      // anymore it thinks it was outside, so is closes the context menu which we don't
      // want automatically.
      setTimeout(() => {
        this.open = false
      })

      if (emit) this.$emit('hidden')
    },
    /**
     * If someone actually clicked on the modal wrapper and not one of his children the
     * modal should be closed.
     */
    outside() {
      if (this.downElement === this.$refs.modalWrapper) this.hide()
    },
    /**
     * When the escape key is pressed the modal needs to be hidden.
     */
    keyup(event) {
      if (event.key === 'Escape') this.hide()
    },

    /**
     * This method set the modal height in order to make the content scrollable.
     * It's useful only in the non full height mode.
     */

    setModalHeight() {
      const modal = this.$refs.modal

      if (!modal) return

      // Get the value of the CSS variable --modal-max-height
      const modalMaxHeight = getComputedStyle(
        this.$refs.modal
      ).getPropertyValue('--modal-max-height')

      // Convert 80vh to pixels
      const viewportHeight = window.innerHeight
      const maxHeightInPixels =
        (parseFloat(modalMaxHeight) / 100) * viewportHeight

      // If modal height is greater than the max height, then we set the height so the content is scrollable
      if (this.originalHeight > Math.floor(maxHeightInPixels))
        modal.style.height = modalMaxHeight.trim()
      else modal.style.height = 'auto'
    },
    /**
     * This methods add an observer on the modal slot content.
     */
    initObserver() {
      const config = {
        subtree: true,
        childList: true,
      }
      const self = this
      const callback = () => {
        self.$nextTick(() => {
          self.slotContentChanged()
        })
      }
      const observer = new MutationObserver(callback)
      observer.observe(this.$refs.content, config)
      this.observer = observer
    },
    slotContentChanged() {
      this.setOriginalHeight()
    },
    setOriginalHeight() {
      this.originalHeight = this.$refs.modal.scrollHeight
    },
  },
}
