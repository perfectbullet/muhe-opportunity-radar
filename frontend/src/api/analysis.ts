/**
 * 分析 API
 */
import { apiClient } from './client'
import type {
  AnalysisRequest,
  AnalysisResponse,
  ComparisonRequest,
  ComparisonResponse,
} from '@/types/api'

/**
 * 单一视角分析
 */
export function analyzeSingle(data: AnalysisRequest): Promise<AnalysisResponse> {
  return apiClient.post('/analyze', data)
}

/**
 * 单一视角流式分析
 */
export function analyzeSingleStream(data: AnalysisRequest): EventSource {
  const params = new URLSearchParams()
  params.append('material', data.material)
  params.append('investor_id', data.investor_id)
  if (data.additional_context) {
    params.append('additional_context', data.additional_context)
  }

  const url = `/api/v1/analyze/stream?${params.toString()}`
  return new EventSource(url)
}

/**
 * 多视角对比分析
 */
export function compareMultiple(data: ComparisonRequest): Promise<ComparisonResponse> {
  return apiClient.post('/compare', data)
}

/**
 * 多视角流式对比分析
 * 注意：由于 POST 请求，需要使用 fetch + SSE 库
 */
export async function* compareMultipleStream(
  data: ComparisonRequest
): AsyncGenerator<string, void, unknown> {
  const response = await fetch('/api/v1/compare/stream', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(data),
  })

  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`)
  }

  const reader = response.body?.getReader()
  if (!reader) {
    throw new Error('Response body is not readable')
  }

  const decoder = new TextDecoder()

  try {
    while (true) {
      const { done, value } = await reader.read()
      if (done) break

      const chunk = decoder.decode(value, { stream: true })
      const lines = chunk.split('\n\n')

      for (const line of lines) {
        if (line.startsWith('data: ')) {
          const data = line.slice(6)
          if (data === '[DONE]') {
            return
          }
          yield data
        }
      }
    }
  } finally {
    reader.releaseLock()
  }
}
