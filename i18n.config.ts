import messages from './locales/messages'

export default defineI18nConfig(() => ({
    legacy: false,
    locale:"ja",
    defaultLocale: "ja",
    locales: ['ja','en','zh'],
    fallbackLocale :'en',
    messages
  }))