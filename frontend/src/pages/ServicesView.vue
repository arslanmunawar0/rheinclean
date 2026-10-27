<script setup lang="ts">
import { onMounted, ref } from "vue"
import ServiceMark from "@/components/ServiceMark.vue"
import { api } from "@/services/api"
import type { Service } from "@/types"

const services = ref<Service[]>([])
const error = ref("")
const loading = ref(true)

onMounted(async () => {
  try {
    const body = await api<{ items: Service[] }>("/api/v1/services")
    services.value = body.items
  } catch (caught) {
    error.value = caught instanceof Error ? caught.message : "Die Leistungen konnten nicht geladen werden."
  } finally {
    loading.value = false
  }
})
</script>

<template>
  <main id="inhalt" class="mx-auto max-w-6xl px-4 py-14">
    <h1 class="text-4xl font-bold text-navy">Leistungen</h1>
    <p class="mt-4 max-w-3xl text-lg text-ink/80">Die Karten beschreiben typische Arbeiten. Festpreise stehen hier nicht, weil der Aufwand vom Objekt abhängt.</p>
    <p v-if="loading" class="mt-8" role="status">Leistungen werden geladen …</p>
    <p v-else-if="error" class="mt-8 rounded-xl bg-red-50 p-4 text-red-900" role="alert">{{ error }}</p>
    <div v-else class="mt-10 grid gap-5 md:grid-cols-2">
      <article v-for="service in services" :key="service.id" class="flex flex-col rounded-2xl border border-line p-6 shadow-sm">
        <ServiceMark :id="service.id" />
        <h2 class="mt-4 text-2xl font-bold text-navy">{{ service.name }}</h2>
        <p class="mt-3 text-ink/80">{{ service.summary }}</p>
        <ul class="mt-4 list-disc space-y-1 pl-5 text-ink/80">
          <li v-for="task in service.tasks" :key="task">{{ task }}</li>
        </ul>
        <RouterLink :to="`/angebot?leistung=${service.id}`" class="mt-6 inline-flex font-semibold text-teal hover:text-teal-700">Diese Leistung anfragen</RouterLink>
      </article>
    </div>
  </main>
</template>
