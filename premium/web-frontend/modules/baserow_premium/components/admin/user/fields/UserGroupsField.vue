<template>
  <div class="user-admin-group">
    <div ref="groups_container" class="user-admin-group__container">
      <span
        v-for="group in groups"
        ref="groups"
        :key="'admin-row-group' + userId + '-' + group.id"
        class="user-admin-group__item"
      >
        {{ group.name }}
        <i
          v-if="group.permissions == 'ADMIN'"
          class="user-admin-group__icon fas fa-users-cog"
        ></i>
      </span>
    </div>
    <a
      v-show="overflowing"
      class="user-admin-group__expand"
      @click.prevent="showContext"
      >+{{ numHidden }}</a
    >
  </div>
</template>
<script>
import ResizeObserver from 'resize-observer-polyfill'
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
      numHidden: 0,
      renderContext: false,
    }
  },
  computed: {
    hiddenGroups() {
      return this.groups.slice(this.groups.length - this.numHidden)
    },
    groups() {
      return this.row[this.column.key]
    },
    userId() {
      return this.row.id
    },
  },
  mounted() {
    this.$el.resizeObserver = new ResizeObserver(this.updatedOverflow)
    this.$el.resizeObserver.observe(this.$el)
  },
  beforeDestroy() {
    this.$el.resizeObserver.unobserve(this.$el)
  },
  created() {
    this.updatedOverflow()
  },
  methods: {
    showContext(event) {
      this.$emit('show-group', {
        hiddenGroups: this.hiddenGroups,
        contextLink: event.target,
        time: Date.now(),
      })
    },
    updatedOverflow() {
      if (process.server) {
        return
      }
      this.$nextTick(() => {
        const container = this.$refs.groups_container
        let numHiddenGroups = this.groups.length
        let visibleWidthUsedUp = 0
        for (let i = 0; i < this.$refs.groups.length; i++) {
          const group = this.$refs.groups[i]
          if (visibleWidthUsedUp + group.scrollWidth < container.clientWidth) {
            numHiddenGroups--
            visibleWidthUsedUp += group.scrollWidth
          } else {
            break
          }
        }
        this.numHidden = numHiddenGroups
        this.overflowing = numHiddenGroups !== 0
      })
    },
  },
}
</script>
