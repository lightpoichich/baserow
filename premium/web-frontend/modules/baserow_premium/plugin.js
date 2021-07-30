import { PremiumPlugin } from '@baserow_premium/plugins'
import {
  JSONTableExporter,
  XMLTableExporter,
} from '@baserow_premium/tableExporterTypes'
import {
  DashboardType,
  GroupsAdminType,
  UsersAdminType,
} from '@baserow_premium/adminTypes'
import rowCommentsStore from '@baserow_premium/store/row_comments'
import RowCommentsSidebar from '@baserow_premium/components/row_comments/RowCommentsSidebar'
import { registerRealtimeEvents } from '@baserow_premium/realtime'

export default ({ store, app }) => {
  store.registerModule('row_comments', rowCommentsStore)

  app.$registry.register('plugin', new PremiumPlugin())
  app.$registry.register('admin', new DashboardType())
  app.$registry.register('admin', new UsersAdminType())
  app.$registry.register('admin', new GroupsAdminType())
  app.$registry.register('exporter', new JSONTableExporter())
  app.$registry.register('exporter', new XMLTableExporter())

  const databaseApplication = app.$registry.get('application', 'database')
  databaseApplication.componentPlugins.RowEditModal = RowCommentsSidebar

  registerRealtimeEvents(app.$realtime)
}
