<template>
  <div>
    <div v-if="!loaded && loading" class="loading-absolute-center" />
    <div v-else>
      <div class="row-comments">
        <div class="row-comments__body">
          <InfiniteScroll
            ref="infiniteScroll"
            :current-count="currentCount"
            :max-count="totalCount"
            :loading="loading"
            :reverse="true"
            @load-next-page="nextPage"
          >
            <RowComment
              v-for="c in comments"
              :key="'row-comment-' + c.id"
              :comment="c"
            />
          </InfiniteScroll>
        </div>
        <div class="row-comments__foot">
          <div
            class="row-comments__foot-fake-textarea"
            :class="{
              'row-comments__foot-input--loading-overlay': postingComment,
            }"
          >
            <div
              v-if="postingComment"
              class="row-comments__foot-input--loading"
            ></div>
            <textarea
              ref="inputTextArea"
              v-model="comment"
              class="input row-comments__foot-input"
              :style="{
                height: textBoxSize + 'px',
                overflow: textBoxOverflow,
              }"
              rows="1"
              @keydown.enter.exact.prevent="postComment"
              @change="resizeTextArea"
              @cut="resizeTextArea"
              @drop="resizeTextArea"
              @keydown="resizeTextArea"
            />
          </div>
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
      numTextAreaLines: 1,
    }
  },
  computed: {
    ...mapGetters({
      comments: 'row_comments/getRowComments',
      loading: 'row_comments/getLoading',
      postingComment: 'row_comments/getPostingComment',
      loaded: 'row_comments/getLoaded',
      currentCount: 'row_comments/getCurrentCount',
      totalCount: 'row_comments/getTotalCount',
    }),
    textBoxSize() {
      return 22 * Math.min(this.numTextAreaLines, 4)
    },
    textBoxOverflow() {
      return this.numTextAreaLines > 4 ? 'auto' : 'hidden'
    },
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
      if (!this.comment.trim() || this.postingComment) {
        return
      }
      try {
        const tableId = this.table.id
        const rowId = this.row.id
        const comment = this.comment.trim()
        await this.$store.dispatch('row_comments/postComment', {
          tableId,
          rowId,
          comment,
        })
        this.comment = ''
        this.resizeTextArea()
        this.$refs.infiniteScroll.scrollToStart()
      } catch (e) {
        notifyIf(e, 'application')
      }
    },
    async nextPage() {
      try {
        const tableId = this.table.id
        const rowId = this.row.id
        await this.$store.dispatch('row_comments/fetchNextSetOfComments', {
          tableId,
          rowId,
        })
      } catch (e) {
        notifyIf(e, 'application')
      }
    },
    resizeTextArea() {
      this.$nextTick(() => {
        const inputTextArea = this.$refs.inputTextArea
        this.numTextAreaLines = this.calculateHeight(inputTextArea)
      })
    },
    /**
     * Taken from https://stackoverflow.com/questions/1760629/how-to-get-number-of-rows-in-textarea-using-javascript/1761203#1761203
     *
     * The key reason we need this is to resize a fully expanded textarea to something
     * smaller as a user deletes newlines or text. Hence we need to actually manipulate
     * the dom and lower the height of the textarea until we find overflow is occurring
     * again to re-find the correct min height.
     */
    calculateContentHeight(ta, scanAmount) {
      const origHeight = ta.style.height
      let height = ta.offsetHeight
      const scrollHeight = ta.scrollHeight
      const overflow = ta.style.overflow
      /// only bother if the ta is bigger than content
      if (height >= scrollHeight) {
        /// check that our browser supports changing dimension
        /// calculations mid-way through a function call...
        ta.style.height = height + scanAmount + 'px'
        /// because the scrollbar can cause calculation problems
        ta.style.overflow = 'hidden'
        /// by checking that scrollHeight has updated
        if (scrollHeight < ta.scrollHeight) {
          /// now try and scan the ta's height downwards
          /// until scrollHeight becomes larger than height
          while (ta.offsetHeight >= ta.scrollHeight) {
            ta.style.height = (height -= scanAmount) + 'px'
          }
          /// be more specific to get the exact height
          while (ta.offsetHeight < ta.scrollHeight) {
            ta.style.height = height++ + 'px'
          }
          height--
          /// reset the ta back to it's original height
          ta.style.height = origHeight
          /// put the overflow back
          ta.style.overflow = overflow
          return height
        }
      } else {
        return scrollHeight
      }
    },
    calculateHeight(ta) {
      const style = window.getComputedStyle
        ? window.getComputedStyle(ta)
        : ta.currentStyle

      // This will get the line-height only if it is set in the css,
      // otherwise it's "normal"
      const taLineHeight = parseInt(style.lineHeight, 10)
      // Get the scroll height of the textarea
      const taHeight = this.calculateContentHeight(ta, taLineHeight)
      // calculate the number of lines
      return Math.ceil(taHeight / taLineHeight)
    },
  },
}
</script>
