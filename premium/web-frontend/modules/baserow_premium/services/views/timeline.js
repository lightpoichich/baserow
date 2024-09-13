import addPublicAuthTokenHeader from '@baserow/modules/database/utils/publicView'

export default (client) => {
  return {
    fetchRows({
      viewId,
      limit = 100,
      offset = null,
      includeFieldOptions = false,
      includeRowMetadata = true,
      userTimeZone = null,
      publicUrl = false,
      publicAuthToken = null,
      search = '',
      searchMode = '',
    }) {
      const include = []
      const params = new URLSearchParams()
      params.append('limit', limit)

      if (offset !== null) {
        params.append('offset', offset)
      }

      if (includeFieldOptions) {
        include.push('field_options')
      }

      if (includeRowMetadata) {
        include.push('row_metadata')
      }

      if (include.length > 0) {
        params.append('include', include.join(','))
      }

      if (userTimeZone) {
        params.append('user_timezone', userTimeZone)
      }
      if (search) {
        params.append('search', search)
        if (searchMode) {
          params.append('search_mode', searchMode)
        }
      }

      const config = { params }

      if (publicAuthToken) {
        addPublicAuthTokenHeader(config, publicAuthToken)
      }

      const url = publicUrl ? 'public/rows/' : ''

      return client.get(`/database/views/timeline/${viewId}/${url}`, config)
    },
  }
}
