import client from './client'

export function searchPatents(query, jurisdictions) {
  const params = { q: query }
  if (jurisdictions) params.jurisdictions = jurisdictions
  return client.get('/patents/search', { params })
}

export function getPatent(patentId) {
  return client.get(`/patents/${patentId}`)
}
