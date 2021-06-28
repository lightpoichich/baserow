import { mapGetters } from 'vuex'
import { notifyIf } from '@baserow/modules/core/utils/error'
import { clone } from '@baserow/modules/core/utils/object'

export default {
  props: {
    storePrefix: {
      type: String,
      required: true,
    },
  },
  methods: {
    async updateForm(values) {
      const view = this.view
      this.$store.dispatch('view/setItemLoading', { view, value: true })

      try {
        await this.$store.dispatch('view/update', {
          view,
          values,
        })
      } catch (error) {
        notifyIf(error, 'view')
      }

      this.$store.dispatch('view/setItemLoading', { view, value: false })
    },
    async updateFieldOptionsOfField(form, field, values) {
      try {
        await this.$store.dispatch(
          this.storePrefix + 'view/form/updateFieldOptionsOfField',
          {
            form,
            field,
            values,
          }
        )
      } catch (error) {
        notifyIf(error, 'view')
      }
    },
    async updateFieldOptionsOfAllFields(form, values) {
      const oldFieldOptions = clone(this.fieldOptions)
      const newFieldOptions = {}
      Object.keys(this.fieldOptions).forEach((fieldId) => {
        newFieldOptions[fieldId] = values
      })

      try {
        await this.$store.dispatch(
          this.storePrefix + 'view/form/updateAllFieldOptions',
          {
            form,
            newFieldOptions,
            oldFieldOptions,
          }
        )
      } catch (error) {
        notifyIf(error, 'view')
      }
    },
  },
  beforeCreate() {
    this.$options.computed = {
      ...(this.$options.computed || {}),
      ...mapGetters({
        fieldOptions:
          this.$options.propsData.storePrefix + 'view/form/getAllFieldOptions',
      }),
    }
  },
}
