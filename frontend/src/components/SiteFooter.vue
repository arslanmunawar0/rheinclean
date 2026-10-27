<template>
  <footer class="bg-navy text-white">
    <div class="mx-auto grid max-w-6xl gap-8 px-4 py-12 md:grid-cols-3">
      <div>
        <p class="text-lg font-bold">RheinClean Gebäudeservice</p>
        <p class="mt-2 text-sm text-white/80">Fiktives Demonstrationsunternehmen. Keine echte Firma, keine echten Kunden.</p>
      </div>
      <div>
        <p class="text-sm font-semibold uppercase tracking-wide text-white/70">Navigation</p>
        <ul class="mt-3 space-y-2 text-sm">
          <li><RouterLink to="/leistungen">Leistungen</RouterLink></li>
          <li><RouterLink to="/ueber-uns">Über uns</RouterLink></li>
          <li><RouterLink to="/angebot">Angebot anfragen</RouterLink></li>
        </ul>
      </div>
      <div>
        <p class="text-sm font-semibold uppercase tracking-wide text-white/70">Kontakt, Platzhalter</p>
        <p class="mt-3 text-sm text-white/80">E-Mail: kontakt@rheinclean.example</p>
        <p class="text-sm text-white/80">Telefon: wird vor einem echten Einsatz ergänzt</p>
        <p class="mt-3 text-sm"><RouterLink to="/impressum">Impressum</RouterLink> · <RouterLink to="/datenschutz">Datenschutz</RouterLink></p>
      </div>
    </div>
  </footer>
</template>
