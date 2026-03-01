import client from './client'

export function submitQuery(query) {
  return client.post('/query', { query })
}

export function healthCheck() {
  return client.get('/health')
}
