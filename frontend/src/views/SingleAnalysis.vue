<template>
  <div class="container mx-auto px-4 py-8">
    <n-card class="glass-card" title="🎯 单一视角分析">
      <n-space vertical :size="20">
        <!-- 投资者选择 -->
        <n-form-item label="选择投资者">
          <n-select
            v-model:value="selectedInvestor"
            :options="investorOptions"
            placeholder="选择一位投资大师"
            size="large"
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
            placeholder="提供额外的市场背景或分析要求..."
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
            @click="handleAnalyze"
          >
            <template #icon>
              <n-icon><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path fill="currentColor" d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z"/></svg></n-icon>
            </template>
            开始分析
          </n-button>
          <n-button @click="handleClear">清空</n-button>
        </n-space>

        <!-- 分析结果 -->
        <n-card v-if="result" title="📊 分析结果" class="result-card">
          <div class="markdown-body" v-html="renderedResult"></div>
        </n-card>
      </n-space>
    </n-card>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useMessage } from 'naive-ui'
import { getAllInvestors, analyzeSingle } from '@/api'
import type { Investor } from '@/types/api'
import MarkdownIt from 'markdown-it'

const message = useMessage()
const md = new MarkdownIt()

// 数据
const investors = ref<Investor[]>([])
const selectedInvestor = ref<string>('')
const material = ref('')
const context = ref('')
const analyzing = ref(false)
const result = ref('')

// 计算属性
const investorOptions = computed(() =>
  investors.value.map((inv) => ({
    label: `${inv.name} - ${inv.title}`,
    value: inv.id,
  }))
)

const canAnalyze = computed(() => selectedInvestor.value && material.value.length >= 10)

const renderedResult = computed(() => md.render(result.value))

// 方法
async function loadInvestors() {
  try {
    const response = await getAllInvestors()
    investors.value = response.investors
  } catch (error: any) {
    message.error(`加载投资者列表失败: ${error.message}`)
  }
}

async function handleAnalyze() {
  if (!canAnalyze.value) return

  analyzing.value = true
  result.value = ''

  try {
    const response = await analyzeSingle({
      material: material.value,
      investor_id: selectedInvestor.value,
      additional_context: context.value || undefined,
    })

    result.value = response.analysis
    message.success('分析完成！')
  } catch (error: any) {
    message.error(`分析失败: ${error.message}`)
  } finally {
    analyzing.value = false
  }
}

function handleClear() {
  material.value = ''
  context.value = ''
  result.value = ''
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

.result-card {
  margin-top: 20px;
  max-height: 600px;
  overflow-y: auto;
}

.markdown-body {
  line-height: 1.8;
}
</style>
