export default (client) => {
  return {
    fetchPage(page, searchQuery) {
      const searchQueryParam = searchQuery ? `&search=${searchQuery}` : ''
      return client.get(`/premium/admin/user/?page=${page}${searchQueryParam}`)
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
