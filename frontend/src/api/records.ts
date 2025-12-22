/**
 * 历史记录 API
 */
import { apiClient } from './client'
import type { RecordListResponse, StatisticsResponse } from '@/types/api'

/**
 * 获取最近记录
 */
export function getRecentRecords(
  limit: number = 20,
  investorFilter?: string
): Promise<RecordListResponse> {
  return apiClient.get('/records', {
    limit,
    investor_filter: investorFilter,
  })
}

/**
 * 获取记录详情
 */
export function getRecordDetail(recordId: string): Promise<any> {
  return apiClient.get(`/records/${recordId}`)
}

/**
 * 搜索记录
 */
export function searchRecords(
  keyword: string,
  limit: number = 20,
  investorFilter?: string
): Promise<RecordListResponse> {
  return apiClient.get(`/records/search/${keyword}`, {
    limit,
    investor_filter: investorFilter,
  })
}

/**
 * 获取统计信息
 */
export function getStatistics(): Promise<StatisticsResponse> {
  return apiClient.get('/statistics')
}
