<script>
import AppLayoutPreview from '@baserow/modules/core/components/onboarding/AppLayoutPreview'
import {
  DatabaseOnboardingType,
  DatabaseImportOnboardingType,
  DatabaseScratchTrackOnboardingType,
  DatabaseViewOnboardingType,
} from '@baserow/modules/database/onboardingTypes'
import DatabaseTablePreview from '@baserow/modules/database/components/onboarding/DatabaseTablePreview.vue'
import { populateTable } from '@baserow/modules/database/store/table'
import { clone } from '@baserow/modules/core/utils/object'
import DatabaseGalleryPreview from '@baserow/modules/database/components/onboarding/DatabaseGalleryPreview.vue'

// TODO: make it more flexible for premium usage
const previewRegistry = {
  table: DatabaseTablePreview,
  gallery: DatabaseGalleryPreview,
}

export default {
  name: 'DatabaseAppLayoutPreview',
  extends: AppLayoutPreview,
  computed: {
    trackTableName() {
      return this.data[DatabaseScratchTrackOnboardingType.getType()]?.tableName
    },
    importTableName() {
      return this.data[DatabaseImportOnboardingType.getType()]?.tableName
    },
    tableName() {
      return this.trackTableName || this.importTableName
    },
    viewType() {
      return (
        this.data[DatabaseViewOnboardingType.getType()]?.viewType || 'table'
      )
    },
    applications() {
      const applications = AppLayoutPreview.computed.applications.call(this)
      applications[0].name =
        this.data[DatabaseOnboardingType.getType()]?.name || ''

      if (this.tableName) {
        applications[0]._.selected = true
        const baseTable = populateTable({
          id: 0,
          name: '',
          order: 0,
          database_id: 0,
        })

        const table = clone(baseTable)
        table._.selected = true
        table.name = this.tableName
        const table2 = clone(baseTable)
        table2.id = -1
        const table3 = clone(baseTable)
        table3.id = -2

        applications[0].tables = [table, table2, table3]
      }

      return applications
    },
    col2Component() {
      // FIXME: for some reason using registry is not reactive
      return this.trackTableName && this.applications[0].tables.length > 0
        ? previewRegistry[this.viewType] || DatabaseTablePreview
        : null
    },
  },
  mounted() {
    // Add a new selected object to the store, so that it works with the sidebar, but
    // doesn't have influence over the actual selected state of the application.
    const application = { id: this.applications[0].id, _: {} }
    this.$store.commit('application/SET_SELECTED', application)
  },
}
</script>
