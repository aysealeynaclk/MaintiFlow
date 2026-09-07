import axios from 'axios'
import { auth } from '../stores/auth'
import router from '../router'

const client = axios.create({ baseURL: '/api' })

client.interceptors.request.use((config) => {
  if (auth.token) {
    config.headers.Authorization = `Bearer ${auth.token}`
  }
  return config
})

client.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      auth.clearSession()
      router.push('/login')
    }
    return Promise.reject(error)
  }
)

export default client

/**
 * FastAPI hatalarini kullaniciya gosterilebilir bir metne cevirir.
 * `detail` duz bir string ise onu gosterir; 422 validasyon hatasi gibi
 * bir dizi/obje ise (FastAPI boyle donuyor) [object Object] gibi
 * cirkin bir sey yerine genel bir mesaja duser.
 */
export function getErrorMessage(err, fallback = 'Bir hata olustu, lutfen tekrar deneyin.') {
  const detail = err?.response?.data?.detail
  if (typeof detail === 'string') {
    return detail
  }
  return fallback
}
