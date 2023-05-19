// https://nuxt.com/docs/api/configuration/nuxt-config

// const modules = ["@/modules/core/module.js"];
// const modules = baseModules.concat([""]);
const locales = [
    { code: "en", name: "English", file: "en.json" },
    { code: "fr", name: "Français", file: "fr.json" },
    { code: "nl", name: "Nederlands", file: "nl.json" },
    { code: "de", name: "Deutsch", file: "de.json" },
    { code: "es", name: "Español", file: "es.json" },
    { code: "it", name: "Italiano", file: "it.json" },
    { code: "pl", name: "Polski (Beta)", file: "pl.json" },
];

export default defineNuxtConfig({
    alias: {
        "@baserow": "./",
    },
    css: [],
    modules: ["@/modules/core/module.js", "@nuxtjs/i18n"],
    i18n: {
        strategy: "no_prefix",
        defaultLocale: "en",
        detectBrowserLanguage: {
            useCookie: true,
            cookieKey: "i18n-language",
        },
        langDir: "./locales",
        locales,
        trailingSlash: true,
    },
});
