import element from '@baserow/modules/builder/mixins/element'
import { mapGetters } from 'vuex'
import { PLACEMENTS } from '@baserow/modules/builder/enums'

export default {
  mixins: [element],
  computed: {
    ...mapGetters({
      elementSelected: 'element/getSelected',
    }),
    PLACEMENTS: () => PLACEMENTS,
    children() {
      return this.$store.getters['element/getChildren'](this.page, this.element)
    },
    elementSelectedId() {
      return this.elementSelected?.id
    },
  },
}
