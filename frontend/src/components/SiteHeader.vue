<script setup lang="ts">
import { ref } from "vue"

const open = ref(false)
const links = [
  { to: "/leistungen", label: "Leistungen" },
  { to: "/ueber-uns", label: "Über uns" },
  { to: "/angebot", label: "Angebot" },
]
</script>

<template>
  <header class="sticky top-0 z-40 border-b border-line bg-white/95 backdrop-blur">
    <div class="mx-auto flex max-w-6xl items-center justify-between gap-4 px-4 py-3">
      <RouterLink to="/" class="leading-tight" @click="open = false">
        <span class="block text-lg font-bold tracking-tight text-navy">RheinClean</span>
        <span class="block text-xs uppercase tracking-[0.16em] text-teal">Gebäudeservice</span>
      </RouterLink>
      <nav class="hidden items-center gap-6 md:flex" aria-label="Hauptnavigation">
        <RouterLink v-for="link in links" :key="link.to" :to="link.to" class="text-sm font-semibold text-navy hover:text-teal">{{ link.label }}</RouterLink>
        <RouterLink to="/angebot" class="rounded-full bg-teal px-4 py-2 text-sm font-semibold text-white hover:bg-teal-700">Kostenloses Angebot</RouterLink>
      </nav>
      <button class="rounded-md border border-line px-3 py-2 text-sm font-semibold text-navy md:hidden" type="button" :aria-expanded="open" aria-controls="mobilenav" @click="open = !open">Menü</button>
    </div>
    <nav v-if="open" id="mobilenav" class="space-y-2 border-t border-line px-4 py-3 md:hidden" aria-label="Mobilnavigation">
      <RouterLink v-for="link in links" :key="link.to" :to="link.to" class="block py-2 font-semibold text-navy" @click="open = false">{{ link.label }}</RouterLink>
      <RouterLink to="/angebot" class="block py-2 font-semibold text-teal" @click="open = false">Kostenloses Angebot</RouterLink>
    </nav>
  </header>
</template>
