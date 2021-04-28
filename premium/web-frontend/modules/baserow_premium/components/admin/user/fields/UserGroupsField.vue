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
      ref="contextLink"
      class="user-admin-group__expand"
      @click.prevent="
        $refs.context.toggle($refs.contextLink, 'bottom', 'left', 4)
      "
      >+{{ numHidden }}</a
    >
    <Context ref="context">
      <ul class="context__menu">
        <li
          v-for="group in hiddenGroups"
          :key="'hidden-admin-row-group' + userId + '-' + group.id"
          class="user-admin-group__dropdown-item"
        >
          {{ group.name }}
          <i
            v-if="group.permissions == 'ADMIN'"
            class="user-admin-group__icon fas fa-users-cog"
          ></i>
        </li>
      </ul>
    </Context>
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
    updatedOverflow() {
      if (process.server) {
        return
      }
      this.$nextTick(() => {
        const container = this.$refs.groups_container
        this.overflowing =
          container.clientWidth < container.scrollWidth ||
          container.clientHeight < container.scrollHeight
        if (this.overflowing) {
          let numHiddenGroups = this.groups.length
          let visibleWidthUsedUp = 0
          this.$refs.groups.forEach((group) => {
            if (
              visibleWidthUsedUp + group.scrollWidth <
              container.clientWidth
            ) {
              numHiddenGroups--
              visibleWidthUsedUp += group.scrollWidth
            } else {
              this.numHidden = numHiddenGroups
            }
          })
        } else {
          this.numHidden = 0
        }
      })
    },
  },
}
</script>
