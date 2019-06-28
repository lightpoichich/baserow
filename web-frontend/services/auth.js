import { client } from './client'

export default {
  login(username, password) {
    return client.post('/api/token-auth/', {
      username: username,
      password: password
    })
  },
  refresh(token) {
    return client.post('/api/token-refresh/', {
      token: token
    })
  }
}
