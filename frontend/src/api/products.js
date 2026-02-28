import client from './client'

export function matchProducts(productDescription, keywords) {
  return client.post('/products/match', {
    product_description: productDescription,
    keywords,
  })
}
