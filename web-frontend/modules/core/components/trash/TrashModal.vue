<template>
  <Modal :sidebar="true">
    <template #sidebar>
      <div v-if="loading" class="loading-absolute-center"></div>
      <TrashSidebar
        v-else
        :groups="groups"
        :selected-group="selectedGroup"
        :selected-application="selectedApplication"
        @selected="selectGroupAndApp"
      >
        <a class="modal__close" @click="hide()">
          <i class="fas fa-times"></i>
        </a>
      </TrashSidebar>
    </template>
    <template #content>
      <div v-if="loading" class="loading-absolute-center"></div>
      <TrashContent
        v-else
        :selected-group="selectedGroup"
        :selected-application="selectedApplication"
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

export default {
  name: 'TrashModal',
  components: { TrashSidebar, TrashContent },
  mixins: [modal],
  props: {},
  data() {
    return {
      loading: true,
      groups: [],
      selectedGroup: null,
      selectedApplication: null,
    }
  },
  methods: {
    async show(...args) {
      modal.methods.show.call(this, ...args)

      this.loading = true
      this.groups = []
      this.selectedGroup = null
      this.selectedApplication = null

      try {
        const { data } = await TrashService(this.$client).fetchStructure()
        this.groups = data.groups
        this.selectedGroup = this.groups[0]
        this.loading = false
      } catch (error) {
        notifyIf(error, 'trash')
        this.hide()
      }
    },
    selectGroupAndApp({ group, application }) {
      this.selectedGroup = group
      this.selectedApplication = application
    },
  },
}
</script>
