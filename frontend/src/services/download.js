import api from '@/services/api'

// Fetch a file with the session cookie (a plain <a href> would not be authenticated cross-origin) and save it.
export async function downloadFile(url, filename) {
  const response = await api.get(url, { responseType: 'blob' })
  const href = URL.createObjectURL(response.data)
  const link = document.createElement('a')
  link.href = href
  link.download = filename
  document.body.appendChild(link)
  link.click()
  link.remove()
  URL.revokeObjectURL(href)
}
