import { createRouter, createWebHistory } from "vue-router"
import { adminRedirect } from "./guard"
import { refreshSession } from "@/services/api"

export const router = createRouter({
  history: createWebHistory(),
  scrollBehavior: () => ({ top: 0 }),
  routes: [
    { path: "/", component: () => import("@/pages/HomeView.vue") },
    { path: "/leistungen", component: () => import("@/pages/ServicesView.vue") },
    { path: "/ueber-uns", component: () => import("@/pages/AboutView.vue") },
    { path: "/angebot", component: () => import("@/pages/QuoteView.vue") },
    { path: "/impressum", component: () => import("@/pages/LegalView.vue"), props: { kind: "impressum" } },
    { path: "/datenschutz", component: () => import("@/pages/LegalView.vue"), props: { kind: "datenschutz" } },
    { path: "/admin/login", component: () => import("@/pages/admin/LoginView.vue") },
    { path: "/admin", component: () => import("@/pages/admin/DashboardView.vue") },
    { path: "/admin/anfragen/:reference", component: () => import("@/pages/admin/EnquiryView.vue") },
    { path: "/:pathMatch(.*)*", component: () => import("@/pages/NotFoundView.vue") },
  ],
})

router.beforeEach(async (to) => {
  if (!to.path.startsWith("/admin")) return true
  try {
    const session = await refreshSession()
    const redirect = adminRedirect(to.path, session.authenticated)
    return redirect ?? true
  } catch {
    if (to.path !== "/admin/login") return "/admin/login"
    return true
  }
})
