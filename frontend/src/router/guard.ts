export function adminRedirect(path: string, authenticated: boolean): string | null {
  const login = "/admin/login"
  if (path.startsWith("/admin") && path !== login && !authenticated) return login
  if (path === login && authenticated) return "/admin"
  return null
}
