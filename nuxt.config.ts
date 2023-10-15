// https://nuxt.com/docs/api/configuration/nuxt-config
import { aliases, mdi } from 'vuetify/iconsets/mdi-svg'
export default defineNuxtConfig({
  devtools: { enabled: true },
  modules: [
    '@invictus.codes/nuxt-vuetify',
    '@pinia/nuxt',
    '@pinia-plugin-persistedstate/nuxt',
  ],
  typescript: {
    shim: false
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
      title: "PtN 素材計算機",
      meta: [
        { property: 'og:type', content: 'website' },
        { property: 'og:site_name', content: 'PtN 素材計算機' },
        { property: 'og:title', content: 'PtN 素材計算機' },
        { property: 'og:description', content: '無期迷途育成素材計算機' },
        { property: 'og:url', content: 'https://pathtonowhere-tool.vercel.app' },
        { property: 'og:image', content:'https://pathtonowhere-tool.vercel.app/img/ogp.png'},
        { name: 'twitter:image', content:'https://pathtonowhere-tool.vercel.app/img/ogp.png'},
        { name: 'twitter:card', content: 'summary' }
      ]
    }
  }
})