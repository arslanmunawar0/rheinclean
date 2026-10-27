export interface Service {
  id: string
  name: string
  summary: string
  tasks: string[]
}

export interface QuotePayload {
  name: string
  email: string
  telephone: string | null
  company: string | null
  service: string
  property_type: string | null
  area_sqm: number | null
  preferred_date: string | null
  message: string
  privacy_accepted: boolean
}

export interface Enquiry {
  reference: string
  name: string
  email: string
  telephone: string | null
  company: string | null
  service: string
  property_type: string | null
  area_sqm: number | null
  preferred_date: string | null
  message: string
  privacy_version: string
  status: string
  created_at: string
  updated_at: string
}

export interface EnquiryPage {
  items: Enquiry[]
  total: number
  page: number
  page_size: number
}

export interface Stats {
  total: number
  neu: number
  in_progress: number
  completed: number
}

export const STATUS_LABELS: Record<string, string> = {
  neu: "Neu",
  kontaktiert: "Kontaktiert",
  angebot_erstellt: "Angebot erstellt",
  abgeschlossen: "Abgeschlossen",
  abgelehnt: "Abgelehnt",
}

export const PROPERTY_LABELS: Record<string, string> = {
  buero: "Büro",
  praxis: "Praxis",
  treppenhaus: "Treppenhaus",
  wohnung: "Wohnung",
  sonstiges: "Sonstiges",
}
