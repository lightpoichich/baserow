export default (client) => {
  return {
    rotateSlug(formId) {
      return client.post(`/database/views/form/${formId}/rotate-slug/`)
    },
    getMetaInformation(slug) {
      return client.get(`/database/views/form/${slug}/submit/`)
    },
    submit(slug, values) {
      return client.post(`/database/views/form/${slug}/submit/`, values)
    },
  }
}
