<script setup lang="ts">
import { computed, onMounted, ref, watch } from "vue"
import { useRouter } from "vue-router"
import { api, formatWhen, resetCsrf } from "@/services/api"
import { STATUS_LABELS, type EnquiryPage, type Stats } from "@/types"

const router = useRouter()
const stats = ref<Stats | null>(null)
const page = ref<EnquiryPage | null>(null)
const query = ref("")
const status = ref("")
const currentPage = ref(1)
const error = ref("")
const loading = ref(true)

const cards = computed(() => stats.value ? [
  { label: "Anfragen gesamt", value: stats.value.total },
  { label: "Neu", value: stats.value.neu },
  { label: "In Bearbeitung", value: stats.value.in_progress },
  { label: "Abgeschlossen", value: stats.value.completed },
] : [])

const pages = computed(() => page.value ? Math.max(1, Math.ceil(page.value.total / page.value.page_size)) : 1)

async function load() {
  loading.value = true
  error.value = ""
  try {
    const params = new URLSearchParams({ page: String(currentPage.value), page_size: "8" })
    if (status.value) params.set("status", status.value)
    if (query.value.trim()) params.set("q", query.value.trim())
    const [nextStats, nextPage] = await Promise.all([
      api<Stats>("/api/v1/admin/stats"),
      api<EnquiryPage>(`/api/v1/admin/quote-requests?${params}`),
    ])
    stats.value = nextStats
    page.value = nextPage
  } catch (caught) {
    error.value = caught instanceof Error ? caught.message : "Die Übersicht konnte nicht geladen werden."
  } finally {
    loading.value = false
  }
}

async function logout() {
  await api("/api/v1/admin/logout", { method: "POST" })
  resetCsrf()
  await router.push("/admin/login")
}

watch([status, currentPage], load)
onMounted(load)

function search() {
  currentPage.value = 1
  load()
}
</script>

<template>
  <main id="inhalt" class="min-h-screen bg-mist">
    <header class="border-b border-line bg-white">
      <div class="mx-auto flex max-w-6xl items-center justify-between px-4 py-4">
        <p class="font-bold text-navy">RheinClean Verwaltung</p>
        <button type="button" class="text-sm font-semibold text-teal" @click="logout">Abmelden</button>
      </div>
    </header>
    <div class="mx-auto max-w-6xl px-4 py-8">
      <h1 class="text-3xl font-bold text-navy">Anfragen</h1>
      <p v-if="error" class="mt-4 rounded-xl bg-red-50 p-4 text-red-900" role="alert">{{ error }}</p>
      <p v-else-if="loading" class="mt-4" role="status">Wird geladen …</p>
      <template v-else>
        <div class="mt-6 grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
          <article v-for="card in cards" :key="card.label" class="rounded-2xl bg-white p-5 shadow-sm">
            <p class="text-sm text-ink/70">{{ card.label }}</p>
            <p class="mt-2 text-3xl font-bold text-navy">{{ card.value }}</p>
          </article>
        </div>
        <form class="mt-8 flex flex-wrap gap-3" @submit.prevent="search">
          <label class="sr-only" for="search">Suche</label>
          <input id="search" v-model="query" placeholder="Referenz oder Name" class="rounded-lg border border-line px-3 py-2" />
          <label class="sr-only" for="status">Status</label>
          <select id="status" v-model="status" class="rounded-lg border border-line px-3 py-2" @change="currentPage = 1">
            <option value="">Alle Status</option>
            <option v-for="(label, key) in STATUS_LABELS" :key="key" :value="key">{{ label }}</option>
          </select>
          <button class="rounded-full bg-navy px-4 py-2 text-sm font-semibold text-white">Suchen</button>
        </form>
        <p v-if="page && page.total === 0" class="mt-6 rounded-xl bg-white p-6">Keine Anfragen für diese Auswahl.</p>
        <div v-else class="mt-6 overflow-x-auto rounded-2xl bg-white shadow-sm">
          <table class="min-w-full text-left text-sm">
            <thead class="bg-navy text-white">
              <tr>
                <th class="px-4 py-3 font-semibold">Referenz</th>
                <th class="px-4 py-3 font-semibold">Name</th>
                <th class="px-4 py-3 font-semibold">Status</th>
                <th class="px-4 py-3 font-semibold">Eingang</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="item in page?.items" :key="item.reference" class="border-t border-line">
                <td class="px-4 py-3"><RouterLink class="font-semibold text-teal" :to="`/admin/anfragen/${item.reference}`">{{ item.reference }}</RouterLink></td>
                <td class="px-4 py-3">{{ item.name }}</td>
                <td class="px-4 py-3">{{ STATUS_LABELS[item.status] }}</td>
                <td class="px-4 py-3">{{ formatWhen(item.created_at) }}</td>
              </tr>
            </tbody>
          </table>
        </div>
        <div v-if="page && pages > 1" class="mt-4 flex gap-3">
          <button type="button" class="rounded-full border border-line px-4 py-2 disabled:opacity-40" :disabled="currentPage === 1" @click="currentPage--">Zurück</button>
          <button type="button" class="rounded-full border border-line px-4 py-2 disabled:opacity-40" :disabled="currentPage === pages" @click="currentPage++">Weiter</button>
        </div>
      </template>
    </div>
  </main>
</template>
