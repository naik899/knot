import client from './client'

export function resolveCompany(companyName) {
  return client.post('/corporate/resolve', { company_name: companyName })
}

export function getOwnershipGraph(companyId) {
  return client.get(`/corporate/graph/${companyId}`)
}
