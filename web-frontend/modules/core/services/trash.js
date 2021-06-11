export default (client) => {
  return {
    fetchStructure() {
      return client.get(`/trash/`)
    },
    fetchContents({ groupId, applicationId = null }) {
      const config = {
        params: {},
      }

      if (applicationId !== null) {
        config.params.application_id = applicationId
      }

      return client.get(`/trash/group/${groupId}/`, config)
    },
    emptyContents({ groupId, applicationId = null }) {
      const config = {
        params: {},
      }

      if (applicationId !== null) {
        config.params.application_id = applicationId
      }

      return client.delete(`/trash/group/${groupId}/`, config)
    },
    restore(trashEntry) {
      return client.patch(
        `/trash/item/${trashEntry.trash_item_type}/${trashEntry.trash_item_id}/`
      )
    },
  }
}
