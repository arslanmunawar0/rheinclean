<script setup lang="ts">
import HeroArt from "@/components/HeroArt.vue"

const highlights = [
  { title: "Büroreinigung", text: "Arbeitsplätze, Besprechungsräume und Sanitärbereiche in einem festen Rhythmus." },
  { title: "Treppenhäuser", text: "Eingänge und Gemeinschaftsflächen, damit das Haus gepflegt wirkt." },
  { title: "Grundreinigung", text: "Ein gründlicher Einsatz, wenn der laufende Unterhalt nicht ausreicht." },
]
const steps = [
  { title: "Anfrage", text: "Sie beschreiben Objekt und Wunsch. Das Formular ist noch kein Auftrag." },
  { title: "Abstimmung", text: "Wir klären Umfang, Zugang und Zeiten und melden uns schriftlich." },
  { title: "Durchführung", text: "Der Einsatz folgt der abgestimmten Leistung, nicht einer allgemeinen Versprechung." },
]
</script>

<template>
  <main id="inhalt">
    <section class="bg-mist">
      <div class="mx-auto grid max-w-6xl items-center gap-10 px-4 py-14 md:grid-cols-2 md:py-20">
        <div>
          <p class="text-sm font-semibold uppercase tracking-[0.14em] text-teal">Duisburg und Umgebung</p>
          <h1 class="mt-3 text-4xl font-bold leading-tight text-navy md:text-5xl">Sauberkeit, auf die Sie sich verlassen können.</h1>
          <p class="mt-5 text-lg leading-relaxed text-ink/80">RheinClean Gebäudeservice stellt auf dieser Demonstrationswebsite Reinigungsleistungen für Büros, Praxen und Treppenhäuser in Duisburg und nahe gelegenen Orten vor.</p>
          <div class="mt-8 flex flex-wrap gap-3">
            <RouterLink to="/angebot" class="rounded-full bg-teal px-5 py-3 font-semibold text-white hover:bg-teal-700">Kostenloses Angebot anfragen</RouterLink>
            <RouterLink to="/leistungen" class="rounded-full border border-navy px-5 py-3 font-semibold text-navy hover:bg-white">Unsere Leistungen</RouterLink>
          </div>
        </div>
        <HeroArt />
      </div>
    </section>

    <section class="mx-auto grid max-w-6xl gap-5 px-4 py-16 md:grid-cols-3">
      <article v-for="item in highlights" :key="item.title" class="rounded-2xl border border-line bg-white p-6 shadow-sm">
        <h2 class="text-xl font-bold text-navy">{{ item.title }}</h2>
        <p class="mt-3 leading-relaxed text-ink/80">{{ item.text }}</p>
      </article>
    </section>

    <section class="bg-navy text-white">
      <div class="mx-auto max-w-6xl px-4 py-16">
        <h2 class="text-3xl font-bold">So läuft eine Anfrage</h2>
        <ol class="mt-8 grid gap-6 md:grid-cols-3">
          <li v-for="(step, index) in steps" :key="step.title" class="rounded-2xl bg-white/10 p-6">
            <p class="text-sm font-semibold text-teal">0{{ index + 1 }}</p>
            <h3 class="mt-2 text-xl font-bold">{{ step.title }}</h3>
            <p class="mt-2 text-white/80">{{ step.text }}</p>
          </li>
        </ol>
      </div>
    </section>

    <section class="mx-auto grid max-w-6xl gap-10 px-4 py-16 md:grid-cols-2">
      <div>
        <h2 class="text-3xl font-bold text-navy">Worauf Sie sich verlassen können</h2>
        <p class="mt-4 leading-relaxed text-ink/80">Vor einem Einsatz werden Umfang, Zugang und Zeiten besprochen. Sie erhalten eine Rückmeldung auf Ihre Anfrage. Diese Website zeigt den Ablauf. Sie belegt keine echten Aufträge, Bewertungen oder Zertifikate.</p>
      </div>
      <div class="rounded-2xl bg-mist p-6">
        <h2 class="text-xl font-bold text-navy">Einsatzgebiet</h2>
        <p class="mt-3 leading-relaxed text-ink/80">Duisburg, und nach Absprache Oberhausen, Mülheim an der Ruhr sowie der Norden von Düsseldorf. Eine Ladenadresse wird hier bewusst nicht genannt, weil das Unternehmen fiktiv ist.</p>
      </div>
    </section>

    <section class="bg-mist">
      <div class="mx-auto flex max-w-6xl flex-col items-start gap-4 px-4 py-14 md:flex-row md:items-center md:justify-between">
        <div>
          <h2 class="text-3xl font-bold text-navy">Unverbindlich anfragen</h2>
          <p class="mt-2 text-ink/80">Schildern Sie Objekt und Wunsch. Wir melden uns mit einer Rückfrage, nicht mit einem automatischen Vertrag.</p>
        </div>
        <RouterLink to="/angebot" class="rounded-full bg-navy px-5 py-3 font-semibold text-white">Zum Formular</RouterLink>
      </div>
    </section>
  </main>
</template>
