<template>
  <div class="user-admin-rows__cell-group">
    <div ref="groups_container" class="user-admin-rows__cell-group-container">
      <span
        v-for="group in groups"
        ref="groups"
        :key="'admin-row-group' + userId + '-' + group.id"
        class="user-admin-rows__cell-group-item"
      >
        {{ group.name }}
        <i
          v-if="group.permissions == 'ADMIN'"
          class="user-admin-rows__cell-group-icon fas fa-users-cog"
        ></i>
      </span>
    </div>
    <a
      v-show="overflowing"
      ref="contextLink"
      class="user-admin-rows__cell-group-plus"
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
          class="user-admin-rows__cell-group-hidden-item"
        >
          {{ group.name }}
          <i
            v-if="group.permissions == 'ADMIN'"
            class="user-admin-rows__cell-group-icon fas fa-users-cog"
          ></i>
        </li>
      </ul>
    </Context>
  </div>
</template>
<script>
export default {
  name: 'UserGroupsField',
  props: {
    groups: {
      required: true,
      type: Array,
    },
    userId: {
      required: true,
      type: Number,
    },
    parentWidth: {
      required: true,
      type: Number,
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
  },
  watch: {
    parentWidth() {
      this.updatedOverflow()
    },
  },
  created() {
    this.updatedOverflow()
  },
  methods: {
    updatedOverflow() {
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
