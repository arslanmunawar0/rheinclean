<script setup lang="ts">
import { computed, onMounted, reactive, ref } from "vue"
import { useRoute } from "vue-router"
import { api } from "@/services/api"
import type { Service } from "@/types"
import { quoteErrors, type QuoteForm } from "@/validation"

const route = useRoute()
const services = ref<Service[]>([])
const loadError = ref("")
const loadingServices = ref(true)
const submitting = ref(false)
const submitError = ref("")
const reference = ref("")
const errors = ref<Record<string, string>>({})

const form = reactive<QuoteForm>({
  name: "",
  email: "",
  telephone: "",
  company: "",
  service: typeof route.query.leistung === "string" ? route.query.leistung : "",
  propertyType: "",
  area: "",
  preferredDate: "",
  message: "",
  privacyAccepted: false,
})

const properties = [
  { id: "", label: "Keine Angabe" },
  { id: "buero", label: "Büro" },
  { id: "praxis", label: "Praxis" },
  { id: "treppenhaus", label: "Treppenhaus" },
  { id: "wohnung", label: "Wohnung" },
  { id: "sonstiges", label: "Sonstiges" },
]

const fieldClass = computed(() => (name: string) =>
  `mt-1 w-full rounded-lg border px-3 py-2 ${errors.value[name] ? "border-red-700" : "border-line"}`)

onMounted(async () => {
  try {
    services.value = (await api<{ items: Service[] }>("/api/v1/services")).items
    if (!services.value.some((item) => item.id === form.service)) form.service = ""
  } catch (caught) {
    loadError.value = caught instanceof Error ? caught.message : "Die Leistungen sind nicht erreichbar."
  } finally {
    loadingServices.value = false
  }
})

async function submit() {
  if (submitting.value || reference.value) return
  errors.value = quoteErrors(form)
  submitError.value = ""
  if (Object.keys(errors.value).length) return
  submitting.value = true
  try {
    const body = await api<{ reference: string }>("/api/v1/quote-requests", {
      method: "POST",
      body: JSON.stringify({
        name: form.name.trim(),
        email: form.email.trim(),
        telephone: form.telephone.trim() || null,
        company: form.company.trim() || null,
        service: form.service,
        property_type: form.propertyType || null,
        area_sqm: form.area.trim() ? Number(form.area) : null,
        preferred_date: form.preferredDate || null,
        message: form.message.trim(),
        privacy_accepted: form.privacyAccepted,
      }),
    })
    reference.value = body.reference
  } catch (caught) {
    submitError.value = caught instanceof Error ? caught.message : "Die Anfrage konnte nicht gesendet werden."
  } finally {
    submitting.value = false
  }
}
</script>

<template>
  <main id="inhalt" class="mx-auto max-w-3xl px-4 py-14">
    <h1 class="text-4xl font-bold text-navy">Kostenloses Angebot anfragen</h1>
    <p class="mt-4 leading-relaxed text-ink/80">Das Formular speichert Ihre Angaben für die Rückmeldung. Mit dem Absenden entsteht kein Auftrag.</p>

    <p v-if="reference" class="mt-8 rounded-2xl bg-mist p-6" role="status">
      <span class="block font-semibold text-navy">Anfrage eingegangen.</span>
      Ihre Referenznummer lautet <strong>{{ reference }}</strong>. Bitte notieren Sie sie für Rückfragen.
    </p>

    <form v-else class="mt-8 space-y-5" novalidate @submit.prevent="submit">
      <p v-if="loadError" class="rounded-xl bg-red-50 p-4 text-red-900" role="alert">{{ loadError }}</p>
      <p v-if="submitError" class="rounded-xl bg-red-50 p-4 text-red-900" role="alert">{{ submitError }}</p>

      <div>
        <label class="font-semibold" for="name">Name</label>
        <input id="name" v-model="form.name" autocomplete="name" required :class="fieldClass('name')" />
        <p v-if="errors.name" class="mt-1 text-sm text-red-800">{{ errors.name }}</p>
      </div>
      <div>
        <label class="font-semibold" for="email">E-Mail</label>
        <input id="email" v-model="form.email" type="email" autocomplete="email" required :class="fieldClass('email')" />
        <p v-if="errors.email" class="mt-1 text-sm text-red-800">{{ errors.email }}</p>
      </div>
      <div class="grid gap-5 md:grid-cols-2">
        <div>
          <label class="font-semibold" for="telephone">Telefon, optional</label>
          <input id="telephone" v-model="form.telephone" type="tel" autocomplete="tel" :class="fieldClass('telephone')" />
          <p v-if="errors.telephone" class="mt-1 text-sm text-red-800">{{ errors.telephone }}</p>
        </div>
        <div>
          <label class="font-semibold" for="company">Firma, optional</label>
          <input id="company" v-model="form.company" autocomplete="organization" class="mt-1 w-full rounded-lg border border-line px-3 py-2" />
        </div>
      </div>
      <div>
        <label class="font-semibold" for="service">Leistung</label>
        <select id="service" v-model="form.service" required :disabled="loadingServices" :class="fieldClass('service')">
          <option value="">Bitte wählen</option>
          <option v-for="service in services" :key="service.id" :value="service.id">{{ service.name }}</option>
        </select>
        <p v-if="errors.service" class="mt-1 text-sm text-red-800">{{ errors.service }}</p>
      </div>
      <div class="grid gap-5 md:grid-cols-2">
        <div>
          <label class="font-semibold" for="property">Objektart, optional</label>
          <select id="property" v-model="form.propertyType" class="mt-1 w-full rounded-lg border border-line px-3 py-2">
            <option v-for="item in properties" :key="item.id" :value="item.id">{{ item.label }}</option>
          </select>
        </div>
        <div>
          <label class="font-semibold" for="area">Fläche in m², optional</label>
          <input id="area" v-model="form.area" inputmode="numeric" :class="fieldClass('area')" />
          <p v-if="errors.area" class="mt-1 text-sm text-red-800">{{ errors.area }}</p>
        </div>
      </div>
      <div>
        <label class="font-semibold" for="date">Wunschdatum, optional</label>
        <input id="date" v-model="form.preferredDate" type="date" :class="fieldClass('preferredDate')" />
        <p v-if="errors.preferredDate" class="mt-1 text-sm text-red-800">{{ errors.preferredDate }}</p>
      </div>
      <div>
        <label class="font-semibold" for="message">Nachricht</label>
        <textarea id="message" v-model="form.message" rows="5" required :class="fieldClass('message')"></textarea>
        <p v-if="errors.message" class="mt-1 text-sm text-red-800">{{ errors.message }}</p>
      </div>
      <div>
        <label class="flex items-start gap-3" for="privacy">
          <input id="privacy" v-model="form.privacyAccepted" type="checkbox" class="mt-1" />
          <span>Ich habe gelesen, dass die Angaben nur für die Bearbeitung dieser Anfrage in der lokalen Demo gespeichert werden. <RouterLink to="/datenschutz" class="font-semibold text-teal">Datenschutzhinweis</RouterLink></span>
        </label>
        <p v-if="errors.privacyAccepted" class="mt-1 text-sm text-red-800">{{ errors.privacyAccepted }}</p>
      </div>
      <button type="submit" class="rounded-full bg-teal px-5 py-3 font-semibold text-white disabled:opacity-60" :disabled="submitting || loadingServices">
        {{ submitting ? "Wird gesendet …" : "Anfrage senden" }}
      </button>
    </form>
  </main>
</template>
