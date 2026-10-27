<script setup lang="ts">
import { onMounted, ref } from "vue"
import { useRoute, useRouter } from "vue-router"
import { api, formatWhen } from "@/services/api"
import { PROPERTY_LABELS, STATUS_LABELS, type Enquiry, type Service } from "@/types"

const route = useRoute()
const router = useRouter()
const enquiry = ref<Enquiry | null>(null)
const services = ref<Service[]>([])
const status = ref("neu")
const error = ref("")
const notice = ref("")
const loading = ref(true)
const saving = ref(false)
const confirmDelete = ref(false)

const reference = String(route.params.reference)

onMounted(async () => {
  try {
    const [item, catalog] = await Promise.all([
      api<Enquiry>(`/api/v1/admin/quote-requests/${reference}`),
      api<{ items: Service[] }>("/api/v1/services"),
    ])
    enquiry.value = item
    status.value = item.status
    services.value = catalog.items
  } catch (caught) {
    error.value = caught instanceof Error ? caught.message : "Die Anfrage wurde nicht gefunden."
  } finally {
    loading.value = false
  }
})

function serviceName(id: string) {
  return services.value.find((item) => item.id === id)?.name ?? id
}

async function save() {
  if (!enquiry.value) return
  saving.value = true
  notice.value = ""
  error.value = ""
  try {
    enquiry.value = await api<Enquiry>(`/api/v1/admin/quote-requests/${reference}`, {
      method: "PATCH",
      body: JSON.stringify({ status: status.value }),
    })
    notice.value = "Status gespeichert."
  } catch (caught) {
    error.value = caught instanceof Error ? caught.message : "Der Status konnte nicht gespeichert werden."
  } finally {
    saving.value = false
  }
}

async function remove() {
  saving.value = true
  try {
    await api(`/api/v1/admin/quote-requests/${reference}`, { method: "DELETE" })
    await router.push("/admin")
  } catch (caught) {
    error.value = caught instanceof Error ? caught.message : "Die Anfrage konnte nicht gelöscht werden."
    saving.value = false
  }
}
</script>

<template>
  <main id="inhalt" class="min-h-screen bg-mist px-4 py-8">
    <div class="mx-auto max-w-3xl">
      <RouterLink to="/admin" class="text-sm font-semibold text-teal">Zurück zur Übersicht</RouterLink>
      <p v-if="loading" class="mt-6" role="status">Wird geladen …</p>
      <p v-else-if="error && !enquiry" class="mt-6 rounded-xl bg-red-50 p-4 text-red-900" role="alert">{{ error }}</p>
      <article v-else-if="enquiry" class="mt-6 rounded-2xl bg-white p-6 shadow-sm">
        <h1 class="text-3xl font-bold text-navy">{{ enquiry.reference }}</h1>
        <p class="mt-2 text-sm text-ink/70">Eingang {{ formatWhen(enquiry.created_at) }} · Aktualisiert {{ formatWhen(enquiry.updated_at) }}</p>
        <dl class="mt-6 grid gap-4 sm:grid-cols-2">
          <div><dt class="text-sm text-ink/60">Name</dt><dd class="font-semibold">{{ enquiry.name }}</dd></div>
          <div><dt class="text-sm text-ink/60">E-Mail</dt><dd class="font-semibold">{{ enquiry.email }}</dd></div>
          <div><dt class="text-sm text-ink/60">Telefon</dt><dd>{{ enquiry.telephone || "Keine Angabe" }}</dd></div>
          <div><dt class="text-sm text-ink/60">Firma</dt><dd>{{ enquiry.company || "Keine Angabe" }}</dd></div>
          <div><dt class="text-sm text-ink/60">Leistung</dt><dd>{{ serviceName(enquiry.service) }}</dd></div>
          <div><dt class="text-sm text-ink/60">Objekt</dt><dd>{{ enquiry.property_type ? PROPERTY_LABELS[enquiry.property_type] : "Keine Angabe" }}</dd></div>
          <div><dt class="text-sm text-ink/60">Fläche</dt><dd>{{ enquiry.area_sqm ? `${enquiry.area_sqm} m²` : "Keine Angabe" }}</dd></div>
          <div><dt class="text-sm text-ink/60">Wunschdatum</dt><dd>{{ enquiry.preferred_date || "Keine Angabe" }}</dd></div>
        </dl>
        <h2 class="mt-6 font-semibold text-navy">Nachricht</h2>
        <p class="mt-2 whitespace-pre-wrap leading-relaxed">{{ enquiry.message }}</p>
        <p class="mt-4 text-sm text-ink/60">Datenschutzhinweis bestätigt, Fassung {{ enquiry.privacy_version }}.</p>
        <form class="mt-6 flex flex-wrap items-end gap-3" @submit.prevent="save">
          <div>
            <label class="text-sm font-semibold" for="status">Status</label>
            <select id="status" v-model="status" class="mt-1 block rounded-lg border border-line px-3 py-2">
              <option v-for="(label, key) in STATUS_LABELS" :key="key" :value="key">{{ label }}</option>
            </select>
          </div>
          <button class="rounded-full bg-teal px-4 py-2 font-semibold text-white disabled:opacity-60" :disabled="saving">Speichern</button>
        </form>
        <p v-if="notice" class="mt-3 text-teal" role="status">{{ notice }}</p>
        <p v-if="error" class="mt-3 text-red-800" role="alert">{{ error }}</p>
        <div class="mt-8 border-t border-line pt-4">
          <button v-if="!confirmDelete" type="button" class="text-sm font-semibold text-red-800" @click="confirmDelete = true">Anfrage löschen</button>
          <div v-else class="rounded-xl bg-red-50 p-4">
            <p>Die personenbezogenen Angaben dieser Anfrage werden aus der lokalen Datenbank entfernt.</p>
            <div class="mt-3 flex gap-3">
              <button type="button" class="rounded-full bg-red-800 px-4 py-2 text-sm font-semibold text-white" :disabled="saving" @click="remove">Endgültig löschen</button>
              <button type="button" class="text-sm font-semibold" @click="confirmDelete = false">Abbrechen</button>
            </div>
          </div>
        </div>
      </article>
    </div>
  </main>
</template>
