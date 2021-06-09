export default (client) => {
  return {
    fetchStructure() {
      return client.get(`/trash/`)
    },
  }
}
