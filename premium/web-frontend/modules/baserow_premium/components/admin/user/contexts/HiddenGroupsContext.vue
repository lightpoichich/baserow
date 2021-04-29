<template>
  <Context v-if="selectedGroup">
    <ul class="context__menu">
      <li
        v-for="group in selectedGroup.hiddenGroups"
        :key="'hidden-admin-row-group' + group.id"
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
</template>

<script>
import context from '@baserow/modules/core/mixins/context'

export default {
  name: 'HiddenGroupsContext',
  mixins: [context],
  props: {
    selectedGroup: {
      required: true,
      validator: (prop) => typeof prop === 'object' || prop === null,
    },
  },
  watch: {
    selectedGroup(selectedGroup) {
      if (selectedGroup) {
        this.$nextTick(function () {
          this.hide()
          this.show(selectedGroup.contextLink, 'bottom', 'left', 4)
        })
      }
    },
  },
}
</script>
