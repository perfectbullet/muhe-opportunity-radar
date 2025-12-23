import { apiClient } from './client'
import axios from 'axios'
import type { 
  DocumentUploadResponse,
  DocumentAnalysisResponse,
  DocumentInfo,
  DocumentMarkdownResponse,
  DocumentMetricsResponse,
  DocumentReportResponse,
  DocumentFullInfoResponse
} from '../types/api'

/**
 * 文档管理 API 客户端
 */

/**
 * 上传文档
 * @param file - 文档文件
 * @param investorId - 投资者 ID（可选）
 * @param autoAnalyze - 是否自动分析（可选）
 */
export const uploadDocument = async (
  file: File,
  investorId?: string,
  autoAnalyze: boolean = false
): Promise<DocumentUploadResponse> => {
  const formData = new FormData()
  formData.append('file', file)
  
  if (investorId) {
    formData.append('investor_id', investorId)
  }
  
  formData.append('auto_analyze', String(autoAnalyze))
  
  // 注意：文件上传需要使用原生 axios，因为 apiClient 不支持 FormData 的特殊处理
  const apiBaseUrl = import.meta.env.VITE_API_BASE_URL || '/api/v1'
  const response = await axios.post(`${apiBaseUrl}/documents/upload`, formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  })
  
  return response.data
}

/**
 * 使用工作流分析文档
 * @param documentId - 文档 ID
 * @param investorId - 投资者 ID
 * @param additionalContext - 额外上下文（可选）
 */
export const analyzeDocumentWithWorkflow = async (
  documentId: string,
  investorId: string,
  additionalContext?: string
): Promise<DocumentAnalysisResponse> => {
  return apiClient.post('/documents/analyze-workflow', {
    document_id: documentId,
    investor_id: investorId,
    additional_context: additionalContext,
  })
}

/**
 * 分析已上传的文档（简化版）
 * @param documentId - 文档 ID
 * @param investorId - 投资者 ID
 */
export const analyzeDocument = async (
  documentId: string,
  investorId: string
): Promise<DocumentAnalysisResponse> => {
  return apiClient.post('/documents/analyze-document', {
    document_id: documentId,
    investor_id: investorId,
  })
}

/**
 * 获取文档列表
 */
export const getDocuments = async (): Promise<DocumentInfo[]> => {
  const response = await apiClient.get<{ documents: DocumentInfo[]; total: number }>('/documents')
  return response.documents
}

/**
 * 删除文档
 * @param documentId - 文档 ID
 */
export const deleteDocument = async (documentId: string): Promise<{ message: string }> => {
  return apiClient.delete(`/documents/${documentId}`)
}

/**
 * 获取支持的文档格式
 */
export const getSupportedFormats = async (): Promise<{
  formats: string[]
  parser_info: Record<string, string>
}> => {
  return apiClient.get('/documents/supported-formats')
}

/**
 * 获取文档的 Markdown 内容
 * @param documentId - 文档 ID
 */
export const getDocumentMarkdown = async (documentId: string): Promise<DocumentMarkdownResponse> => {
  return apiClient.get(`/documents/${documentId}/markdown`)
}

/**
 * 获取文档的财务指标
 * @param documentId - 文档 ID
 */
export const getDocumentMetrics = async (documentId: string): Promise<DocumentMetricsResponse> => {
  return apiClient.get(`/documents/${documentId}/metrics`)
}

/**
 * 获取文档的分析报告列表
 * @param documentId - 文档 ID
 * @param investorId - 投资者 ID（可选，筛选特定投资者的报告）
 */
export const getDocumentReports = async (
  documentId: string,
  investorId?: string
): Promise<DocumentReportResponse[]> => {
  const params = investorId ? { investor_id: investorId } : undefined
  return apiClient.get(`/documents/${documentId}/reports`, params)
}

/**
 * 获取文档的完整信息（包含 markdown、指标、报告）
 * @param documentId - 文档 ID
 */
export const getDocumentFullInfo = async (documentId: string): Promise<DocumentFullInfoResponse> => {
  return apiClient.get(`/documents/${documentId}/full`)
}
