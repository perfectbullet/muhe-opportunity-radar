<template>
  <div class="document-upload-container">
    <n-card title="文档上传与分析" class="main-card">
      <n-space vertical :size="24">
        <!-- 上传区域 -->
        <div>
          <n-upload
            ref="uploadRef"
            :action="`${apiBaseUrl}/documents/upload`"
            :headers="uploadHeaders"
            :data="uploadData"
            :max="1"
            :on-before-upload="handleBeforeUpload"
            :on-finish="handleUploadFinish"
            :on-error="handleUploadError"
            accept=".pdf,.docx,.doc,.md,.txt"
            :show-file-list="false"
          >
            <n-upload-dragger>
              <div style="margin-bottom: 12px">
                <n-icon size="48" :depth="3">
                  <CloudUploadOutline />
                </n-icon>
              </div>
              <n-text style="font-size: 16px">
                点击或拖拽文件到此区域上传
              </n-text>
              <n-p depth="3" style="margin: 8px 0 0 0">
                支持 PDF、Word、Markdown 格式，最大 10MB
              </n-p>
            </n-upload-dragger>
          </n-upload>
        </div>

        <!-- 上传配置 -->
        <n-card title="上传配置" size="small">
          <n-space vertical>
            <n-form-item label="选择投资者视角">
              <n-select
                v-model:value="selectedInvestorId"
                :options="investorOptions"
                placeholder="选择投资者（可选）"
                clearable
              />
            </n-form-item>
            
            <n-form-item label="自动分析">
              <n-switch v-model:value="autoAnalyze">
                <template #checked>
                  上传后自动分析
                </template>
                <template #unchecked>
                  仅上传，稍后分析
                </template>
              </n-switch>
            </n-form-item>
          </n-space>
        </n-card>

        <!-- 文档列表 -->
        <n-card title="已上传文档" size="small">
          <n-space vertical :size="12">
            <n-button
              @click="loadDocuments"
              :loading="documentsLoading"
              secondary
              type="info"
            >
              <template #icon>
                <n-icon><RefreshOutline /></n-icon>
              </template>
              刷新列表
            </n-button>

            <n-data-table
              :columns="documentColumns"
              :data="documents"
              :loading="documentsLoading"
              :pagination="pagination"
              :bordered="false"
              striped
            />
          </n-space>
        </n-card>
      </n-space>
    </n-card>

    <!-- 分析进度对话框 -->
    <n-modal
      v-model:show="showAnalysisModal"
      preset="card"
      title="文档分析中"
      style="width: 600px"
      :closable="false"
      :mask-closable="false"
    >
      <n-space vertical>
        <n-progress
          type="line"
          :percentage="analysisProgress"
          :indicator-placement="'inside'"
          processing
        />
        <n-text>{{ analysisStatus }}</n-text>
      </n-space>
    </n-modal>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, h } from 'vue'
import { useRouter } from 'vue-router'
import {
  NCard,
  NSpace,
  NUpload,
  NUploadDragger,
  NIcon,
  NText,
  NP,
  NFormItem,
  NSelect,
  NSwitch,
  NButton,
  NDataTable,
  NModal,
  NProgress,
  useMessage,
  type DataTableColumns,
  type UploadFileInfo,
} from 'naive-ui'
import { CloudUploadOutline, RefreshOutline, DocumentTextOutline, TrashOutline } from '@vicons/ionicons5'
import {
  uploadDocument,
  getDocuments,
  deleteDocument,
  analyzeDocumentWithWorkflow,
} from '@/api'
import { getInvestors } from '@/api/investors'
import type { DocumentInfo, Investor } from '@/types/api'

const router = useRouter()
const message = useMessage()

// API 配置
const apiBaseUrl = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api/v1'

// 上传配置
const selectedInvestorId = ref<string | null>(null)
const autoAnalyze = ref(true)
const uploadRef = ref()

// 投资者选项
const investorOptions = ref<{ label: string; value: string }[]>([])

// 文档列表
const documents = ref<DocumentInfo[]>([])
const documentsLoading = ref(false)

// 分析进度
const showAnalysisModal = ref(false)
const analysisProgress = ref(0)
const analysisStatus = ref('准备分析...')

// 分页配置
const pagination = {
  pageSize: 10,
}

// 上传头信息
const uploadHeaders = {
  // 可以添加认证 token 等
}

// 上传数据
const uploadData = () => ({
  investor_id: selectedInvestorId.value || '',
  auto_analyze: String(autoAnalyze.value),
})

// 加载投资者列表
const loadInvestors = async () => {
  try {
    const response = await getInvestors()
    investorOptions.value = response.investors.map((investor: Investor) => ({
      label: `${investor.name} - ${investor.title}`,
      value: investor.id,
    }))
  } catch (error: any) {
    message.error(`加载投资者列表失败: ${error.message}`)
  }
}

// 加载文档列表
const loadDocuments = async () => {
  documentsLoading.value = true
  try {
    documents.value = await getDocuments()
  } catch (error: any) {
    message.error(`加载文档列表失败: ${error.message}`)
  } finally {
    documentsLoading.value = false
  }
}

// 上传前检查
const handleBeforeUpload = (data: { file: UploadFileInfo }) => {
  const file = data.file.file as File
  const maxSize = 10 * 1024 * 1024 // 10MB
  
  if (file.size > maxSize) {
    message.error('文件大小不能超过 10MB')
    return false
  }
  
  const validExtensions = ['.pdf', '.docx', '.doc', '.md', '.txt']
  const fileName = file.name.toLowerCase()
  const isValidType = validExtensions.some(ext => fileName.endsWith(ext))
  
  if (!isValidType) {
    message.error('不支持的文件格式，请上传 PDF、Word 或 Markdown 文件')
    return false
  }
  
  return true
}

// 上传完成
const handleUploadFinish = async ({ file, event }: any) => {
  try {
    const response = JSON.parse((event.target as XMLHttpRequest).response)
    
    if (response.document_id) {
      message.success(`文件上传成功: ${response.filename}`)
      
      // 刷新文档列表
      await loadDocuments()
      
      // 如果有分析结果，显示提示
      if (response.analysis_result) {
        message.info('文档分析已完成，可在文档查看页面查看详情')
      }
    } else {
      message.error('上传失败，请重试')
    }
  } catch (error: any) {
    console.error('Upload finish error:', error)
    message.error(`上传处理失败: ${error.message}`)
  }
}

// 上传错误
const handleUploadError = ({ file, event }: any) => {
  console.error('Upload error:', event)
  message.error(`上传失败: ${file.name}`)
}

// 手动分析文档
const handleAnalyzeDocument = async (documentId: string) => {
  if (!selectedInvestorId.value) {
    message.warning('请先选择投资者视角')
    return
  }
  
  showAnalysisModal.value = true
  analysisProgress.value = 0
  analysisStatus.value = '开始分析...'
  
  try {
    analysisProgress.value = 30
    analysisStatus.value = '解析文档内容...'
    
    await analyzeDocumentWithWorkflow(documentId, selectedInvestorId.value)
    
    analysisProgress.value = 100
    analysisStatus.value = '分析完成！'
    
    message.success('文档分析完成')
    
    setTimeout(() => {
      showAnalysisModal.value = false
      // 跳转到查看页面
      router.push(`/documents/${documentId}`)
    }, 1000)
  } catch (error: any) {
    message.error(`分析失败: ${error.message}`)
    showAnalysisModal.value = false
  }
}

// 查看文档
const handleViewDocument = (documentId: string) => {
  router.push(`/documents/${documentId}`)
}

// 删除文档
const handleDeleteDocument = async (documentId: string) => {
  try {
    await deleteDocument(documentId)
    message.success('文档已删除')
    await loadDocuments()
  } catch (error: any) {
    message.error(`删除失败: ${error.message}`)
  }
}

// 表格列定义
const documentColumns: DataTableColumns<DocumentInfo> = [
  {
    title: '文件名',
    key: 'filename',
    ellipsis: {
      tooltip: true,
    },
  },
  {
    title: '格式',
    key: 'format',
    width: 80,
  },
  {
    title: '上传时间',
    key: 'upload_time',
    width: 180,
    render(row) {
      return new Date(row.upload_time).toLocaleString('zh-CN')
    },
  },
  {
    title: '操作',
    key: 'actions',
    width: 220,
    render(row) {
      return h(
        NSpace,
        {},
        {
          default: () => [
            h(
              NButton,
              {
                size: 'small',
                type: 'info',
                onClick: () => handleViewDocument(row.document_id),
              },
              {
                icon: () => h(NIcon, null, { default: () => h(DocumentTextOutline) }),
                default: () => '查看',
              }
            ),
            h(
              NButton,
              {
                size: 'small',
                type: 'primary',
                onClick: () => handleAnalyzeDocument(row.document_id),
                disabled: !selectedInvestorId.value,
              },
              { default: () => '分析' }
            ),
            h(
              NButton,
              {
                size: 'small',
                type: 'error',
                onClick: () => handleDeleteDocument(row.document_id),
              },
              {
                icon: () => h(NIcon, null, { default: () => h(TrashOutline) }),
              }
            ),
          ],
        }
      )
    },
  },
]

// 初始化
onMounted(async () => {
  await loadInvestors()
  await loadDocuments()
})
</script>

<style scoped>
.document-upload-container {
  padding: 24px;
  max-width: 1400px;
  margin: 0 auto;
}

.main-card {
  background: var(--n-color);
}

:deep(.n-upload-dragger) {
  padding: 40px 20px;
}
</style>
