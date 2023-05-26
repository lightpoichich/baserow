import {
  defineNuxtModule,
  addPlugin,
  addServerHandler,
  extendViteConfig,
  addComponent,
  extendPages,
  addLayout,
  createResolver,
  addRouteMiddleware,
  addTemplate,
} from "@nuxt/kit";
import { routes } from "./routes";
import { defu } from "defu";
import pathe from "pathe";

import en from "./locales/en.json";
import fr from "./locales/fr.json";
import nl from "./locales/nl.json";
import de from "./locales/de.json";
import es from "./locales/es.json";
import it from "./locales/it.json";
import pl from "./locales/pl.json";

export default defineNuxtModule({
  meta: {
    // Usually the npm package name of your module
    name: "@baserow/core",
    // The key in `nuxt.config` that holds your module options
    configKey: "core",
    // Compatibility constraints
    compatibility: {
      // Semver version of supported nuxt versions
      nuxt: "^3.0.0",
    },
  },
  // Default configuration options for your module, can also be a function returning those
  defaults: {},
  // Shorthand sugar to register Nuxt hooks
  hooks: {},
  // The function holding your module logic, it can be asynchronous
  setup(moduleOptions, nuxt) {
    const { resolve } = createResolver(import.meta.url);

    addLayout(
      {
        write: true,
        src: pathe.resolve(__dirname, "./layouts/app.vue"),
        filename: "app.vue",
      },
      "app"
    );

    addLayout(
      {
        write: true,
        src: pathe.resolve(__dirname, "./layouts/login.vue"),
        filename: "login.vue",
      },
      "login"
    );

    // Add routes
    extendPages((pages) => {
      pages.push(...routes);
    });

    // Env vars
    nuxt.options.runtimeConfig.public = defu(
      nuxt.options.runtimeConfig.public,
      {
        baserowPublicUrl: "http://localhost",
        downloadFileViaXhr: false,
        privateBackendUrl: "http://backend:8000",
        baserowDisablePublicUrlCheck: false,
        publicBackendUrl: "http://localhost:8000",
        publicWebFrontendUrl: "http://localhost:3000",
        initialTableDataLimit: null,
        baserowDisablePublicUrlCheck: false,
        initalTableDataLimit: null,
        hoursUntilTrashPermanentlyDeleted: 24 * 3,
        disableAnonymousPublicViewWsConnections: false,
        baserowMaxImportFileSizeMb: 512,
        featureFlags: "",
        baserowDisableGoogleDocsFilePreview: "",
        baserowMaxSnapshotsPerGroup: -1,
        baserowFrontendJobsPollingTimeoutMs: 2000,
      }
    );

    // i18n:registerModule module didnt work properly, had to
    nuxt.hook(
      "i18n:extend-messages",
      async (additionalMessages, localeCodes) => {
        additionalMessages.push({
          en,
          fr,
          nl,
          de,
          es,
          it,
          pl,
        });
      }
    );

    // Load public assets (images and fonts)
    nuxt.hook("nitro:config", async (nitroConfig) => {
      nitroConfig.publicAssets ||= [];
      nitroConfig.publicAssets.push({
        baseURL: "@baserow/modules/core/static",
        dir: resolve("static"),
      });
    });

    // Load vuex store
    addPlugin(resolve("./plugins/store"));

    // Load the client handler plugin. `append` is set to true to make sure
    // it's loaded after the store plugin (as client handler depends on it)
    addPlugin(resolve("./plugins/clientHandler"), { append: true });
    addPlugin(resolve("./plugin"), { append: true });

    addRouteMiddleware({
      name: "authentication",
      path: resolve("./middleware/authentication"),
      global: true, // make sure the middleware is added to every route
    });

    addRouteMiddleware({
      name: "settings",
      path: resolve("./middleware/settings"),
    });

    addRouteMiddleware({
      name: "urlCheck",
      path: resolve("./middleware/urlCheck"),
    });

    // Add the main scss file which contains all the generic scss code.
    nuxt.options.css.push(resolve("./assets/scss/default.scss"));
  },
});
