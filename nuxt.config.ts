// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  compatibilityDate: '2024-04-03',
  devtools: { enabled: true },
  css: ['~/scss/theme.scss'],
  srcDir: 'app/',

  ignore: [
    "./*",
    "!./app/**"
  ],
  vite: {
    css: {
      preprocessorOptions: {
        scss: {
          api: 'modern-compiler'
        }
      }
    }
  },
  ssr: false,
  modules: ['@pinia/nuxt'],
  pinia: {
    storesDirs: ['./app/stores/**']
  }
})