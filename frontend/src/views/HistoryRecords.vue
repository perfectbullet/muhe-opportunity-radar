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
                <n-button text @click="viewDetail(record.record_id)">
                  查看详情 →
                </n-button>
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
    </n-modal>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useMessage } from 'naive-ui'
import { getRecentRecords, searchRecords, getRecordDetail, getAllInvestors } from '@/api'
import type { RecordItem, Investor } from '@/types/api'
import MarkdownIt from 'markdown-it'

const message = useMessage()
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

// 计算属性
const investorFilterOptions = computed(() => [
  { label: '全部', value: undefined },
  ...investors.value.map((inv) => ({
    label: inv.name,
    value: inv.id,
  })),
])

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
