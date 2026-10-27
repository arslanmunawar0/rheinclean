<script setup lang="ts">
import { computed } from "vue"
import { useRoute } from "vue-router"
import SiteFooter from "@/components/SiteFooter.vue"
import SiteHeader from "@/components/SiteHeader.vue"

const route = useRoute()
const admin = computed(() => route.path.startsWith("/admin"))
</script>

<template>
  <div class="min-h-screen bg-white font-sans text-ink">
    <a href="#inhalt" class="sr-only focus:not-sr-only focus:absolute focus:left-4 focus:top-4 focus:z-50 focus:bg-white focus:px-3 focus:py-2">Zum Inhalt</a>
    <SiteHeader v-if="!admin" />
    <RouterView />
    <SiteFooter v-if="!admin" />
  </div>
</template>
