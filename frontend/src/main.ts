import "@fontsource/source-sans-3/400.css"
import "@fontsource/source-sans-3/600.css"
import "@fontsource/source-sans-3/700.css"
import { createApp } from "vue"
import App from "./App.vue"
import { router } from "./router"
import "./style.css"

createApp(App).use(router).mount("#app")
