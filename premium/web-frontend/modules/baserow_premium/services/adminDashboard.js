export default (client) => {
  return {
    dashboard() {
      return client.get(`/admin/dashboard/`)
    },
  }
}
