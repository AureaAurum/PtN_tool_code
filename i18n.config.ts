import en from './locales/en.json'
import ja from './locales/ja.json'
import zh from './locales/zh.json'

export default defineI18nConfig(() => ({
    legacy: false,
    locale:"ja",
    defaultLocale: "ja",
    locales: ['ja','en','zh'],
    fallbackLocale :'zh',
    messages: {
      en,
      ja,
      zh
    }
  }))