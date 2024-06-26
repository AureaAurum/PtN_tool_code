// https://nuxt.com/docs/api/configuration/nuxt-config
import { aliases, mdi } from 'vuetify/iconsets/mdi-svg'
export default defineNuxtConfig({
  devtools: { enabled: true },
  modules: [
    '@invictus.codes/nuxt-vuetify',
    '@pinia/nuxt',
    '@pinia-plugin-persistedstate/nuxt',
    '@nuxtjs/i18n',
  ],
  typescript: {
    shim: false,
    typeCheck: false,
  },
  i18n: {
    /* module options */
    vueI18n: './i18n.config.ts'
  },
  vuetify: {
    /* vuetify options */
    vuetifyOptions: {
      // @TODO: list all vuetify options
      icons: {
        defaultSet: 'mdi',
        aliases,
        sets: {
          mdi,
        },
      },
    },
    moduleOptions: {
      /* nuxt-vuetify module options */
      treeshaking: true,
      useIconCDN: false,

      /* vite-plugin-vuetify options */
      styles: true,
      autoImport: true,
      useVuetifyLabs: true,
    },
  },
  alias: {
    pinia: "/node_modules/@pinia/nuxt/node_modules/pinia/dist/pinia.mjs"
  },
  build: {
    transpile: ['pinia-plugin-persistedstate'],
  },
  ssr:false,
  app: {
    head: {
      htmlAttrs: {
        lang: 'ja', prefix: 'og: https://ogp.me/ns#'
      },
      title: "無期迷途 素材計算機",
      meta: [
        { property: 'og:type', content: 'website' },
        { property: 'og:site_name', content: '無期迷途育成素材計算機' },
        { property: 'og:title', content: '無期迷途育成素材計算機' },
        { property: 'og:description', content: '無期迷途育成素材計算機' },
        { property: 'og:url', content: 'https://pathtonowhere-tool.vercel.app' },
        { property: 'og:image', content:'https://pathtonowhere-tool.vercel.app/img/ogp.png'},
        { name: 'twitter:image', content:'https://pathtonowhere-tool.vercel.app/img/ogp.png'},
        { name: 'twitter:card', content: 'summary' },
        { name: 'description', content: '無期迷途の必要な育成素材を集計するツール' },
        { name:"google-site-verification", content:"1b4qYOs-FVRUExwnvCNL28aYnR3cFZgWJVvOuqL5IL8" }
      ]
    }
  }
})