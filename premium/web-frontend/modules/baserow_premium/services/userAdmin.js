export default (client) => {
  return {
    fetchPage(page) {
      return client.get(`/premium/user/?page=${page}`)
    },
    update(userId, values) {
      return client.patch(`/premium/user/${userId}/`, values)
    },
    delete(userId) {
      return client.delete(`/premium/user/${userId}/`)
    },
  }
}
