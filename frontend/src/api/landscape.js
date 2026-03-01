import client from './client'

export function analyzeLandscape(domain, keywords) {
  return client.post('/landscape/analyze', { domain, keywords })
}
