import client from './client'

export function findPriorArt(patentId, keywords) {
  return client.post('/validity/prior-art', { patent_id: patentId, keywords })
}
