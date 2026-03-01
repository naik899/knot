import client from './client'

export function analyzeFTO(productDescription, targetMarkets, keywords) {
  return client.post('/fto/analyze', {
    product_description: productDescription,
    target_markets: targetMarkets,
    keywords,
  })
}
