<template>
  <Modal ref="createGroupModal">
    <h2 class="box-title">Create new group</h2>
    <form>
      <div class="control">
        <label class="control-label">
          <i class="fas fa-font"></i>
          Name
        </label>
        <div class="control-elements">
          <input type="text" class="input input-large" />
        </div>
      </div>
    </form>
  </Modal>
</template>

<script>
export default {
  name: 'CreateGroupModal',
  methods: {
    show() {
      this.$refs.createGroupModal.show()
    }
  }
}
</script>
