import { describe, expect, it } from "vitest"
import { adminRedirect } from "./guard"

describe("admin routes", () => {
  it("sends anonymous visitors to the login page", () => {
    expect(adminRedirect("/admin", false)).toBe("/admin/login")
    expect(adminRedirect("/admin/anfragen/RC-1", false)).toBe("/admin/login")
  })

  it("leaves the public site and a signed-in dashboard alone", () => {
    expect(adminRedirect("/", false)).toBeNull()
    expect(adminRedirect("/admin", true)).toBeNull()
    expect(adminRedirect("/admin/login", true)).toBe("/admin")
  })
})
