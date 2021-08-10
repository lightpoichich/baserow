export default function (base = '@') {
  // Support adding in extra modules say from a plugin using the ADDITIONAL_MODULES
  // env variable which is a comma separated list of absolute module paths.
  const additionalModulesCsv = process.env.ADDITIONAL_MODULES
  const additionalModules = additionalModulesCsv
    ? additionalModulesCsv.split(',')
    : []

  const baseModules = [
    [
      '@nuxtjs/i18n',
      {
        vueI18nLoader: true,
        strategy: 'no_prefix',
        defaultLocale: 'en',
        detectBrowserLanguage: {
          useCookie: true,
          cookieKey: 'i18n-language',
        },
        locales: [
          { code: 'fr', name: 'Français', file: 'fr.js' },
          { code: 'en', name: 'English', file: 'en.js' },
        ],
        langDir: 'locales/',
        vueI18n: {
          fallbackLocale: 'en',
        },
      },
    ],
    base + '/modules/core/module.js',
    base + '/modules/database/module.js',
  ]
  const modules = baseModules.concat(additionalModules)
  return {
    modules,
  }
}
