<template>
  <div class="container mx-auto px-4 py-8">
    <n-card class="glass-card" title="🔄 多视角对比分析">
      <n-space vertical :size="20">
        <!-- 投资者多选 -->
        <n-form-item label="选择投资者（2-10位）">
          <n-select
            v-model:value="selectedInvestors"
            :options="investorOptions"
            placeholder="选择多位投资大师进行对比"
            multiple
            size="large"
            :max-tag-count="5"
          />
        </n-form-item>

        <!-- 分析材料输入 -->
        <n-form-item label="分析材料">
          <n-input
            v-model:value="material"
            type="textarea"
            placeholder="输入分析材料..."
            :rows="10"
            :maxlength="5000"
            show-count
          />
        </n-form-item>

        <!-- 额外上下文 -->
        <n-form-item label="额外上下文（可选）">
          <n-input
            v-model:value="context"
            placeholder="提供额外的市场背景..."
            :maxlength="500"
            show-count
          />
        </n-form-item>

        <!-- 操作按钮 -->
        <n-space>
          <n-button
            type="primary"
            size="large"
            :loading="analyzing"
            :disabled="!canAnalyze"
            @click="handleCompare"
          >
            <template #icon>
              <n-icon><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path fill="currentColor" d="M9 3L5 6.99h3V14h2V6.99h3L9 3zm7 14.01V10h-2v7.01h-3L15 21l4-3.99h-3z"/></svg></n-icon>
            </template>
            开始对比分析
          </n-button>
          <n-button @click="handleClear">清空</n-button>
        </n-space>

        <!-- 对比结果 -->
        <div v-if="result">
          <!-- 各投资者分析 -->
          <n-space vertical :size="15">
            <n-card
              v-for="analysis in result.analyses"
              :key="analysis.investor_id"
              :title="`${analysis.investor_name} - ${analysis.investor_title}`"
              class="analysis-card"
            >
              <div class="markdown-body" v-html="renderMarkdown(analysis.analysis)"></div>
            </n-card>

            <!-- 综合对比总结 -->
            <n-card title="🔍 综合对比总结" class="summary-card">
              <div class="markdown-body" v-html="renderMarkdown(result.comparison_summary)"></div>
            </n-card>
          </n-space>
        </div>
      </n-space>
    </n-card>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useMessage } from 'naive-ui'
import { getAllInvestors, compareMultiple } from '@/api'
import type { Investor, ComparisonResponse } from '@/types/api'
import MarkdownIt from 'markdown-it'

const message = useMessage()
const md = new MarkdownIt()

// 数据
const investors = ref<Investor[]>([])
const selectedInvestors = ref<string[]>([])
const material = ref('')
const context = ref('')
const analyzing = ref(false)
const result = ref<ComparisonResponse | null>(null)

// 计算属性
const investorOptions = computed(() =>
  investors.value.map((inv) => ({
    label: `${inv.name} - ${inv.title}`,
    value: inv.id,
  }))
)

const canAnalyze = computed(() =>
  selectedInvestors.value.length >= 2 &&
  selectedInvestors.value.length <= 10 &&
  material.value.length >= 10
)

// 方法
function renderMarkdown(text: string): string {
  return md.render(text)
}

async function loadInvestors() {
  try {
    const response = await getAllInvestors()
    investors.value = response.investors
  } catch (error: any) {
    message.error(`加载投资者列表失败: ${error.message}`)
  }
}

async function handleCompare() {
  if (!canAnalyze.value) return

  analyzing.value = true
  result.value = null

  try {
    const response = await compareMultiple({
      material: material.value,
      investor_ids: selectedInvestors.value,
      additional_context: context.value || undefined,
    })

    result.value = response
    message.success('对比分析完成！')
  } catch (error: any) {
    message.error(`对比分析失败: ${error.message}`)
  } finally {
    analyzing.value = false
  }
}

function handleClear() {
  material.value = ''
  context.value = ''
  result.value = null
}

// 生命周期
onMounted(() => {
  loadInvestors()
})
</script>

<style scoped>
.glass-card {
  backdrop-filter: blur(10px);
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.analysis-card,
.summary-card {
  background: rgba(255, 255, 255, 0.05);
  backdrop-filter: blur(5px);
}

.markdown-body {
  line-height: 1.8;
}
</style>
