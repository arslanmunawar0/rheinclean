export interface QuoteForm {
  name: string
  email: string
  telephone: string
  company: string
  service: string
  propertyType: string
  area: string
  preferredDate: string
  message: string
  privacyAccepted: boolean
}

const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/

function localToday(): string {
  const now = new Date()
  const month = String(now.getMonth() + 1).padStart(2, "0")
  const day = String(now.getDate()).padStart(2, "0")
  return `${now.getFullYear()}-${month}-${day}`
}

export function quoteErrors(form: QuoteForm): Record<string, string> {
  const errors: Record<string, string> = {}
  const name = form.name.trim()
  if (name.length < 2 || name.length > 80) errors.name = "Bitte geben Sie Ihren Namen mit 2 bis 80 Zeichen ein."
  if (!emailPattern.test(form.email.trim())) errors.email = "Bitte geben Sie eine gültige E-Mail-Adresse ein."
  if (form.telephone.trim().length > 30) errors.telephone = "Die Telefonnummer ist zu lang."
  if (!form.service) errors.service = "Bitte wählen Sie eine Leistung."
  if (form.area.trim()) {
    const area = Number(form.area)
    if (!Number.isInteger(area) || area < 1 || area > 100000) {
      errors.area = "Bitte geben Sie eine ganze Fläche zwischen 1 und 100.000 m² an."
    }
  }
  if (form.preferredDate && form.preferredDate < localToday()) {
    errors.preferredDate = "Das Wunschdatum darf nicht in der Vergangenheit liegen."
  }
  if (form.message.trim().length < 10) errors.message = "Beschreiben Sie Ihr Anliegen in mindestens 10 Zeichen."
  if (form.message.trim().length > 2000) errors.message = "Die Nachricht darf höchstens 2.000 Zeichen haben."
  if (!form.privacyAccepted) errors.privacyAccepted = "Bitte bestätigen Sie den Hinweis zum Datenschutz."
  return errors
}
