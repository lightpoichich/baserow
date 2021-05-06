<template>
  <Context v-if="showGroupsEvent">
    <ul class="context__menu">
      <li
        v-for="group in showGroupsEvent.hiddenGroups"
        :key="'hidden-admin-row-group' + group.id"
        class="user-admin-group__dropdown-item"
      >
        {{ group.name }}
        <i
          v-if="group.permissions == 'ADMIN'"
          v-tooltip="'is group admin'"
          class="user-admin-group__icon fas fa-users-cog"
        ></i>
      </li>
    </ul>
  </Context>
</template>

<script>
import context from '@baserow/modules/core/mixins/context'

export default {
  name: 'HiddenGroupsContext',
  mixins: [context],
  props: {
    showGroupsEvent: {
      required: true,
      validator: (prop) => typeof prop === 'object' || prop === null,
    },
  },
  watch: {
    showGroupsEvent(showGroupsEvent) {
      if (showGroupsEvent) {
        this.$nextTick(function () {
          this.hide()
          this.show(showGroupsEvent.target, 'bottom', 'left', 4)
        })
      }
    },
  },
}
</script>
