<template>
  <div class="box">
    <h2 :style="{ marginBottom: '32px' }">
      {{ $t('initTimelineViewSettings.settings') }}
    </h2>
    <Error :error="error"></Error>
    <TimelineViewSettingsForm
      ref="dateFieldSelectForm"
      :all-date-fields="dateFields"
      :view="view"
      @submitted="submitted"
    >
      <div class="actions">
        <div class="align-right">
          <Button type="primary" :loading="loading" :disabled="loading">
            {{ $t('selectDateFieldModal.save') }}</Button
          >
        </div>
      </div>
    </TimelineViewSettingsForm>
  </div>
</template>

<script>
import modal from '@baserow/modules/core/mixins/modal'
import error from '@baserow/modules/core/mixins/error'
import TimelineViewSettingsForm from './TimelineViewSettingsForm'

export default {
  name: 'InitTimelineViewSettings',
  components: {
    TimelineViewSettingsForm,
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
          values: {
            start_date_field: values.startDateFieldId,
            end_date_field: values.endDateFieldId,
          },
        })
        this.$emit('refresh', {
          includeFieldOptions: true,
        })
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

<style scoped>
.box {
  margin: 20px auto;
  max-width: 480px;
}
</style>
