<template>
  <div>
    <Error :error="error"></Error>
    <div v-if="loading">Loading</div>
    <div v-else>
      <Comment
        v-for="c in comments"
        :key="c.id"
        :comment="c"
        :left="c.user === userId"
      ></Comment>
      <input v-model="comment" type="text" />
      <a href="#" @click.prevent="postComment">Add comment</a>
    </div>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'
import error from '@baserow/modules/core/mixins/error'
import Comment from '@baserow_premium/components/row_comments/Comment'

export default {
  name: 'RowCommentsSideBar',
  components: { Comment },
  mixins: [error],
  props: {
    tableId: {
      required: true,
      type: Number,
    },
    rowId: {
      required: true,
      type: Number,
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
      const tableId = this.tableId
      const rowId = this.rowId
      await this.$store.dispatch('row_comments/fetchRowComments', {
        tableId,
        rowId,
      })
    } catch (e) {
      this.handleError(e, 'application')
    }
  },
  methods: {
    async postComment() {
      if (!this.comment) {
        return
      }
      try {
        const tableId = this.tableId
        const rowId = this.rowId
        const comment = this.comment
        await this.$store.dispatch('row_comments/postComment', {
          tableId,
          rowId,
          comment,
        })
        this.comment = ''
      } catch (e) {
        this.handleError(e, 'application')
      }
    },
  },
}
</script>
