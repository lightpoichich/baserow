<template>
  <div>
    <div class="box__title trash-box-title">
      <h2 class="trash-box-title__header">{{ title }}</h2>
      <div class="trash-sub-header">
        <h3 class="trash-sub-header__title">
          Restore deleted items from the past {{ trashDuration }}
        </h3>
        <a
          v-show="totalServerSideTrashContentsCount > 0"
          class="button button--error"
          :disabled="loadingContents"
          @click="showEmptyModalIfNotLoading"
          >{{ emptyButtonText }}</a
        >
      </div>
    </div>
    <div v-if="loadingContents" class="loading-overlay"></div>
    <div
      v-if="totalServerSideTrashContentsCount === 0"
      class="trash-empty-contents"
    >
      <i class="trash-empty-contents__icon fas fa-recycle"></i>
      <span class="trash-empty-contents__text"
        >Nothing has been deleted in the past three days.</span
      >
    </div>
    <div v-else>
      <InfiniteScroll
        :max-count="totalServerSideTrashContentsCount"
        :items="trashContents"
        @load-next-page="$emit('load-next-page', $event)"
      >
        <template #default="item">
          <TrashEntry
            :key="'trash-item-' + item.id"
            :trash-entry="item"
            :disabled="loadingContents || shouldTrashEntryBeDisabled(item)"
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
      :selected-is-trashed="selectedItem.trashed"
      @empty="$emit('empty')"
    ></TrashEmptyModal>
  </div>
</template>

<script>
/**
 * Displays a infinite scrolling list of trash contents for either a selectedGroup or
 * a specific selectedApplication in the selectedGroup. The user can empty the trash
 * contents permanently deleting them all, or restore individual trashed items.
 *
 * If the selectedItem (the selectedApplication if provided, otherwise the selectedGroup
 * ) is trashed itself then the modal will display buttons and modals which indicate
 * that they will permanently delete the selectedItem instead of just emptying it's
 * contents.
 */

import moment from 'moment'
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
    totalServerSideTrashContentsCount: {
      type: Number,
      required: true,
    },
  },
  computed: {
    selectedItem() {
      return this.selectedApplication === null
        ? this.selectedGroup
        : this.selectedApplication
    },
    selectedItemType() {
      return this.selectedApplication === null ? 'Group' : 'Application'
    },
    title() {
      const title = this.selectedItem.name
      return title === ''
        ? `Unnamed ${this.selectedItemType} ${this.selectedItem.id}`
        : title
    },
    emptyButtonText() {
      if (this.selectedItem.trashed) {
        return `Delete ${this.selectedItemType} permanently`
      } else {
        return `Empty this ${this.selectedItemType}'s trash`
      }
    },
    trashDuration() {
      const hours = this.$env.HOURS_UNTIL_TRASH_PERMANENTLY_DELETED
      return moment().subtract(hours, 'hours').fromNow().replace('ago', '')
    },
  },
  methods: {
    showEmptyModalIfNotLoading() {
      if (!this.loadingContents) {
        this.$refs.emptyModal.show()
      }
    },
    shouldTrashEntryBeDisabled(entry) {
      const selectedItemType = this.selectedItemType.toLowerCase()
      const entryIsForSelectedItem =
        entry.trash_item_id === this.selectedItem.id &&
        entry.trash_item_type === selectedItemType
      return this.selectedItem.trashed && !entryIsForSelectedItem
    },
  },
}
</script>
