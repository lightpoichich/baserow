<template>
  <Context :style="{ padding: '16px 20px', width: '320px' }">
    <TimelineViewSettingsForm
      ref="datesFieldSelectForm"
      :all-date-fields="allDateFields"
      :view="view"
      :read-only="readOnly"
      @submitted="submitted"
    >
      <div class="actions">
        <div v-if="!readOnly">
          <Button type="secondary" :loading="loading" :disabled="loading">
            {{ $t('selectDateFieldContext.update') }}</Button
          >
        </div>
      </div>
    </TimelineViewSettingsForm>
  </Context>
</template>

<script>
import context from '@baserow/modules/core/mixins/context'
import { notifyIf } from '@baserow/modules/core/utils/error'
import TimelineViewSettingsForm from '@baserow_premium/components/views/timeline/TimelineViewSettingsForm'

export default {
  name: 'SelectDateFieldContext',
  components: {
    TimelineViewSettingsForm,
  },
  mixins: [context],
  props: {
    view: {
      type: Object,
      required: true,
    },
    fields: {
      type: Array,
      required: true,
    },
    readOnly: {
      type: Boolean,
      required: true,
    },
  },
  data() {
    return {
      loading: false,
    }
  },
  computed: {
    allDateFields() {
      return this.fields.filter((f) => {
        return this.$registry.get('field', f.type).canRepresentDate(f)
      })
    },
  },
  methods: {
    async submitted(values) {
      this.loading = true
      const view = this.view
      this.$store.dispatch('view/setItemLoading', { view, value: true })
      try {
        await this.$store.dispatch('view/update', {
          view,
          values: {
            start_date_field: values.startDateFieldId,
            end_date_field: values.endDateFieldId,
          },
        })
        this.$emit('refresh', {
          includeFieldOptions: true,
        })
        this.hide()
      } catch (error) {
        notifyIf(error, 'view')
      } finally {
        this.loading = false
        this.$store.dispatch('view/setItemLoading', { view, value: false })
      }
    },
  },
}
</script>
