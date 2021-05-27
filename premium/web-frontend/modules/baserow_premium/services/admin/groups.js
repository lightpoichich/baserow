import baseService from '@baserow_premium/crud_table/baseService'

export default (client) => {
  return baseService(client, '/admin/groups/')
}
