<template>
  <div class="user-admin-group">
    <div class="user-admin-group__container">
      <span ref="empty" class="user-admin-group__empty-item"></span>
      <span
        v-for="group in groups"
        ref="groups"
        :key="'admin-row-group' + userId + '-' + group.id"
        class="user-admin-group__item"
      >
        {{ group.name }}
        <i
          v-if="group.permissions == 'ADMIN'"
          v-tooltip="'is group admin'"
          class="user-admin-group__icon fas fa-users-cog"
        ></i>
      </span>
    </div>
    <a
      v-show="overflowing"
      class="user-admin-group__expand"
      @click.prevent="showContext"
      >+{{ numHiddenGroups }}</a
    >
  </div>
</template>
<script>
import ResizeObserver from 'resize-observer-polyfill'

/**
 * Displays a list of a users groups with a modal displaying any groups that do not fit.
 * Adds an icon showing if the user is an admin of the group.
 */
export default {
  name: 'UserGroupsField',
  props: {
    row: {
      required: true,
      type: Object,
    },
    column: {
      required: true,
      type: Object,
    },
  },
  data() {
    return {
      overflowing: false,
      numHiddenGroups: 0,
      renderContext: false,
    }
  },
  computed: {
    hiddenGroups() {
      return this.groups.slice(this.groups.length - this.numHiddenGroups)
    },
    groups() {
      return this.row[this.column.key]
    },
    userId() {
      return this.row.id
    },
  },
  mounted() {
    this.$el.resizeObserver = new ResizeObserver(this.recalculateHiddenGroups)
    this.$el.resizeObserver.observe(this.$el)
  },
  beforeDestroy() {
    this.$el.resizeObserver.unobserve(this.$el)
  },
  created() {
    this.recalculateHiddenGroups()
  },
  methods: {
    showContext(event) {
      this.$emit('show-group', {
        hiddenGroups: this.hiddenGroups,
        contextLink: event.target,
        time: Date.now(),
      })
    },
    /**
     * Calculates how many groups fit into the groups cell, if any are overflowing and
     * do not fit we add a + button to display a context menu showing these hidden
     * groups.
     */
    recalculateHiddenGroups() {
      if (process.server) {
        return
      }
      this.$nextTick(() => {
        let numHiddenGroups = this.groups.length
        // The starting empty element never flex-wraps down into a new row. So if
        // a group after it has the same top value then it must not have wrapped down
        // and hence must fit and be visible.
        const emptyElementTop = this.$refs.empty.getBoundingClientRect().top
        for (let i = 0; i < this.$refs.groups.length; i++) {
          const groupEl = this.$refs.groups[i]
          const groupTop = groupEl.getBoundingClientRect().top
          if (groupTop > emptyElementTop) {
            // A groupEl element has been flex-wrapped down into a new row due to no
            // space. Every group after this one must also be hidden hence we now have
            // calculated the number of hidden groups.
            break
          } else {
            numHiddenGroups--
          }
        }
        this.numHiddenGroups = numHiddenGroups
        this.overflowing = numHiddenGroups !== 0
      })
    },
  },
}
</script>
