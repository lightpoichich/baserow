import { DataSyncType } from '@baserow/modules/database/dataSyncTypes'

import LocalBaserowTableDataSync from '@baserow_enterprise/components/dataSync/LocalBaserowTableDataSync'
import EnterpriseFeatures from '@baserow_enterprise/features'
import EnterpriseModal from '@baserow_enterprise/components/EnterpriseModal'
import JiraIssuesDataSyncForm from '@baserow_enterprise/components/dataSync/JiraIssuesDataSyncForm'

export class LocalBaserowTableDataSyncType extends DataSyncType {
  static getType() {
    return 'local_baserow_table'
  }

  getIconClass() {
    return 'iconoir-menu'
  }

  getName() {
    const { i18n } = this.app
    return i18n.t('enterpriseDataSyncType.localBaserowTable')
  }

  getFormComponent() {
    return LocalBaserowTableDataSync
  }

  isDeactivated(workspaceId) {
    return !this.app.$hasFeature(EnterpriseFeatures.DATA_SYNC, workspaceId)
  }

  getDeactivatedClickModal() {
    return EnterpriseModal
  }
}

export class JiraIssuesDataSyncType extends DataSyncType {
  static getType() {
    return 'jira_issues'
  }

  getIconClass() {
    return 'iconoir-git-pull-request'
  }

  getName() {
    const { i18n } = this.app
    return i18n.t('dataSyncType.jiraIssues')
  }

  getFormComponent() {
    return JiraIssuesDataSyncForm
  }

  isDeactivated(workspaceId) {
    return !this.app.$hasFeature(EnterpriseFeatures.DATA_SYNC, workspaceId)
  }

  getDeactivatedClickModal() {
    return EnterpriseModal
  }
}
