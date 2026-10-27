<script setup lang="ts">
defineProps<{ id: string }>()
</script>

<template>
  <svg class="h-10 w-10 text-teal" viewBox="0 0 48 48" fill="none" aria-hidden="true">
    <rect x="4" y="4" width="40" height="40" rx="12" stroke="currentColor" stroke-width="2" />
    <path v-if="id === 'buero'" d="M14 32V20h8v12M26 32V16h8v16" stroke="currentColor" stroke-width="2" stroke-linejoin="round" />
    <path v-else-if="id === 'treppenhaus'" d="M14 32h6v-6h6v-6h8" stroke="currentColor" stroke-width="2" stroke-linejoin="round" />
    <path v-else-if="id === 'praxis'" d="M24 14v20M14 24h20" stroke="currentColor" stroke-width="2" />
    <path v-else-if="id === 'fenster'" d="M14 14h20v20H14zM24 14v20M14 24h20" stroke="currentColor" stroke-width="2" />
    <path v-else-if="id === 'grund'" d="M16 30c6-10 10-10 16 0M18 20h12" stroke="currentColor" stroke-width="2" stroke-linecap="round" />
    <path v-else d="M16 18h16M16 24h16M16 30h10" stroke="currentColor" stroke-width="2" stroke-linecap="round" />
  </svg>
</template>
