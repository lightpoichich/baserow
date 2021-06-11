<template>
  <div>
    <div class="box__title trash-box-title">
      <h2 class="trash-box-title__header">
        {{
          selectedApplication === null
            ? selectedGroup.name
            : selectedApplication.name
        }}
      </h2>
      <div class="trash-sub-header">
        <h3 class="trash-sub-header__title">
          Restore deleted items from the past three days
        </h3>
        <a
          class="button button--error"
          :disabled="loadingContents"
          @click="$emit('empty')"
          >{{ emptyButtonText }}</a
        >
      </div>
    </div>
    <div v-if="loadingContents" class="loading-overlay"></div>
    <div v-else>
      <TrashEntry
        v-for="trashEntry in trashContents"
        :key="'trash-item-' + trashEntry.id"
        :trash-entry="trashEntry"
        :disabled="loadingContents"
        @restore="$emit('restore', $event)"
      >
      </TrashEntry>
    </div>
  </div>
</template>

<script>
import TrashEntry from '@baserow/modules/core/components/trash/TrashEntry'
export default {
  name: 'TrashContents',
  components: { TrashEntry },
  mixins: [],
  props: {
    selectedGroup: {
      type: Object,
      required: true,
    },
    selectedApplication: {
      type: Object,
      required: false,
      default: null,
    },
    trashContents: {
      type: Array,
      required: true,
    },
    loadingContents: {
      type: Boolean,
      required: true,
    },
  },
  computed: {
    emptyButtonText() {
      if (this.selectedApplication === null) {
        if (this.selectedGroup.trashed) {
          return 'Delete group permanently'
        } else {
          return "Empty this group's trash"
        }
      } else if (this.selectedApplication.trashed) {
        return 'Delete application permanently'
      } else {
        return "Empty this application's trash"
      }
    },
  },
}
</script>
