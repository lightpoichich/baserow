export default (client) => {
  return {
    fetchPage(page, searchQuery) {
      const params = { page }
      if (searchQuery) {
        params.search = searchQuery
      }
      return client.get(`/premium/admin/user/`, { params })
    },
    update(userId, values) {
      values.id = userId
      return client.patch(`/premium/admin/user/${userId}/`, values)
    },
    delete(userId) {
      return client.delete(`/premium/admin/user/${userId}/`)
    },
  }
}
