<template>
  <div class="user-admin-group" v-on="$listeners">
    <div ref="groupsContainer" class="user-admin-group__container">
      <span ref="empty" class="user-admin-group__empty-item"></span>
      <span
        v-for="(group, index) in groups"
        ref="groups"
        :key="'admin-row-group' + userId + '-' + group.id"
        class="user-admin-group__item"
        :style="{
          order: index,
        }"
      >
        {{ group.name }}
        <i
          v-if="group.permissions == 'ADMIN'"
          v-tooltip="'is group admin'"
          class="user-admin-group__icon fas fa-users-cog"
        ></i>
      </span>
      <a
        v-show="overflowing"
        ref="expandButton"
        class="user-admin-group__expand"
        :style="{
          order: expandOrder,
        }"
        @click.prevent="showContext"
        >+{{ numHiddenGroups }}</a
      >
    </div>
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
      expandOrder: -1,
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
        target: event.currentTarget,
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
        // We calculate how much space is left on the first visible row as we go
        let firstRowSpaceRemaining = this.$refs.groupsContainer.clientWidth
        // Then we dynamically change the order of the expand button to slot it into
        // the correct place depending on if groups are hidden or not.
        let expandOrder = 0
        for (let i = 0; i < this.$refs.groups.length; i++) {
          const groupEl = this.$refs.groups[i]
          const groupTop = groupEl.getBoundingClientRect().top
          if (groupTop > emptyElementTop) {
            // A groupEl element has been flex-wrapped down into a new row due to no
            // space. Every group after this one must also be hidden hence we now have
            // calculated the number of hidden groups.
            const expandButtonWidth = this.$refs.expandButton.scrollWidth

            const wrappingErrorMargin = 15
            if (
              firstRowSpaceRemaining - groupEl.scrollWidth >
                wrappingErrorMargin &&
              numHiddenGroups === 1
            ) {
              // However first check, if this group which has been wrapped down would
              // fit on the first row (with some room for error) if the expand button
              // was not also on the first row. If that is so AND there is only one
              // hidden group we can safely hide the expand button and let the
              // group wrap back into fitting on the first row.
              expandOrder = i
              numHiddenGroups--
            } else if (
              firstRowSpaceRemaining >
              expandButtonWidth + wrappingErrorMargin
            ) {
              // We need to show the expand button and there is room for it on the first
              // row so we can put it after the last visible group on the first row.
              expandOrder = i - 1
            } else {
              // There is no room on the first row for the expand button, so we put it
              // before the last group on the first row which will cause that group
              // to wrap down and no longer be visible.
              expandOrder = i - 2
              numHiddenGroups++
            }
            break
          } else {
            expandOrder = i
            firstRowSpaceRemaining -= groupEl.scrollWidth
            numHiddenGroups--
          }
        }
        this.expandOrder = expandOrder
        this.numHiddenGroups = numHiddenGroups
        this.overflowing = numHiddenGroups !== 0
      })
    },
  },
}
</script>
