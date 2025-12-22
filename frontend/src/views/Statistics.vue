<template>
  <div class="container mx-auto px-4 py-8">
    <n-card class="glass-card" title="📊 统计信息">
      <n-space vertical :size="30">
        <!-- 总览卡片 -->
        <n-grid :cols="3" :x-gap="20">
          <n-gi>
            <n-statistic label="总分析次数" :value="stats?.total_count || 0">
              <template #prefix>
                <n-icon size="24"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path fill="currentColor" d="M19 3H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zM9 17H7v-7h2v7zm4 0h-2V7h2v10zm4 0h-2v-4h2v4z"/></svg></n-icon>
              </template>
            </n-statistic>
          </n-gi>
          <n-gi>
            <n-statistic label="单一视角分析" :value="stats?.by_type?.single || 0">
              <template #prefix>
                <n-icon size="24" color="#18a058"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path fill="currentColor" d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z"/></svg></n-icon>
              </template>
            </n-statistic>
          </n-gi>
          <n-gi>
            <n-statistic label="多视角对比" :value="stats?.by_type?.comparison || 0">
              <template #prefix>
                <n-icon size="24" color="#2080f0"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path fill="currentColor" d="M9 3L5 6.99h3V14h2V6.99h3L9 3zm7 14.01V10h-2v7.01h-3L15 21l4-3.99h-3z"/></svg></n-icon>
              </template>
            </n-statistic>
          </n-gi>
        </n-grid>

        <!-- 投资者分析次数排行 -->
        <n-card title="📈 投资者分析次数排行">
          <div ref="chartRef" style="width: 100%; height: 400px"></div>
        </n-card>
      </n-space>
    </n-card>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, nextTick } from 'vue'
import { useMessage } from 'naive-ui'
import { getStatistics } from '@/api'
import type { StatisticsResponse } from '@/types/api'
import * as echarts from 'echarts'

const message = useMessage()
const stats = ref<StatisticsResponse | null>(null)
const chartRef = ref<HTMLElement>()

// 方法
async function loadStatistics() {
  try {
    stats.value = await getStatistics()
    await nextTick()
    renderChart()
  } catch (error: any) {
    message.error(`加载统计数据失败: ${error.message}`)
  }
}

function renderChart() {
  if (!chartRef.value || !stats.value) return

  const chart = echarts.init(chartRef.value)
  
  const data = Object.entries(stats.value.by_investor).map(([name, count]) => ({
    name,
    value: count,
  }))

  const option = {
    backgroundColor: 'transparent',
    tooltip: {
      trigger: 'axis',
      axisPointer: {
        type: 'shadow',
      },
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '3%',
      containLabel: true,
    },
    xAxis: {
      type: 'value',
      boundaryGap: [0, 0.01],
      axisLine: {
        lineStyle: {
          color: '#fff',
        },
      },
    },
    yAxis: {
      type: 'category',
      data: data.map((d) => d.name),
      axisLine: {
        lineStyle: {
          color: '#fff',
        },
      },
    },
    series: [
      {
        type: 'bar',
        data: data.map((d) => d.value),
        itemStyle: {
          color: new echarts.graphic.LinearGradient(0, 0, 1, 0, [
            { offset: 0, color: '#667eea' },
            { offset: 1, color: '#764ba2' },
          ]),
        },
        label: {
          show: true,
          position: 'right',
          color: '#fff',
        },
      },
    ],
  }

  chart.setOption(option)

  // 响应式
  window.addEventListener('resize', () => chart.resize())
}

// 生命周期
onMounted(() => {
  loadStatistics()
})
</script>

<style scoped>
.glass-card {
  backdrop-filter: blur(10px);
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
}
</style>
