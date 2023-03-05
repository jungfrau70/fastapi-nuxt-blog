require('dotenv').config()
import colors from 'vuetify/es5/util/colors'

export default {
  mode: 'universal',
  srcDir: '.',

  watchers: {
      webpack: {
          poll: true
      }
  },
  // Global page headers: https://go.nuxtjs.dev/config-head
  head: {
    titleTemplate: '%s - ' + process.env.npm_package_name,
    title: process.env.npm_package_name || '',    
    htmlAttrs: {
      lang: 'en',
    },
    meta: [
      { charset: 'utf-8' },
      { name: 'viewport', content: 'width=device-width, initial-scale=1' },
      { hid: 'description', name: 'description', content: process.env.npm_package_description || '' },
      { name: 'format-detection', content: 'telephone=no' },
    ],
    link: [{ rel: 'icon', type: 'image/x-icon', href: '/favicon.ico' }],
  },
  /*
  ** Customize the progress-bar color
  */
  loading: { color: '#fff' },
  // Global CSS: https://go.nuxtjs.dev/config-css
  css: [],

  // Plugins to run before rendering page: https://go.nuxtjs.dev/config-plugins
  plugins: [
    // { src: '~/plugins/vega-embed.js' },
    { src: '@/plugins/vuetify-datetimepicker.js' }, // datepicker plugin here
    {
        src: '@/plugins/vue-mavon-editor',
        ssr: false
    },
    { src: '@/plugins/day' }
  ],

  // Auto import components: https://go.nuxtjs.dev/config-components
  components: true,

  // Modules for dev and build (recommended): https://go.nuxtjs.dev/config-modules
  buildModules: [
    // https://go.nuxtjs.dev/eslint
    '@nuxtjs/eslint-module',
    // https://go.nuxtjs.dev/vuetify
    '@nuxtjs/vuetify',
    // '@nuxt/components',
    '@nuxtjs/moment',    
  ],
  moment: {
    defaultLocale: 'en',
    locales: ['ko'],
    timezone: true,
    defaultTimezone: 'Korea/Seoul',
    plugins: ['moment-strftime', 'moment-fquarter'],
  },

  // Modules: https://go.nuxtjs.dev/config-modules
  modules: [
    // https://go.nuxtjs.dev/axios
    '@nuxtjs/axios',
    // https://go.nuxtjs.dev/pwa
    '@nuxtjs/pwa',
    '@nuxtjs/auth',
    ['@nuxtjs/dotenv', { filename: process.env.NODE_ENV !== 'production' ? "./configs/.env.dev" : "./configs/.env.prod" }
    ],
  ],

  // Axios module configuration: https://go.nuxtjs.dev/config-axios
  axios: {
    // baseURL: process.env.BASE_URL || "http://localhost:8000/",
    baseURL: "http://localhost:8000/",
    browserBaseURL: process.env.BROWSER_BASE_URL,
    credentials: true,
    proxyHeaders: false
  },

  // PWA module configuration: https://go.nuxtjs.dev/pwa
  pwa: {
    manifest: {
      lang: 'en',
    },
  },

  auth: {
    redirect: {
        home: '/',
    },
    strategies: {
        local: {
            endpoints: {
                login: { url: '/auth/token', method: 'post', propertyName: 'access_token', headers: { "Content-Type": "multipart/form-data" } },
                user: { url: '/users/me/', method: 'get', propertyName: false },
                logout: false
            }
        },
    }
  },
  // router: {
  //     middleware: ['auth']
  // },

  /*
  ** vuetify module configuration
  ** https://github.com/nuxt-community/vuetify-module
  */
  vuetify: {
    customVariables: ['~/assets/variables.scss'],
    theme: {
        dark: false,
        themes: {
            dark: {
                primary: colors.blue.darken2,
                accent: colors.grey.darken3,
                secondary: colors.amber.darken3,
                info: colors.teal.lighten1,
                warning: colors.amber.base,
                error: colors.deepOrange.accent4,
                success: colors.green.accent3
            }
        }
    }
  },  
      /*
  ** Build configuration
  */
  build: {
    // transpile: ['vega-embed', 'vuetify-datetime-picker'],
    transpile: ['vuetify-datetime-picker'],    
    /*
    ** You can extend webpack config here
    */
    extend(config, ctx) {
    }
  },

  rules: {
    'no-console': process.env.NODE_ENV === 'production' ? 'error' : 'off',
  },

  publicRuntimeConfig: {
    apiURL: process.env.BASE_URL || "http://localhost:8000/",
  },
}
