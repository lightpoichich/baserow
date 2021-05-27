<template>
  <Context>
    <template v-if="Object.keys(group).length > 0">
      <ul class="context__menu">
        <li>
          <a @click.prevent="showDeleteModal">
            <i class="context__menu-icon fas fa-fw fa-trash-alt"></i>
            Permanently delete
          </a>
        </li>
      </ul>
      <!--
      <DeleteUserModal
        ref="deleteUserModal"
        :user="user"
        @delete-user="onDeleteUser"
      ></DeleteUserModal>
      -->
    </template>
  </Context>
</template>

<script>
import context from '@baserow/modules/core/mixins/context'

export default {
  name: 'EditUserContext',
  mixins: [context],
  props: {
    group: {
      required: true,
      type: Object,
    },
  },
  methods: {
    showDeleteModal() {
      this.hide()
      this.$refs.deleteUserModal.show()
    },
  },
}
</script>
