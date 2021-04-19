export default (client) => {
  return {
    fetchPage(page) {
      return client.get(`/premium/users/?page=${page}`)
    },
  }
}
