<template>
  <div>
    <div class="box__title trash-box-title">
      <h2 class="trash-box-title__header">{{ title }}</h2>
      <div class="trash-sub-header">
        <h3 class="trash-sub-header__title">
          Restore deleted items from the past three days
        </h3>
        <a
          v-show="entryCount > 0"
          class="button button--error"
          :disabled="loadingContents"
          @click="showEmptyModalIfNotLoading"
          >{{ emptyButtonText }}</a
        >
      </div>
    </div>
    <div v-if="loadingContents" class="loading-overlay"></div>
    <div v-if="entryCount === 0" class="trash-empty-contents">
      <i class="trash-empty-contents__icon fas fa-recycle"></i>
      <span class="trash-empty-contents__text"
        >Nothing has been deleted in the past three days.</span
      >
    </div>
    <div v-else>
      <InfiniteScroll
        :max-count="entryCount"
        :items="trashContents"
        @load-next-page="$emit('load-next-page', $event)"
      >
        <template #default="item">
          <TrashEntry
            :key="'trash-item-' + item.id"
            :trash-entry="item"
            :disabled="loadingContents || isParentItemTrashed(item)"
            @restore="$emit('restore', $event)"
          >
          </TrashEntry>
        </template>
      </InfiniteScroll>
      <div v-if="loadingNextPage" class="trash-contents__loading-box">
        <div class="loading"></div>
      </div>
    </div>
    <TrashEmptyModal
      ref="emptyModal"
      :name="title"
      :loading="loadingContents"
      :is-empty-or-perm-delete="isEmptying"
      @empty="$emit('empty')"
    ></TrashEmptyModal>
  </div>
</template>

<script>
import TrashEntry from '@baserow/modules/core/components/trash/TrashEntry'
import InfiniteScroll from '@baserow/modules/core/components/infinite_scroll/InfiniteScroll'
import TrashEmptyModal from '@baserow/modules/core/components/trash/TrashEmptyModal'
export default {
  name: 'TrashContents',
  components: { InfiniteScroll, TrashEntry, TrashEmptyModal },
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
    loadingNextPage: {
      type: Boolean,
      required: true,
    },
    entryCount: {
      type: Number,
      required: true,
    },
  },
  computed: {
    title() {
      const title =
        this.selectedApplication === null
          ? this.selectedGroup.name
          : this.selectedApplication.name
      const groupOrApp =
        this.selectedApplication === null ? 'Group' : 'Application'
      const id =
        this.selectedApplication === null
          ? this.selectedGroup.id
          : this.selectedApplication.id
      return title === '' ? 'Unnamed ' + groupOrApp + ' ' + id : title
    },
    isEmptying() {
      if (this.selectedApplication !== null) {
        return !this.selectedApplication.trashed
      } else {
        return !this.selectedGroup.trashed
      }
    },
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
    selfIsTrashed() {
      return this.selectedApplication === null
        ? this.selectedGroup.trashed
        : this.selectedApplication.trashed
    },
    selfTrashItemId() {
      return this.selectedApplication === null
        ? this.selectedGroup.id
        : this.selectedApplication.id
    },
  },
  methods: {
    showEmptyModalIfNotLoading() {
      if (!this.loadingContents) {
        this.$refs.emptyModal.show()
      }
    },
    isParentItemTrashed(item) {
      const parentType =
        this.selectedApplication === null ? 'group' : 'application'
      const parentId = item.parent_trash_item_id
      let parentIsTrashed = false
      if (parentId !== null) {
        const index = this.trashContents.findIndex(
          (i) => i.trash_item_id === parentId
        )
        parentIsTrashed = index !== -1
      }
      return (
        (this.selfIsTrashed &&
          !(
            item.trash_item_id === this.selfTrashItemId &&
            item.trash_item_type === parentType
          )) ||
        parentIsTrashed
      )
    },
  },
}
</script>
