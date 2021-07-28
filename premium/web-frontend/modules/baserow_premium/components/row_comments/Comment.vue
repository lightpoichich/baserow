<template>
  <div>
    <div :class="{ 'comment--right': ownComment }" class="comment">
      <div :class="{ 'comment--right': ownComment }" class="comment__top">
        <div
          v-if="!ownComment"
          :class="{ 'comment--right': ownComment }"
          class="comment__initials"
        >
          {{ comment.first_name | nameAbbreviation }}
        </div>
        <div :class="{ 'comment--right': ownComment }" class="comment__content">
          <strong v-if="!ownComment" class="comment__name">
            {{ comment.first_name }}
          </strong>
          <strong v-else class="comment__name">You</strong>
          <div class="comment__commented-at-display">{{ timeAgo }}</div>
        </div>
        <div v-if="ownComment" class="comment__initials">
          {{ comment.first_name | nameAbbreviation }}
        </div>
      </div>
      <div :class="{ 'comment--right': ownComment }" class="comment__body">
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
    ownComment: {
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
