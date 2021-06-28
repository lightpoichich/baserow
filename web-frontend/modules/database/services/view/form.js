export default (client) => {
  return {
    rotateSlug(formId) {
      return client.post(`/database/views/form/${formId}/rotate-slug/`)
    },
  }
}
