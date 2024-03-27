<template>
  <Modal>
    <h2 class="modal__title">
      {{ $t('selectDateFieldModal.chooseDateField') }}
    </h2>
    <div class="modal__content">
      <Error :error="error"></Error>
      <DateFieldSelectForm
        ref="dateFieldSelectForm"
        :date-fields="dateFields"
        :date-field-id="dateFieldId"
        :table="table"
        @submitted="submitted"
      >
      </DateFieldSelectForm>
    </div>

    <div class="modal__footer">
      <Button
        type="primary"
        :loading="loading"
        :disabled="loading"
        @click="$refs.dateFieldSelectForm.submit()"
      >
        {{ $t('selectDateFieldModal.save') }}</Button
      >
    </div>
  </Modal>
</template>

<script>
import modal from '@baserow/modules/core/mixins/modal'
import error from '@baserow/modules/core/mixins/error'
import DateFieldSelectForm from '@baserow_premium/components/views/calendar/DateFieldSelectForm'

export default {
  name: 'SelectDateFieldModal',
  components: {
    DateFieldSelectForm,
  },
  mixins: [modal, error],
  props: {
    view: {
      type: Object,
      required: true,
    },
    table: {
      type: Object,
      required: true,
    },
    fields: {
      type: Array,
      required: true,
    },
    database: {
      type: Object,
      required: true,
    },
    dateFieldId: {
      type: Number,
      required: false,
      default: null,
    },
  },
  data() {
    return {
      loading: false,
    }
  },
  computed: {
    dateFields() {
      return this.fields.filter((f) => {
        return this.$registry.get('field', f.type).canRepresentDate(f)
      })
    },
  },
  methods: {
    async submitted(values) {
      this.loading = true
      this.hideError()
      const view = this.view
      this.$store.dispatch('view/setItemLoading', { view, value: true })
      try {
        await this.$store.dispatch('view/update', {
          view,
          values: { date_field: values.dateFieldId },
        })
        this.$emit('refresh', {
          includeFieldOptions: true,
        })
        this.hide()
      } catch (error) {
        this.handleError(error)
      } finally {
        this.loading = false
        this.$store.dispatch('view/setItemLoading', { view, value: false })
      }
    },
  },
}
</script>
