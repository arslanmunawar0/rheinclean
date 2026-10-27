import { describe, expect, it } from "vitest"
import { quoteErrors, type QuoteForm } from "./validation"

function form(overrides: Partial<QuoteForm> = {}): QuoteForm {
  return {
    name: "Anna Beispiel",
    email: "anna@example.com",
    telephone: "",
    company: "",
    service: "buero",
    propertyType: "",
    area: "",
    preferredDate: "",
    message: "Bitte um ein Angebot für die wöchentliche Reinigung.",
    privacyAccepted: true,
    ...overrides,
  }
}

describe("quote form", () => {
  it("accepts a complete request", () => {
    expect(quoteErrors(form())).toEqual({})
  })

  it("requires a valid email, a service and the privacy notice", () => {
    const errors = quoteErrors(form({ email: "anna", service: "", privacyAccepted: false, message: "kurz" }))
    expect(errors.email).toBeTruthy()
    expect(errors.service).toBeTruthy()
    expect(errors.privacyAccepted).toBeTruthy()
    expect(errors.message).toBeTruthy()
  })

  it("rejects an area outside the allowed range", () => {
    expect(quoteErrors(form({ area: "0" })).area).toBeTruthy()
  })

  it("rejects a preferred date in the past", () => {
    expect(quoteErrors(form({ preferredDate: "2000-01-01" })).preferredDate).toBeTruthy()
  })
})
