import messages from './locales/messages'

export default defineI18nConfig(() => ({

    legacy: false,
    locales: [{code:'ja',iso:'ja_JP'},{code:'en',iso:'en-US'},{code:'zh',iso:'zh-CN'}],
    locale: "ja",
    defaultLocale: "ja",
    detectBrowserLanguage: {
      useCookie: true,
      cookieKey: 'i18n_redirected',
    },
    strategy: 'no_prefix',
    lazy: true,
    fallbackLocale :'en',
    silentFallbackWarn: true,
    silentTranslationWarn: true,
    messages
  }))