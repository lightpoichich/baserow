<template>
  <div>
    <div v-if="loadingViews" :class="{ 'loading-overlay': loadingViews }"></div>
    <div v-else>
      <Error :error="error"></Error>
      <form @submit.prevent="submit">
        <div class="row">
          <div class="col col-12">
            <div class="control">
              <label class="control__label">Select the view to export:</label>
              <div class="control__elements">
                <ExportTableDropdown
                  v-model="values.view_id"
                  :views="views"
                  :loading="loading"
                  :table="table"
                ></ExportTableDropdown>
              </div>
            </div>
            <ExporterTypeChoices
              v-model="values.exporter_type"
              :exporter-types="exporterTypes"
              :loading="loading"
            ></ExporterTypeChoices>
            <div v-if="$v.values.exporter_type.$error" class="error">
              No exporter type available please select a different view or
              entire table.
            </div>
          </div>
        </div>
        <component
          :is="exporterComponent"
          :loading="loading"
          @values-changed="valuesChanged"
        />
        <ExportTableLoadingBar
          :job="job"
          :loading="loading"
          :disabled="formIsInvalid"
        ></ExportTableLoadingBar>
      </form>
    </div>
  </div>
</template>

<script>
import error from '@baserow/modules/core/mixins/error'
import ExportTableDropdown from '@baserow/modules/database/components/export/ExportTableDropdown'
import form from '@baserow/modules/core/mixins/form'
import ExporterTypeChoices from '@baserow/modules/database/components/export/ExporterTypeChoices'
import ExportTableLoadingBar from '@baserow/modules/database/components/export/ExportTableLoadingBar'
import { populateView } from '@baserow/modules/database/store/view'
import { mapState } from 'vuex'
import ViewService from '@baserow/modules/database/services/view'
import { required } from 'vuelidate/lib/validators'

export default {
  name: 'ExportTableForm',
  components: {
    ExporterTypeChoices,
    ExportTableDropdown,
    ExportTableLoadingBar,
  },
  mixins: [error, form],
  props: {
    table: {
      type: Object,
      required: true,
    },
    job: {
      type: Object,
      required: false,
      default: null,
    },
    view: {
      type: Object,
      required: false,
      default: null,
    },
    loading: {
      type: Boolean,
      required: true,
    },
  },
  data() {
    return {
      views: [],
      loadingViews: true,
      values: {
        view_id: this.view === null ? null : this.view.id,
        exporter_type: null,
      },
    }
  },
  computed: {
    selectedView() {
      if (this.values.view_id === null) {
        return null
      } else {
        const index = this.views.findIndex((view) => {
          return view.id === this.values.view_id
        })
        return this.views[index]
      }
    },
    exporterTypes() {
      const types = Object.values(this.$registry.getAll('exporter'))
      return types.filter((exporterType) => {
        if (this.selectedView !== null) {
          return exporterType
            .getSupportedViews()
            .includes(this.selectedView.type)
        } else {
          return exporterType.getCanExportTable()
        }
      })
    },
    firstExporterType() {
      return this.exporterTypes.length > 0 ? this.exporterTypes[0].type : null
    },
    exporterComponent() {
      if (!this.values.exporter_type) {
        return null
      } else {
        const index = this.exporterTypes.findIndex((exporterType) => {
          return exporterType.type === this.values.exporter_type
        })
        const exporterType = this.exporterTypes[index]
        return exporterType.getFormComponent()
      }
    },
    ...mapState({
      selectedTableViews: (state) => state.view.items,
    }),
    formIsInvalid() {
      return !this.isFormValid()
    },
  },
  watch: {
    selectedView() {
      this.values.exporter_type = this.firstExporterType
      this.$v.$touch()
    },
  },
  created() {
    this.fetchViews()
    this.values.exporter_type = this.firstExporterType
  },
  methods: {
    valuesChanged(values) {
      this.$emit('values-changed', values)
    },
    async fetchViews() {
      this.loadingViews = true
      if (this.table._.selected) {
        this.views = this.selectedTableViews
      } else {
        // Show loading state for entire modal using overlay
        const { data: viewsData } = await ViewService(this.$client).fetchAll(
          this.table.id
        )
        viewsData.forEach((v) => populateView(v, this.$registry))
        this.views = viewsData
      }
      this.loadingViews = false
    },
  },
  validations: {
    values: {
      exporter_type: { required },
    },
  },
}
</script>
