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
    primaryColor: '#667eea',
    primaryColorHover: '#5a67d8',
    primaryColorPressed: '#4c51bf',
    borderRadius: '8px',
  },
  Card: {
    borderRadius: '12px',
  },
  Button: {
    borderRadius: '8px',
  },
}
</script>

<style scoped>
.app-container {
  min-height: 100vh;
}
</style>
