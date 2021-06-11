<template>
  <Context ref="context">
    <div class="context__menu-title">{{ group.name }} ({{ group.id }})</div>
    <ul class="context__menu">
      <li>
        <a @click="$emit('rename')">
          <i class="context__menu-icon fas fa-fw fa-pen"></i>
          Rename group
        </a>
      </li>
      <li>
        <a @click=";[$refs.groupMembersModal.show(), hide()]">
          <i class="context__menu-icon fas fa-fw fa-users"></i>
          Members
        </a>
      </li>
      <li :class="{ 'context__menu-item--loading': loading }">
        <a @click="deleteGroup">
          <i class="context__menu-icon fas fa-fw fa-trash"></i>
          Delete group
        </a>
      </li>
    </ul>
    <GroupMembersModal
      ref="groupMembersModal"
      :group="group"
    ></GroupMembersModal>
  </Context>
</template>

<script>
import GroupMembersModal from '@baserow/modules/core/components/group/GroupMembersModal'
import context from '@baserow/modules/core/mixins/context'
import { notifyIf } from '@baserow/modules/core/utils/error'

export default {
  name: 'GroupContext',
  components: { GroupMembersModal },
  mixins: [context],
  props: {
    group: {
      type: Object,
      required: true,
    },
  },
  data() {
    return {
      loading: false,
    }
  },
  methods: {
    showGroupMembersModal() {
      this.$refs.groupMembersModal.show()
    },
    async deleteGroup() {
      this.loading = true

      try {
        await this.$store.dispatch('group/delete', this.group)
        await this.$store.dispatch('notification/undoDelete', {
          trashItemType: 'group',
          trashItemId: this.group.id,
        })
        this.hide()
      } catch (error) {
        notifyIf(error, 'application')
      }

      this.loading = false
    },
  },
}
</script>
