/**
 * 投资者 API
 */
import { apiClient } from './client'
import type { InvestorListResponse, Investor } from '@/types/api'

/**
 * 获取所有投资者列表
 */
export function getAllInvestors(): Promise<InvestorListResponse> {
  return apiClient.get('/investors')
}

/**
 * 获取所有投资者列表（别名）
 */
export const getInvestors = getAllInvestors

/**
 * 获取投资者详情
 */
export function getInvestorDetail(investorId: string): Promise<Investor> {
  return apiClient.get(`/investors/${investorId}`)
}
