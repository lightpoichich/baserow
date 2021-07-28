const RowCommentService = (client) => {
  return {
    fetchAll(tableId, rowId) {
      return client.get(`/row_comments/${tableId}/${rowId}/`)
    },
    create(tableId, rowId, comment) {
      return client.post(`/row_comments/${tableId}/${rowId}/`, { comment })
    },
  }
}
export default RowCommentService
