/**
 * API 类型定义
 */

export interface Investor {
  id: string
  name: string
  title: string
  style: string
  philosophy: string
}

export interface AnalysisRequest {
  material: string
  investor_id: string
  additional_context?: string
}

export interface ComparisonRequest {
  material: string
  investor_ids: string[]
  additional_context?: string
}

export interface AnalysisResponse {
  record_id: string
  investor_id: string
  investor_name: string
  analysis: string
  created_at: string
  metadata?: Record<string, any>
}

export interface ComparisonAnalysis {
  investor_id: string
  investor_name: string
  investor_title: string
  analysis: string
}

export interface ComparisonResponse {
  record_id: string
  investor_ids: string[]
  analyses: ComparisonAnalysis[]
  comparison_summary: string
  created_at: string
}

export interface RecordItem {
  record_id: string
  type: 'single' | 'comparison'
  material: string
  investor_name?: string
  investor_names?: string[]
  created_at: string
  preview: string
}

export interface RecordListResponse {
  records: RecordItem[]
  total: number
  page: number
}

export interface StatisticsResponse {
  total_count: number
  by_investor: Record<string, number>
  by_type: Record<string, number>
  recent_days: number
}

export interface InvestorListResponse {
  investors: Investor[]
  total: number
}
