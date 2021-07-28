<template>
  <div>
    <div v-if="left" class="comment">
      <div class="comment__top">
        <div class="comment__initials">
          {{ comment.first_name | nameAbbreviation }}
        </div>
        <div class="comment__content">
          <div class="comment__name">
            {{ comment.first_name }}
          </div>
          <div class="comment__commented-at-display">{{ timeAgo }}</div>
        </div>
      </div>
      <div class="comment__body">
        {{ comment.comment }}
      </div>
    </div>
    <div v-else class="comment">
      <div class="comment__top">
        <div class="comment__content">
          <div class="comment__name comment--right">
            {{ comment.first_name }}
          </div>
          <div class="comment__commented-at-display comment--right">
            {{ timeAgo }}
          </div>
        </div>
        <div class="comment__initials">
          {{ comment.first_name | nameAbbreviation }}
        </div>
      </div>
      <div class="comment__body comment--right">
        {{ comment.comment }}
      </div>
    </div>
  </div>
</template>

<script>
import moment from 'moment'

export default {
  name: 'Comment',
  props: {
    comment: {
      type: Object,
      required: true,
    },
    left: {
      type: Boolean,
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
