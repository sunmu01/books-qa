import { createApp } from "vue";
import "./style.css";
import "virtual:windi.css";
import "virtual:windi-devtools";
import App from "./App.vue";
import { createRouter, createWebHistory } from "vue-router";

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: "/", component: () => import("./views/QA.vue") },
    { path: "/up", component: () => import("./views/UP.vue") },
  ],
});

const app = createApp(App);

app.use(router);

app.mount("#app");
