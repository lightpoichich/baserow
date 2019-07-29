import { client } from './client'

export default {
  fetchAll() {
    return client.get('/groups/')
  }
}
