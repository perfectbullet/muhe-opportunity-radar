<template>
  <div class="document-view-container">
    <n-spin :show="loading" description="加载中...">
      <n-space vertical :size="24">
        <!-- 文档信息卡片 -->
        <n-card v-if="documentInfo" title="文档信息">
          <n-descriptions :column="2" bordered>
            <n-descriptions-item label="文件名">
              {{ documentInfo.document.filename }}
            </n-descriptions-item>
            <n-descriptions-item label="格式">
              <n-tag :type="getFormatType(documentInfo.document.format)">
                {{ documentInfo.document.format.toUpperCase() }}
              </n-tag>
            </n-descriptions-item>
            <n-descriptions-item label="上传时间">
              {{ formatDateTime(documentInfo.document.upload_time) }}
            </n-descriptions-item>
            <n-descriptions-item label="文档 ID">
              <n-text code>{{ documentInfo.document.document_id }}</n-text>
            </n-descriptions-item>
          </n-descriptions>
        </n-card>

        <!-- Markdown 内容 -->
        <n-card v-if="documentInfo?.markdown_content" title="文档内容">
          <n-scrollbar style="max-height: 600px">
            <div class="markdown-content" v-html="renderedMarkdown"></div>
          </n-scrollbar>
        </n-card>

        <!-- 财务指标 -->
        <n-card v-if="documentInfo?.metrics" title="财务指标分析">
          <n-space vertical :size="16">
            <!-- 指标详情 -->
            <n-descriptions v-if="documentInfo.metrics.metrics" :column="2" bordered>
              <n-descriptions-item
                v-for="(value, key) in documentInfo.metrics.metrics"
                :key="key"
                :label="formatMetricLabel(key)"
              >
                <n-text :type="getMetricType(key, value)">
                  {{ formatMetricValue(value) }}
                </n-text>
              </n-descriptions-item>
            </n-descriptions>

            <!-- 汇总信息 -->
            <n-alert v-if="documentInfo.metrics.summary" type="info" title="指标汇总">
              <pre>{{ JSON.stringify(documentInfo.metrics.summary, null, 2) }}</pre>
            </n-alert>
          </n-space>
        </n-card>

        <!-- 分析报告 -->
        <n-card v-if="documentInfo?.reports && documentInfo.reports.length > 0" title="投资分析报告">
          <n-space vertical :size="12">
            <n-collapse>
              <n-collapse-item
                v-for="report in documentInfo.reports"
                :key="report._id"
                :title="`${report.investor_name} 的分析报告`"
                :name="report._id"
              >
                <template #header-extra>
                  <n-tag type="success">
                    {{ formatDateTime(report.created_at) }}
                  </n-tag>
                </template>

                <!-- 报告内容 -->
                <n-space vertical :size="16">
                  <!-- Markdown 报告 -->
                  <div class="markdown-content" v-html="renderMarkdown(report.report_markdown)"></div>

                  <!-- 结构化数据 -->
                  <n-card v-if="Object.keys(report.structured_data || {}).length > 0" title="结构化数据" size="small">
                    <n-descriptions :column="1" bordered size="small">
                      <n-descriptions-item
                        v-for="(value, key) in report.structured_data"
                        :key="key"
                        :label="formatStructuredDataLabel(key)"
                      >
                        {{ formatStructuredDataValue(value) }}
                      </n-descriptions-item>
                    </n-descriptions>
                  </n-card>
                </n-space>
              </n-collapse-item>
            </n-collapse>
          </n-space>
        </n-card>

        <!-- 无数据提示 -->
        <n-empty
          v-if="!loading && (!documentInfo || (!documentInfo.markdown_content && !documentInfo.metrics && !documentInfo.reports?.length))"
          description="暂无数据"
        >
          <template #extra>
            <n-button @click="router.push('/documents/upload')">
              返回上传页面
            </n-button>
          </template>
        </n-empty>

        <!-- 操作按钮 -->
        <n-space v-if="documentInfo" justify="end">
          <n-button @click="router.push('/documents/upload')">
            返回
          </n-button>
          <n-button type="primary" @click="refreshData">
            <template #icon>
              <n-icon><RefreshOutline /></n-icon>
            </template>
            刷新
          </n-button>
        </n-space>
      </n-space>
    </n-spin>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import {
  NCard,
  NSpace,
  NSpin,
  NDescriptions,
  NDescriptionsItem,
  NTag,
  NText,
  NScrollbar,
  NAlert,
  NCollapse,
  NCollapseItem,
  NEmpty,
  NButton,
  NIcon,
  useMessage,
} from 'naive-ui'
import { RefreshOutline } from '@vicons/ionicons5'
import { marked } from 'marked'
import { getDocumentFullInfo } from '@/api'
import type { DocumentFullInfoResponse } from '@/types/api'

const route = useRoute()
const router = useRouter()
const message = useMessage()

const loading = ref(false)
const documentInfo = ref<DocumentFullInfoResponse | null>(null)

// 获取文档 ID
const documentId = computed(() => route.params.id as string)

// 加载文档数据
const loadDocumentData = async () => {
  if (!documentId.value) {
    message.error('文档 ID 无效')
    return
  }

  loading.value = true
  try {
    documentInfo.value = await getDocumentFullInfo(documentId.value)
  } catch (error: any) {
    message.error(`加载文档失败: ${error.message}`)
    console.error('Load document error:', error)
  } finally {
    loading.value = false
  }
}

// 刷新数据
const refreshData = async () => {
  await loadDocumentData()
  message.success('数据已刷新')
}

// 渲染 Markdown
const renderedMarkdown = computed(() => {
  if (!documentInfo.value?.markdown_content) return ''
  return marked.parse(documentInfo.value.markdown_content)
})

const renderMarkdown = (content: string) => {
  return marked.parse(content || '')
}

// 格式化日期时间
const formatDateTime = (dateString: string) => {
  return new Date(dateString).toLocaleString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit',
  })
}

// 获取格式类型
const getFormatType = (format: string) => {
  const typeMap: Record<string, any> = {
    pdf: 'error',
    docx: 'info',
    doc: 'info',
    md: 'success',
    markdown: 'success',
  }
  return typeMap[format.toLowerCase()] || 'default'
}

// 格式化指标标签
const formatMetricLabel = (key: string) => {
  const labelMap: Record<string, string> = {
    pe: '市盈率 (PE)',
    pb: '市净率 (PB)',
    roe: '净资产收益率 (ROE)',
    peg: 'PEG 比率',
    revenue_growth: '营收增长率',
    net_profit_margin: '净利润率',
    debt_ratio: '资产负债率',
    current_ratio: '流动比率',
  }
  return labelMap[key] || key
}

// 格式化指标值
const formatMetricValue = (value: any) => {
  if (typeof value === 'number') {
    return value.toFixed(2)
  }
  if (typeof value === 'string') {
    return value
  }
  return JSON.stringify(value)
}

// 获取指标类型（用于着色）
const getMetricType = (key: string, value: any) => {
  if (typeof value !== 'number') return 'default'
  
  // 根据指标类型判断好坏
  if (key === 'roe' && value > 15) return 'success'
  if (key === 'roe' && value < 8) return 'error'
  if (key === 'debt_ratio' && value > 70) return 'warning'
  if (key === 'current_ratio' && value < 1) return 'error'
  
  return 'default'
}

// 格式化结构化数据标签
const formatStructuredDataLabel = (key: string) => {
  const labelMap: Record<string, string> = {
    recommendation: '投资建议',
    risk_level: '风险等级',
    target_price: '目标价格',
    holding_period: '建议持有期',
    key_points: '关键要点',
    risks: '主要风险',
  }
  return labelMap[key] || key
}

// 格式化结构化数据值
const formatStructuredDataValue = (value: any) => {
  if (Array.isArray(value)) {
    return value.join(', ')
  }
  if (typeof value === 'object') {
    return JSON.stringify(value, null, 2)
  }
  return String(value)
}

// 初始化
onMounted(async () => {
  await loadDocumentData()
})
</script>

<style scoped>
.document-view-container {
  padding: 24px;
  max-width: 1400px;
  margin: 0 auto;
}

.markdown-content {
  padding: 16px;
  line-height: 1.8;
  color: var(--n-text-color);
}

.markdown-content :deep(h1) {
  font-size: 2em;
  margin-bottom: 0.5em;
  border-bottom: 1px solid var(--n-border-color);
  padding-bottom: 0.3em;
}

.markdown-content :deep(h2) {
  font-size: 1.5em;
  margin-top: 1em;
  margin-bottom: 0.5em;
}

.markdown-content :deep(h3) {
  font-size: 1.25em;
  margin-top: 0.8em;
  margin-bottom: 0.4em;
}

.markdown-content :deep(p) {
  margin-bottom: 1em;
}

.markdown-content :deep(ul),
.markdown-content :deep(ol) {
  margin-bottom: 1em;
  padding-left: 2em;
}

.markdown-content :deep(code) {
  background-color: var(--n-color-embedded);
  padding: 2px 6px;
  border-radius: 4px;
  font-family: 'Consolas', 'Monaco', monospace;
}

.markdown-content :deep(pre) {
  background-color: var(--n-color-embedded);
  padding: 12px;
  border-radius: 4px;
  overflow-x: auto;
  margin-bottom: 1em;
}

.markdown-content :deep(blockquote) {
  border-left: 4px solid var(--n-border-color);
  padding-left: 16px;
  margin: 1em 0;
  color: var(--n-text-color-depth-3);
}
</style>
