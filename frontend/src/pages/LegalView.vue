<script setup lang="ts">
defineProps<{ kind: "impressum" | "datenschutz" }>()
</script>

<template>
  <main id="inhalt" class="mx-auto max-w-3xl px-4 py-14">
    <p class="rounded-xl border border-amber-300 bg-amber-50 p-4 text-amber-950" role="note">Platzhalter für die Entwicklung. Vor einer öffentlichen Website müssen diese Angaben rechtlich geprüft und mit echten Pflichtangaben ersetzt werden. Hier stehen absichtlich keine Adresse, keine Steuernummer und keine Registernummer.</p>
    <template v-if="kind === 'impressum'">
      <h1 class="mt-8 text-4xl font-bold text-navy">Impressum</h1>
      <p class="mt-4 leading-relaxed">Anbieter dieser Demonstration: RheinClean Gebäudeservice, fiktiv. Verantwortlich für den Demo-Inhalt ist die Person, die das Projekt betreibt. Eine ladungsfähige Anschrift wird nicht erfunden.</p>
    </template>
    <template v-else>
      <h1 class="mt-8 text-4xl font-bold text-navy">Datenschutzerklärung</h1>
      <p class="mt-4 leading-relaxed">Das Formular speichert Name, E-Mail, die Nachricht und die optionalen Angaben lokal in einer SQLite-Datei, damit die Demo die Anfrage anzeigen kann. Es gibt kein Analyse-Werkzeug und keine Weitergabe an Werbenetze. Vor einem echten Betrieb braucht diese Erklärung eine Prüfung nach DSGVO, einschließlich Rechtsgrundlage, Speicherdauer und Betroffenenrechte.</p>
      <p class="mt-4 leading-relaxed">Gespeicherte Anfragen können in der Verwaltung gelöscht werden. Ein zusätzlicher Befehl entfernt Einträge, die älter sind als eine selbst gewählte Frist. Eine gesetzliche Frist wird hier nicht behauptet.</p>
    </template>
  </main>
</template>
