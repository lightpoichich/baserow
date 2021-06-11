<template>
  <Modal :sidebar="true">
    <template #sidebar>
      <div v-if="loading" class="loading-absolute-center"></div>
      <TrashSidebar
        v-else-if="groups.length > 0"
        :groups="groups"
        :selected-group="selectedGroup"
        :selected-application="selectedApplication"
        @selected="selectGroupOrApp"
      >
        <a class="modal__close" @click="hide()">
          <i class="fas fa-times"></i>
        </a>
      </TrashSidebar>
    </template>
    <template #content>
      <Error :error="error"></Error>
      <div v-if="loading" class="loading-absolute-center"></div>
      <div v-else-if="groups.length === 0" class="placeholder">
        <div class="placeholder__icon">
          <i class="fas fa-layer-group"></i>
        </div>
        <h1 class="placeholder__title">No groups found</h1>
        <p class="placeholder__content">
          You aren't a member of any group. Applications like databases belong
          to a group, so in order to create them you need to create a group.
        </p>
      </div>
      <TrashContent
        v-else
        :selected-group="selectedGroup"
        :selected-application="selectedApplication"
        :trash-contents="trashContents"
        :loading-contents="loadingContents"
        @empty="onEmpty"
        @restore="onRestore"
      ></TrashContent>
    </template>
  </Modal>
</template>

<script>
import modal from '@baserow/modules/core/mixins/modal'
import TrashService from '@baserow/modules/core/services/trash'
import { notifyIf } from '@baserow/modules/core/utils/error'
import TrashSidebar from '@baserow/modules/core/components/trash/TrashSidebar'
import TrashContent from '@baserow/modules/core/components/trash/TrashContents'
import error from '@baserow/modules/core/mixins/error'

export default {
  name: 'TrashModal',
  components: { TrashSidebar, TrashContent },
  mixins: [modal, error],
  props: {},
  data() {
    return {
      loading: true,
      loadingContents: true,
      groups: [],
      trashContents: [],
      selectedGroup: null,
      selectedApplication: null,
    }
  },
  methods: {
    async show(...args) {
      modal.methods.show.call(this, ...args)

      this.loading = true
      this.groups = []
      this.trashContents = []
      this.selectedGroup = null
      this.selectedApplication = null

      try {
        const { data } = await TrashService(this.$client).fetchStructure()
        this.groups = data.groups
        this.selectGroupOrApp({ group: this.groups[0] })
      } catch (error) {
        notifyIf(error, 'trash')
        this.hide()
      }
      this.loading = false
    },
    async fetchContents() {
      this.loadingContents = true
      this.trashContents = []
      try {
        const { data } = await TrashService(this.$client).fetchContents({
          groupId: this.selectedGroup.id,
          applicationId:
            this.selectedApplication !== null
              ? this.selectedApplication.id
              : null,
        })
        this.trashContents = data.results
      } catch (error) {
        this.handleError(error, 'trash')
      }
      this.loadingContents = false
    },
    selectGroupOrApp({ group, application = null }) {
      this.selectedGroup = group
      this.selectedApplication = application
      this.fetchContents()
    },
    async onRestore(trashEntry) {
      try {
        trashEntry.loading = true
        await TrashService(this.$client).restore(trashEntry)
        const index = this.trashContents.findIndex(
          (t) => t.id === trashEntry.id
        )
        this.trashContents.splice(index, 1)
        this.updateStructureIfGroupOrAppRestored(trashEntry)
      } catch (error) {
        this.handleError(error, 'trash')
      }
      trashEntry.loading = false
    },
    updateStructureIfGroupOrAppRestored(trashEntry) {
      const trashItemId = trashEntry.trash_item_id
      const trashItemType = trashEntry.trash_item_type
      if (trashItemType === 'group') {
        const index = this.groups.findIndex((group) => group.id === trashItemId)
        this.groups[index].trashed = false
      } else if (trashItemType === 'application') {
        const index = this.selectedGroup.applications.findIndex(
          (app) => app.id === trashItemId
        )
        this.selectedGroup.groups[index].trashed = false
      }
    },
    async onEmpty() {
      this.loadingContents = true
      try {
        const applicationIdOrNull =
          this.selectedApplication !== null ? this.selectedApplication.id : null
        await TrashService(this.$client).emptyContents({
          groupId: this.selectedGroup.id,
          applicationId: applicationIdOrNull,
        })
        this.removeGroupOrAppFromSidebarIfNowPermDeleted()
        this.trashContents = []
        this.loadingContents = false
      } catch (error) {
        this.handleError(error, 'trash')
      }
    },
    removeSelectedAppFromSidebar() {
      const applicationId = this.selectedApplication.id

      const indexToDelete = this.selectedGroup.applications.findIndex(
        (app) => app.id === applicationId
      )
      this.selectedGroup.applications.splice(indexToDelete, 1)
      if (this.selectedGroup.applications.length > 0) {
        this.selectedApplication = this.selectedGroup.applications[0]
      } else {
        this.selectedApplication = null
      }
    },
    removeSelectedGroupFromSidebar() {
      const indexToDelete = this.groups.findIndex(
        (group) => group.id === this.selectedGroup.id
      )
      this.groups.splice(indexToDelete, 1)
      if (this.groups.length > 0) {
        this.selectedGroup = this.groups[0]
      } else {
        this.selectedGroup = null
      }
    },
    removeGroupOrAppFromSidebarIfNowPermDeleted() {
      if (
        this.selectedApplication !== null &&
        this.selectedApplication.trashed
      ) {
        this.removeSelectedAppFromSidebar()
      } else if (this.selectedGroup.trashed) {
        this.removeSelectedGroupFromSidebar()
      }
    },
  },
}
</script>
