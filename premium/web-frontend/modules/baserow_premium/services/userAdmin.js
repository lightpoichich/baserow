export default (client) => {
  return {
    fetchPage(page, searchQuery, sorts) {
      const params = { page }
      if (searchQuery) {
        params.search = searchQuery
      }
      if (sorts.length > 0) {
        params.sorts = sorts
          .map((s) => {
            const direction = s.direction === 'asc' ? '-' : '+'
            return `${direction}${s.key}`
          })
          .join(',')
      }
      return client.get(`/premium/admin/user/`, { params })
    },
    update(userId, values) {
      return client.patch(`/premium/admin/user/${userId}/`, values)
    },
    delete(userId) {
      return client.delete(`/premium/admin/user/${userId}/`)
    },
  }
}
