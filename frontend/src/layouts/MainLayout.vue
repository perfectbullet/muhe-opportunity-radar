<template>
  <n-layout has-sider class="main-layout">
    <n-layout-sider
      bordered
      collapse-mode="width"
      :collapsed-width="64"
      :width="240"
      :collapsed="collapsed"
      show-trigger
      @collapse="collapsed = true"
      @expand="collapsed = false"
      class="layout-sider"
    >
      <div class="logo-container">
        <div class="logo-icon">🎯</div>
        <transition name="fade">
          <div v-if="!collapsed" class="logo-text">炑禾机会雷达</div>
        </transition>
      </div>
      
      <n-menu
        :collapsed="collapsed"
        :collapsed-width="64"
        :collapsed-icon-size="22"
        :options="menuOptions"
        :value="activeKey"
        @update:value="handleMenuSelect"
        class="nav-menu"
      />
      
      <div class="sider-footer">
        <n-divider style="margin: 12px 0" />
        <div v-if="!collapsed" class="footer-text">
          <n-text depth="3" style="font-size: 12px;">
            Powered by AI
          </n-text>
        </div>
      </div>
    </n-layout-sider>
    
    <n-layout class="content-layout">
      <n-layout-header bordered class="layout-header">
        <div class="header-content">
          <n-breadcrumb>
            <n-breadcrumb-item>{{ currentPageTitle }}</n-breadcrumb-item>
          </n-breadcrumb>
          
          <div class="header-actions">
            <n-button text @click="handleRefresh">
              <template #icon>
                <n-icon :component="RefreshOutline" />
              </template>
            </n-button>
          </div>
        </div>
      </n-layout-header>
      
      <n-layout-content class="layout-content" content-style="padding: 24px;">
        <router-view v-slot="{ Component }">
          <transition name="fade-slide" mode="out-in">
            <component :is="Component" />
          </transition>
        </router-view>
      </n-layout-content>
    </n-layout>
  </n-layout>
</template>

<script setup lang="ts">
import { ref, computed, h } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import type { MenuOption } from 'naive-ui'
import { 
  AnalyticsOutline,
  GitCompareOutline,
  TimeOutline,
  StatsChartOutline,
  RefreshOutline,
  CloudUploadOutline
} from '@vicons/ionicons5'
import { NIcon } from 'naive-ui'

const router = useRouter()
const route = useRoute()

const collapsed = ref(false)

// 菜单选项
const menuOptions: MenuOption[] = [
  {
    label: '单一视角分析',
    key: 'analysis',
    icon: () => h(NIcon, null, { default: () => h(AnalyticsOutline) })
  },
  {
    label: '多视角对比',
    key: 'comparison',
    icon: () => h(NIcon, null, { default: () => h(GitCompareOutline) })
  },
  {
    label: '历史记录',
    key: 'history',
    icon: () => h(NIcon, null, { default: () => h(TimeOutline) })
  },
  {
    label: '统计信息',
    key: 'statistics',
    icon: () => h(NIcon, null, { default: () => h(StatsChartOutline) })
  },
  {
    type: 'divider',
    key: 'divider-1'
  },
  {
    label: '文档管理',
    key: 'documentUpload',
    icon: () => h(NIcon, null, { default: () => h(CloudUploadOutline) })
  }
]

// 当前激活的菜单
const activeKey = computed(() => {
  const name = route.name as string
  // 文档查看页面也高亮文档管理菜单
  if (name === 'documentView') {
    return 'documentUpload'
  }
  return name || 'analysis'
})

// 当前页面标题
const currentPageTitle = computed(() => {
  const meta = route.meta
  return meta.title || '炑禾机会雷达'
})

// 菜单选择
const handleMenuSelect = (key: string) => {
  router.push({ name: key })
}

// 刷新页面
const handleRefresh = () => {
  window.location.reload()
}
</script>

<style scoped>
.main-layout {
  height: 100vh;
  background: #0a0e27;
}

.layout-sider {
  background: #0f172a !important;
  box-shadow: 2px 0 8px rgba(0, 0, 0, 0.3);
}

.logo-container {
  display: flex;
  align-items: center;
  padding: 20px 16px;
  gap: 12px;
  border-bottom: 1px solid rgba(59, 130, 246, 0.2);
  margin-bottom: 8px;
}

.logo-icon {
  font-size: 32px;
  line-height: 1;
  filter: drop-shadow(0 0 8px rgba(59, 130, 246, 0.5));
}

.logo-text {
  font-size: 18px;
  font-weight: 600;
  background: linear-gradient(135deg, #3b82f6 0%, #6366f1 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  white-space: nowrap;
}

.nav-menu {
  background: transparent !important;
}

.sider-footer {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  padding: 12px 16px;
  background: rgba(15, 23, 42, 0.8);
}

.footer-text {
  text-align: center;
}

.content-layout {
  background: transparent;
}

.layout-header {
  background: rgba(15, 23, 42, 0.8) !important;
  backdrop-filter: blur(10px);
  border-bottom: 1px solid rgba(59, 130, 246, 0.2) !important;
  padding: 0 24px;
  height: 64px;
  display: flex;
  align-items: center;
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100%;
}

.header-actions {
  display: flex;
  gap: 12px;
  align-items: center;
}

.layout-content {
  background: transparent;
  min-height: calc(100vh - 64px);
  overflow-y: auto;
}

/* 过渡动画 */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

.fade-slide-enter-active {
  transition: all 0.3s ease-out;
}

.fade-slide-leave-active {
  transition: all 0.2s ease-in;
}

.fade-slide-enter-from {
  opacity: 0;
  transform: translateX(20px);
}

.fade-slide-leave-to {
  opacity: 0;
  transform: translateX(-20px);
}

/* 滚动条样式 */
.layout-content :deep(.n-layout-scroll-container)::-webkit-scrollbar {
  width: 8px;
}

.layout-content :deep(.n-layout-scroll-container)::-webkit-scrollbar-track {
  background: rgba(15, 23, 42, 0.5);
}

.layout-content :deep(.n-layout-scroll-container)::-webkit-scrollbar-thumb {
  background: linear-gradient(180deg, #3b82f6 0%, #6366f1 100%);
  border-radius: 4px;
}
</style>
