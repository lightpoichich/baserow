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
        :loading-next-page="loadingNextPage"
        :entry-count="totalServerSideTrashContentsCount"
        @empty="onEmpty"
        @restore="onRestore"
        @load-next-page="loadTrashContentsPage"
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
  props: {
    initialGroup: {
      type: Object,
      required: false,
      default: null,
    },
    initialApplication: {
      type: Object,
      required: false,
      default: null,
    },
  },
  data() {
    return {
      loading: true,
      loadingContents: true,
      loadingNextPage: false,
      groups: [],
      trashContents: [],
      selectedGroup: null,
      selectedApplication: null,
      totalServerSideTrashContentsCount: 0,
    }
  },
  methods: {
    async show(...args) {
      /**
       * Loads the structure of the trash modal from the server, selects an initial
       * group or application depending on the props and shows the trash modal.
       **/
      modal.methods.show.call(this, ...args)

      this.loading = true
      this.groups = []
      this.trashContents = []
      this.selectedGroup = null
      this.selectedApplication = null
      this.hideError()
      this.totalServerSideTrashContentsCount = 0

      try {
        const { data } = await TrashService(this.$client).fetchStructure()
        this.groups = data.groups
        const group = this.initialGroup || this.groups[0]
        this.selectGroupOrApp({ group, application: this.initialApplication })
      } catch (error) {
        notifyIf(error, 'trash')
        this.hide()
      }
      this.loading = false
    },
    async loadTrashContentsPage(nextPage) {
      /**
       * Loads the next page of trash contents for the currently selected application.
       */
      this.hideError()
      try {
        this.loadingNextPage = true
        const { data } = await TrashService(this.$client).fetchContents({
          page: nextPage,
          groupId: this.selectedGroup.id,
          applicationId:
            this.selectedApplication !== null
              ? this.selectedApplication.id
              : null,
        })
        this.totalServerSideTrashContentsCount = data.count
        this.trashContents = this.trashContents.concat(data.results)
      } catch (error) {
        this.handleError(error, 'trash')
      }
      this.loadingNextPage = false
    },
    selectGroupOrApp({ group, application = null }) {
      /**
       * Switches to a different group or application to display the trash contents for
       * and triggers the fetch for the first page of contents.
       */
      this.selectedGroup = group
      this.selectedApplication = application
      this.loadTrashContentsPage(0)
    },
    async onRestore(trashEntry) {
      /**
       * Triggered when a user requests a trashEntry be restored. Sends the request to
       * the server, updates the client side state if successful and updates the trash
       * structure if say a group or application was restored.
       */
      this.hideError()
      try {
        trashEntry.loading = true
        await TrashService(this.$client).restore({
          trash_item_type: trashEntry.trash_item_type,
          trash_item_id: trashEntry.trash_item_id,
          parent_trash_item_id: trashEntry.parent_trash_item_id,
        })
        const index = this.trashContents.findIndex(
          (t) => t.id === trashEntry.id
        )
        this.trashContents.splice(index, 1)
        this.totalServerSideTrashContentsCount--
        this.updateStructureIfGroupOrAppRestored(trashEntry)
      } catch (error) {
        this.handleError(error, 'trash')
      }
      trashEntry.loading = false
    },
    updateStructureIfGroupOrAppRestored(trashEntry) {
      /**
       * If a group or app is trashed it is displayed with a strike through it's text.
       * This method checks if a restored trash entry is a group or application and
       * if so updates the state of said group/app so it no longer is displayed as
       * trashed.
       */
      const trashItemId = trashEntry.trash_item_id
      const trashItemType = trashEntry.trash_item_type
      if (trashItemType === 'group') {
        const index = this.groups.findIndex((group) => group.id === trashItemId)
        this.groups[index].trashed = false
      } else if (trashItemType === 'application') {
        const index = this.selectedGroup.applications.findIndex(
          (app) => app.id === trashItemId
        )
        this.selectedGroup.applications[index].trashed = false
      }
    },
    async onEmpty() {
      /**
       * Triggered when the user has requested the currently selected group or app
       * should be emptied. If the selected item is trashed itself the empty operation
       * will permanently delete the selected item also. Once emptied this method will
       * ensure that any now permanently deleted groups or apps are removed from the
       * sidebar.
       */
      this.hideError()
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
        this.totalServerSideTrashContentsCount = 0
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
      /**
       * Updates the trash structure to remove any deleted groups or applications after
       * an empty is performed.
       */
      if (
        this.selectedApplication !== null &&
        this.selectedApplication.trashed
      ) {
        this.removeSelectedAppFromSidebar()
      } else if (this.selectedGroup.trashed) {
        this.removeSelectedGroupFromSidebar()
      } else if (this.selectedApplication === null) {
        // The group was emptied, it might have contained trashed applications hence
        // we need to search through the trash and remove any now deleted applications.
        for (const app of this.selectedGroup.applications.slice()) {
          const index = this.trashContents.findIndex((item) => {
            return (
              item.trash_item_id === app.id &&
              item.trash_item_type === 'application'
            )
          })
          if (index !== -1) {
            this.selectedGroup.applications.splice(index, 1)
          }
        }
      }
    },
  },
}
</script>
