import axios from './client'
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
  
  const response = await axios.post('/documents/upload', formData, {
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
  const response = await axios.post('/documents/analyze-workflow', {
    document_id: documentId,
    investor_id: investorId,
    additional_context: additionalContext,
  })
  
  return response.data
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
  const response = await axios.post('/documents/analyze-document', {
    document_id: documentId,
    investor_id: investorId,
  })
  
  return response.data
}

/**
 * 获取文档列表
 */
export const getDocuments = async (): Promise<DocumentInfo[]> => {
  const response = await axios.get('/documents')
  return response.data
}

/**
 * 删除文档
 * @param documentId - 文档 ID
 */
export const deleteDocument = async (documentId: string): Promise<{ message: string }> => {
  const response = await axios.delete(`/documents/${documentId}`)
  return response.data
}

/**
 * 获取支持的文档格式
 */
export const getSupportedFormats = async (): Promise<{
  formats: string[]
  parser_info: Record<string, string>
}> => {
  const response = await axios.get('/documents/supported-formats')
  return response.data
}

/**
 * 获取文档的 Markdown 内容
 * @param documentId - 文档 ID
 */
export const getDocumentMarkdown = async (documentId: string): Promise<DocumentMarkdownResponse> => {
  const response = await axios.get(`/documents/${documentId}/markdown`)
  return response.data
}

/**
 * 获取文档的财务指标
 * @param documentId - 文档 ID
 */
export const getDocumentMetrics = async (documentId: string): Promise<DocumentMetricsResponse> => {
  const response = await axios.get(`/documents/${documentId}/metrics`)
  return response.data
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
  const params = investorId ? { investor_id: investorId } : {}
  const response = await axios.get(`/documents/${documentId}/reports`, { params })
  return response.data
}

/**
 * 获取文档的完整信息（包含 markdown、指标、报告）
 * @param documentId - 文档 ID
 */
export const getDocumentFullInfo = async (documentId: string): Promise<DocumentFullInfoResponse> => {
  const response = await axios.get(`/documents/${documentId}/full`)
  return response.data
}
