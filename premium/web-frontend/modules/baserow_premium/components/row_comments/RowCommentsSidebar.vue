<template>
  <div>
    <div v-if="!loaded && loading" class="loading-absolute-center" />
    <div v-else>
      <div class="row-comments">
        <div ref="rowCommentsBody" class="row-comments__body">
          <InfiniteScroll
            :current-count="currentCount"
            :max-count="totalCount"
            :loading="loading"
            :reverse="true"
            @load-next-page="nextPage"
          >
            <div v-if="loaded && loading" class="row-comments__loading">
              <div class="loading" />
            </div>
            <RowComment v-for="c in comments" :key="c.id" :comment="c" />
          </InfiniteScroll>
        </div>
        <div class="row-comments__foot">
          <textarea
            v-model="comment"
            class="input row-comments__foot-input"
            @keydown.enter.exact.prevent="postComment"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'
import { notifyIf } from '@baserow/modules/core/utils/error'
import RowComment from '@baserow_premium/components/row_comments/RowComment'
import InfiniteScroll from '@baserow/modules/core/components/infinite_scroll/InfiniteScroll'

export default {
  name: 'RowCommentsSidebar',
  components: { InfiniteScroll, RowComment },
  props: {
    table: {
      required: true,
      type: Object,
    },
    row: {
      required: true,
      type: Object,
    },
  },
  data() {
    return {
      comment: '',
    }
  },
  computed: {
    ...mapGetters({
      comments: 'row_comments/getRowComments',
      loading: 'row_comments/getLoading',
      loaded: 'row_comments/getLoaded',
      currentCount: 'row_comments/getCurrentCount',
      totalCount: 'row_comments/getTotalCount',
    }),
  },
  async created() {
    try {
      const tableId = this.table.id
      const rowId = this.row.id
      await this.$store.dispatch('row_comments/fetchRowComments', {
        tableId,
        rowId,
      })
    } catch (e) {
      notifyIf(e, 'application')
    }
  },
  methods: {
    async postComment() {
      if (!this.comment.trim()) {
        return
      }
      try {
        const tableId = this.table.id
        const rowId = this.row.id
        const comment = this.comment
        await this.$store.dispatch('row_comments/postComment', {
          tableId,
          rowId,
          comment,
        })
        this.comment = ''
      } catch (e) {
        notifyIf(e, 'application')
      }
    },
    async nextPage(page) {
      try {
        const tableId = this.table.id
        const rowId = this.row.id
        await this.$store.dispatch('row_comments/fetchPage', {
          tableId,
          rowId,
          page,
        })
      } catch (e) {
        notifyIf(e, 'application')
      }
    },
  },
}
</script>
