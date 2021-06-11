<template>
  <div
    ref="member"
    class="trash-entry"
    :class="{ 'trash-entry--highlight': highlighted }"
  >
    <div class="trash-entry__initials">
      {{ trashEntry.user_who_trashed | nameAbbreviation }}
    </div>
    <div class="trash-entry__content">
      <div class="trash-entry__name">
        {{ trashEntry.user_who_trashed }} Deleted
        <strong>{{ trashEntry.name }}</strong>
        {{ trashEntry.parent_name ? ' from ' + trashEntry.parent_name : '' }}
      </div>
      <div class="trash-entry__description">{{ timeAgo }}</div>
    </div>
    <div class="trash-entry__actions">
      <a
        v-if="!disabled"
        class="trash-entry__action"
        :class="{ 'trash-entry__action--loading': trashEntry.loading }"
        @click="$emit('restore', trashEntry)"
      >
        {{ trashEntry.loading ? '' : 'Restore' }}
      </a>
    </div>
  </div>
</template>

<script>
import moment from 'moment'

export default {
  name: 'TrashEntry',
  props: {
    trashEntry: {
      type: Object,
      required: true,
    },
    disabled: {
      type: Boolean,
      required: false,
      default: false,
    },
  },
  data() {
    return {
      highlighted: false,
    }
  },
  computed: {
    timeAgo() {
      return moment.utc(this.trashEntry.trashed_at).fromNow()
    },
  },
  methods: {
    highlight() {
      this.$refs.member.scrollIntoView({ behavior: 'smooth' })
      this.highlighted = true
      setTimeout(() => {
        this.highlighted = false
      }, 2000)
    },
  },
}
</script>
