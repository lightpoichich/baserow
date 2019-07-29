<template>
  <Context ref="groupContext" class="select">
    <div class="select-search">
      <i class="select-search-icon fas fa-search"></i>
      <input
        type="text"
        class="select-search-input"
        placeholder="Search views"
      />
    </div>
    <div v-if="isLoading" class="context-loading">
      <div class="loading"></div>
    </div>
    <ul v-if="!isLoading && groups.length > 0" class="select-items">
      <li v-for="group in groups" :key="group.id" class="select-item">
        <a href="#" class="select-item-link">{{ group.name }}</a>
        <a
          :ref="'groupOptions' + group.id"
          class="select-item-options"
          @click="toggleContext(group.id)"
        >
          <i class="fas fa-ellipsis-v"></i>
        </a>
      </li>
    </ul>
    <div v-if="!isLoading && groups.length == 0" class="context-description">
      No results found
    </div>
    <Context ref="groupsItemContext">
      <ul class="context-menu">
        <li>
          <a href="#">
            <i class="context-menu-icon fas fa-fw fa-pen"></i>
            Rename group
          </a>
        </li>
        <li>
          <a href="#">
            <i class="context-menu-icon fas fa-fw fa-trash"></i>
            Delete group
          </a>
        </li>
      </ul>
    </Context>
    <div class="select-footer">
      <a class="select-footer-button" @click="$refs.createGroupModal.show()">
        <i class="fas fa-plus"></i>
        Create group
      </a>
    </div>
    <CreateGroupModal ref="createGroupModal"></CreateGroupModal>
  </Context>
</template>

<script>
import { mapGetters, mapState } from 'vuex'

import CreateGroupModal from '@/components/group/CreateGroupModal'

export default {
  name: 'GroupsItemContext',
  components: {
    CreateGroupModal
  },
  data() {
    return {
      open: false
    }
  },
  computed: {
    ...mapState({
      groups: state => state.group.items
    }),
    ...mapGetters({
      isLoading: 'group/isLoading'
    })
  },
  methods: {
    toggle(...args) {
      this.$store.dispatch('group/loadAll')
      this.$refs.groupContext.toggle(...args)
    },
    toggleContext(groupId) {
      const target = this.$refs['groupOptions' + groupId][0]
      this.$refs.groupsItemContext.toggle(target, 'bottom', 'right', 0)
    }
  }
}
</script>
