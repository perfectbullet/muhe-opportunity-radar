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

// 文档管理相关类型
export interface DocumentInfo {
  document_id: string
  filename: string
  upload_time: string
  size?: number
  format?: string
}

export interface DocumentUploadResponse {
  document_id: string
  filename: string
  format: string
  message: string
  analysis_result?: DocumentAnalysisResponse
}

export interface DocumentAnalysisResponse {
  success: boolean
  document_info?: {
    format: string
    pages?: number
    metadata?: Record<string, any>
  }
  workflow_result?: {
    parsed_content?: string
    calculated_metrics?: {
      metrics: Record<string, any>
      summary: Record<string, any>
    }
    analysis_result?: string
    final_report?: {
      markdown: string
      structured_data: Record<string, any>
      metadata: Record<string, any>
    }
    investor_info?: {
      id: string
      name: string
      title: string
    }
  }
  final_report?: {
    markdown: string
    structured_data: Record<string, any>
    metadata: Record<string, any>
  }
  error?: string
}

export interface DocumentMarkdownResponse {
  document_id: string
  markdown_content: string
}

export interface DocumentMetricsResponse {
  document_id: string
  metrics: {
    _id?: string
    document_id: string
    metrics: Record<string, any>
    summary: Record<string, any>
    created_at: string
  }
}

export interface DocumentReportResponse {
  _id: string
  document_id: string
  investor_id: string
  investor_name: string
  report_markdown: string
  structured_data: Record<string, any>
  metadata: Record<string, any>
  created_at: string
}

export interface DocumentFullInfoResponse {
  document: {
    _id: string
    document_id: string
    filename: string
    content: string
    format: string
    markdown_content: string
    metadata: Record<string, any>
    upload_time: string
  }
  markdown_content: string
  metrics: DocumentMetricsResponse['metrics'] | null
  reports: DocumentReportResponse[]
}
