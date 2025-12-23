<template>
  <n-config-provider :theme="darkTheme" :theme-overrides="themeOverrides">
    <n-message-provider>
      <n-notification-provider>
        <n-dialog-provider>
          <div class="app-container">
            <router-view />
          </div>
        </n-dialog-provider>
      </n-notification-provider>
    </n-message-provider>
  </n-config-provider>
</template>

<script setup lang="ts">
import { darkTheme, type GlobalThemeOverrides } from 'naive-ui'

const themeOverrides: GlobalThemeOverrides = {
  common: {
    primaryColor: '#3b82f6',
    primaryColorHover: '#60a5fa',
    primaryColorPressed: '#2563eb',
    primaryColorSuppl: '#6366f1',
    borderRadius: '8px',
    fontSize: '14px',
    baseColor: '#0f172a',
  },
  Card: {
    color: '#0f172a',
    colorModal: '#1e293b',
    borderRadius: '16px',
    boxShadow: '0 8px 32px rgba(0, 0, 0, 0.5)',
  },
  Button: {
    borderRadius: '8px',
    colorHover: '#1e293b',
    textColorPrimary: '#ffffff',
  },
  Input: {
    color: '#1e293b',
    colorFocus: '#1e293b',
    border: '1px solid rgba(59, 130, 246, 0.3)',
  },
}
</script>

<style scoped>
.app-container {
  min-height: 100vh;
}
</style>
