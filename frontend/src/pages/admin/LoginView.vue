<script setup lang="ts">
import { ref } from "vue"
import { useRouter } from "vue-router"
import { api } from "@/services/api"

const router = useRouter()
const email = ref("")
const password = ref("")
const error = ref("")
const loading = ref(false)

async function submit() {
  error.value = ""
  if (!email.value.includes("@") || password.value.length < 1) {
    error.value = "Bitte geben Sie E-Mail und Passwort ein."
    return
  }
  loading.value = true
  try {
    await api("/api/v1/admin/login", { method: "POST", body: JSON.stringify({ email: email.value, password: password.value }) })
    await router.push("/admin")
  } catch (caught) {
    error.value = caught instanceof Error && caught.message.includes("nicht erreichbar") ? caught.message : "Anmeldung fehlgeschlagen."
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <main id="inhalt" class="mx-auto flex min-h-screen max-w-md flex-col justify-center px-4 py-16">
    <p class="text-sm font-semibold uppercase tracking-[0.14em] text-teal">Verwaltung</p>
    <h1 class="mt-2 text-3xl font-bold text-navy">Anmelden</h1>
    <p class="mt-3 text-sm text-ink/70">Nur für das vorab angelegte Demonstrationskonto. Eine Registrierung gibt es nicht.</p>
    <form class="mt-8 space-y-4" @submit.prevent="submit">
      <p v-if="error" class="rounded-xl bg-red-50 p-3 text-red-900" role="alert">{{ error }}</p>
      <div>
        <label class="font-semibold" for="admin-email">E-Mail</label>
        <input id="admin-email" v-model="email" type="email" autocomplete="username" required class="mt-1 w-full rounded-lg border border-line px-3 py-2" />
      </div>
      <div>
        <label class="font-semibold" for="admin-password">Passwort</label>
        <input id="admin-password" v-model="password" type="password" autocomplete="current-password" required class="mt-1 w-full rounded-lg border border-line px-3 py-2" />
      </div>
      <button class="w-full rounded-full bg-navy py-3 font-semibold text-white disabled:opacity-60" :disabled="loading">{{ loading ? "Wird geprüft …" : "Anmelden" }}</button>
    </form>
  </main>
</template>
