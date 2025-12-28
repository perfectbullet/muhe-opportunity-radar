<template>
  <div class="container mx-auto px-4 py-8">
    <n-card class="glass-card" title="📚 历史记录">
      <n-space vertical :size="20">
        <!-- 搜索和筛选 -->
        <n-space>
          <n-input
            v-model:value="searchKeyword"
            placeholder="搜索关键词..."
            clearable
            style="width: 300px"
          >
            <template #prefix>
              <n-icon><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path fill="currentColor" d="M15.5 14h-.79l-.28-.27A6.471 6.471 0 0 0 16 9.5 6.5 6.5 0 1 0 9.5 16c1.61 0 3.09-.59 4.23-1.57l.27.28v.79l5 4.99L20.49 19l-4.99-5zm-6 0C7.01 14 5 11.99 5 9.5S7.01 5 9.5 5 14 7.01 14 9.5 11.99 14 9.5 14z"/></svg></n-icon>
            </template>
          </n-input>
          <n-button type="primary" @click="handleSearch">搜索</n-button>
          <n-select
            v-model:value="filterInvestor"
            :options="investorFilterOptions"
            placeholder="筛选投资者"
            clearable
            style="width: 200px"
          />
          <n-button @click="handleReset">重置</n-button>
        </n-space>

        <!-- 记录列表 -->
        <n-list bordered>
          <n-list-item v-for="record in records" :key="record.record_id">
            <n-thing>
              <template #header>
                <n-space align="center">
                  <n-tag :type="record.type === 'comparison' ? 'info' : 'success'">
                    {{ record.type === 'comparison' ? '多视角' : '单一视角' }}
                  </n-tag>
                  <span v-if="record.investor_name">{{ record.investor_name }}</span>
                  <span v-else>{{ record.investor_names?.join('、') }}</span>
                </n-space>
              </template>
              <template #description>
                <n-text depth="3">
                  {{ new Date(record.created_at).toLocaleString() }}
                </n-text>
              </template>
              <n-ellipsis :line-clamp="2" :tooltip="false">
                {{ record.material }}
              </n-ellipsis>
              <template #footer>
                <n-space>
                  <n-button text @click="viewDetail(record.record_id)">
                    查看详情 →
                  </n-button>
                  <n-button text type="primary" @click="openReanalyzeDialog(record)">
                    重新分析 🔄
                  </n-button>
                </n-space>
              </template>
            </n-thing>
          </n-list-item>
          <template #footer>
            <n-pagination
              v-model:page="currentPage"
              :page-count="pageCount"
              show-size-picker
              :page-sizes="[10, 20, 50]"
              @update:page="handlePageChange"
            />
          </template>
        </n-list>
      </n-space>
    </n-card>

    <!-- 详情对话框 -->
    <n-modal v-model:show="showDetail" preset="card" style="width: 800px" title="记录详情">
      <div v-if="detailData" class="markdown-body" v-html="renderDetail()"></div>
      <template #footer>
        <n-space justify="end">
          <n-button @click="showDetail = false">关闭</n-button>
          <n-button type="primary" @click="openReanalyzeDialog(detailData)">
            使用此材料重新分析
          </n-button>
        </n-space>
      </template>
    </n-modal>

    <!-- 重新分析对话框 -->
    <n-modal v-model:show="showReanalyze" preset="card" style="width: 600px" title="🔄 重新分析材料">
      <n-space vertical :size="20">
        <n-alert type="info" title="重新分析说明">
          将使用原始材料进行新的分析。您可以选择不同的投资者视角或进行多视角对比。
        </n-alert>

        <n-form ref="reanalyzeFormRef" :model="reanalyzeForm">
          <n-form-item label="分析模式" path="mode">
            <n-radio-group v-model:value="reanalyzeForm.mode">
              <n-space>
                <n-radio value="single">单一视角</n-radio>
                <n-radio value="comparison">多视角对比</n-radio>
              </n-space>
            </n-radio-group>
          </n-form-item>

          <n-form-item v-if="reanalyzeForm.mode === 'single'" label="选择投资者" path="investorId">
            <n-select
              v-model:value="reanalyzeForm.investorId"
              :options="investorOptions"
              placeholder="选择一位投资者"
            />
          </n-form-item>

          <n-form-item v-if="reanalyzeForm.mode === 'comparison'" label="选择投资者" path="investorIds">
            <n-select
              v-model:value="reanalyzeForm.investorIds"
              :options="investorOptions"
              placeholder="选择2-10位投资者"
              multiple
              :max-tag-count="3"
            />
          </n-form-item>

          <n-form-item label="额外上下文（可选）" path="additionalContext">
            <n-input
              v-model:value="reanalyzeForm.additionalContext"
              type="textarea"
              placeholder="例如：当前市场环境、特殊考虑因素等..."
              :autosize="{ minRows: 3, maxRows: 6 }"
            />
          </n-form-item>
        </n-form>
      </n-space>

      <template #footer>
        <n-space justify="end">
          <n-button @click="showReanalyze = false">取消</n-button>
          <n-button type="primary" @click="handleReanalyze" :loading="reanalyzing">
            开始分析
          </n-button>
        </n-space>
      </template>
    </n-modal>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useMessage, useDialog } from 'naive-ui'
import { useRouter } from 'vue-router'
import { getRecentRecords, searchRecords, getRecordDetail, getAllInvestors, reanalyzeMaterial } from '@/api'
import type { RecordItem, Investor } from '@/types/api'
import MarkdownIt from 'markdown-it'

const message = useMessage()
const dialog = useDialog()
const router = useRouter()
const md = new MarkdownIt()

// 数据
const records = ref<RecordItem[]>([])
const investors = ref<Investor[]>([])
const searchKeyword = ref('')
const filterInvestor = ref<string>()
const currentPage = ref(1)
const pageCount = ref(1)
const showDetail = ref(false)
const detailData = ref<any>(null)

// 重新分析相关
const showReanalyze = ref(false)
const reanalyzing = ref(false)
const currentReanalyzeRecord = ref<any>(null)
const reanalyzeForm = ref({
  mode: 'single' as 'single' | 'comparison',
  investorId: '',
  investorIds: [] as string[],
  additionalContext: ''
})
const reanalyzeFormRef = ref()

// 计算属性
const investorFilterOptions = computed(() => [
  { label: '全部', value: undefined },
  ...investors.value.map((inv) => ({
    label: inv.name,
    value: inv.id,
  })),
])

const investorOptions = computed(() =>
  investors.value.map((inv) => ({
    label: `${inv.name} (${inv.title})`,
    value: inv.id,
  }))
)

// 方法
async function loadRecords() {
  try {
    const response = await getRecentRecords(20, filterInvestor.value)
    records.value = response.records
    pageCount.value = Math.ceil(response.total / 20)
  } catch (error: any) {
    message.error(`加载记录失败: ${error.message}`)
  }
}

async function handleSearch() {
  if (!searchKeyword.value) {
    loadRecords()
    return
  }

  try {
    const response = await searchRecords(searchKeyword.value, 20, filterInvestor.value)
    records.value = response.records
    pageCount.value = Math.ceil(response.total / 20)
  } catch (error: any) {
    message.error(`搜索失败: ${error.message}`)
  }
}

function handleReset() {
  searchKeyword.value = ''
  filterInvestor.value = undefined
  currentPage.value = 1
  loadRecords()
}

function handlePageChange(page: number) {
  currentPage.value = page
  // 实际应用中需要支持分页参数
  loadRecords()
}

async function viewDetail(recordId: string) {
  try {
    detailData.value = await getRecordDetail(recordId)
    showDetail.value = true
  } catch (error: any) {
    message.error(`加载详情失败: ${error.message}`)
  }
}

function renderDetail(): string {
  if (!detailData.value) return ''

  if (detailData.value.type === 'comparison') {
    let html = '<h2>多视角对比分析</h2>'
    detailData.value.analyses?.forEach((analysis: any) => {
      html += `<h3>${analysis.investor_name}</h3>`
      html += md.render(analysis.analysis)
    })
    html += '<h2>综合对比</h2>'
    html += md.render(detailData.value.comparison_summary || '')
    return html
  } else {
    return md.render(detailData.value.analysis_result || '')
  }
}

async function loadInvestors() {
  try {
    const response = await getAllInvestors()
    investors.value = response.investors
  } catch (error: any) {
    console.error('加载投资者列表失败:', error)
  }
}

// 打开重新分析对话框
function openReanalyzeDialog(record: any) {
  currentReanalyzeRecord.value = record
  reanalyzeForm.value = {
    mode: 'single',
    investorId: '',
    investorIds: [],
    additionalContext: ''
  }
  showReanalyze.value = true
}

// 执行重新分析
async function handleReanalyze() {
  try {
    // 验证表单
    if (reanalyzeForm.value.mode === 'single' && !reanalyzeForm.value.investorId) {
      message.warning('请选择一位投资者')
      return
    }
    
    if (reanalyzeForm.value.mode === 'comparison') {
      if (reanalyzeForm.value.investorIds.length < 2) {
        message.warning('多视角对比至少需要选择2位投资者')
        return
      }
      if (reanalyzeForm.value.investorIds.length > 10) {
        message.warning('最多只能选择10位投资者')
        return
      }
    }

    reanalyzing.value = true
    
    const recordId = currentReanalyzeRecord.value.record_id || currentReanalyzeRecord.value._id
    const requestData = {
      investor_id: reanalyzeForm.value.investorId,
      additional_context: reanalyzeForm.value.additionalContext || undefined,
      use_comparison: reanalyzeForm.value.mode === 'comparison',
      investor_ids: reanalyzeForm.value.mode === 'comparison' ? reanalyzeForm.value.investorIds : undefined
    }

    const result = await reanalyzeMaterial(recordId, requestData)
    
    message.success('重新分析完成！')
    showReanalyze.value = false
    
    // 显示结果对话框
    dialog.success({
      title: '分析完成',
      content: '已完成重新分析，是否查看结果？',
      positiveText: '查看结果',
      negativeText: '返回列表',
      onPositiveClick: () => {
        // 刷新记录列表并显示新记录
        loadRecords()
      }
    })
    
  } catch (error: any) {
    message.error(`重新分析失败: ${error.message || '未知错误'}`)
  } finally {
    reanalyzing.value = false
  }
}

// 生命周期
onMounted(() => {
  loadInvestors()
  loadRecords()
})
</script>

<style scoped>
.glass-card {
  backdrop-filter: blur(10px);
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
}
</style>
