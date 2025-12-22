import axios, { type AxiosInstance } from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || '/api/v1'

class ApiClient {
  private client: AxiosInstance

  constructor() {
    this.client = axios.create({
      baseURL: API_BASE_URL,
      timeout: 120000, // 120秒超时（AI 分析可能较慢）
      headers: {
        'Content-Type': 'application/json',
      },
    })

    // 请求拦截器
    this.client.interceptors.request.use(
      (config) => {
        return config
      },
      (error) => {
        return Promise.reject(error)
      }
    )

    // 响应拦截器
    this.client.interceptors.response.use(
      (response) => {
        return response.data
      },
      (error) => {
        const message = error.response?.data?.detail || error.message || '请求失败'
        return Promise.reject(new Error(message))
      }
    )
  }

  get<T = any>(url: string, params?: any): Promise<T> {
    return this.client.get(url, { params })
  }

  post<T = any>(url: string, data?: any): Promise<T> {
    return this.client.post(url, data)
  }

  put<T = any>(url: string, data?: any): Promise<T> {
    return this.client.put(url, data)
  }

  delete<T = any>(url: string): Promise<T> {
    return this.client.delete(url)
  }
}

export const apiClient = new ApiClient()
