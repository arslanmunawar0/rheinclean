let csrfToken = ""

interface ApiError extends Error {
  status: number
}

function failure(status: number, detail: string): ApiError {
  const error = new Error(detail) as ApiError
  error.status = status
  return error
}

async function readError(response: Response): Promise<string> {
  try {
    const body = await response.json()
    if (Array.isArray(body.errors) && body.errors.length > 0) {
      const messages = body.errors
        .map((item: { message?: string }) => item.message)
        .filter((message: string | undefined): message is string => Boolean(message))
      if (messages.length) return messages.join(" ")
    }
    if (typeof body.detail === "string") return body.detail
  } catch {
    return "Die Anfrage konnte nicht verarbeitet werden."
  }
  return "Die Anfrage konnte nicht verarbeitet werden."
}

export async function api<T>(path: string, options: RequestInit = {}, retry = true): Promise<T> {
  const method = (options.method ?? "GET").toUpperCase()
  const headers = new Headers(options.headers)
  if (options.body && !headers.has("Content-Type")) headers.set("Content-Type", "application/json")
  if (method !== "GET") {
    if (!csrfToken) await refreshSession()
    headers.set("X-CSRF-Token", csrfToken)
  }
  let response: Response
  try {
    response = await fetch(path, { ...options, method, headers, credentials: "include" })
  } catch {
    throw failure(0, "Der Server ist nicht erreichbar. Bitte starten Sie die API und versuchen Sie es erneut.")
  }
  if (response.status === 403 && method !== "GET" && retry) {
    csrfToken = ""
    await refreshSession()
    return api<T>(path, options, false)
  }
  if (response.status === 204) return undefined as T
  if (!response.ok) throw failure(response.status, await readError(response))
  const body = await response.json()
  if (body && typeof body.csrf_token === "string") csrfToken = body.csrf_token
  return body as T
}

export function resetCsrf(): void {
  csrfToken = ""
}

export async function refreshSession(): Promise<{ authenticated: boolean; csrf_token: string }> {
  const response = await fetch("/api/v1/admin/session", { credentials: "include" })
  if (!response.ok) throw failure(response.status, "Die Sitzung konnte nicht geprüft werden.")
  const body = await response.json()
  csrfToken = body.csrf_token
  return body
}

export function formatWhen(value: string): string {
  return new Intl.DateTimeFormat("de-DE", {
    dateStyle: "medium",
    timeStyle: "short",
    timeZone: "Europe/Berlin",
  }).format(new Date(value))
}
