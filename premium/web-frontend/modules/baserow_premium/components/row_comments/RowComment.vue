<template>
  <div
    :class="{ 'row-comments__comment--right': comment.own_comment }"
    class="row-comments__comment"
  >
    <div class="row-comments__comment-head">
      <div class="row-comments__comment-head-initial">
        {{ comment.first_name | nameAbbreviation }}
      </div>
      <div class="row-comments__comment-head-details">
        <div class="row-comments__comment-head-name">
          {{ comment.own_comment ? 'You' : comment.first_name }}
        </div>
        <div class="row-comments__comment-head-time">{{ timeAgo }}</div>
      </div>
    </div>
    <div class="row-comments__comment-text">{{ comment.comment }}</div>
  </div>
</template>

<script>
import moment from 'moment'

export default {
  name: 'RowComment',
  props: {
    comment: {
      type: Object,
      required: true,
    },
  },
  computed: {
    timeAgo() {
      return moment.utc(this.comment.created_at).fromNow()
    },
  },
}
</script>
