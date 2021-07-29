<template>
  <div>
    <div v-if="!loaded && loading" class="loading-absolute-center"></div>
    <div v-else>
      <div class="row-comments">
        <div class="row-comments__body">
          <div class="row-comments__loading">
            <div class="loading"></div>
          </div>
          <RowComment
            v-for="c in comments"
            :key="c.id"
            :comment="c"
          ></RowComment>
        </div>
        <div class="row-comments__foot">
          <textarea
            v-model="comment"
            class="input row-comments__foot-input"
            @keydown.enter="postComment"
          ></textarea>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'
import { notifyIf } from '@baserow/modules/core/utils/error'
import RowComment from '@baserow_premium/components/row_comments/RowComment'

export default {
  name: 'RowCommentsSidebar',
  components: { RowComment },
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
      userId: 'auth/getUserId',
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
      if (!this.comment) {
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
  },
}
</script>
