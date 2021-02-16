export default (client) => {
  return {
    get() {
      return client.get('/config/')
    },
    update(values) {
      return client.patch('/config/update/', values)
    },
  }
}
