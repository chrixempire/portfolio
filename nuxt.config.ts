// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  compatibilityDate: '2025-07-15',
  devtools: { enabled: false },
  css: ['~/assets/css/main.css'],
  app: {
    head: {
      title: 'Christian Anyikamadu - Frontend Engineer',
      htmlAttrs: { lang: 'en' },
      meta: [
        { name: 'viewport', content: 'width=device-width, initial-scale=1' },
        { name: 'description', content: 'Frontend engineer in Lagos with 4 years of experience shipping Vue, Nuxt, React, and Next.js products across fintech, procurement, SaaS, and marketplaces.' },
        { name: 'author', content: 'Christian Anyikamadu' },
        { name: 'robots', content: 'index, follow' },
        { name: 'theme-color', content: '#ffffff' },
        { name: 'application-name', content: 'Christian Anyikamadu' },
        { name: 'apple-mobile-web-app-title', content: 'Christian Anyikamadu' }
      ],
      link: [
        { rel: 'icon', type: 'image/png', sizes: '32x32', href: '/favicon-32.png' },
        { rel: 'icon', type: 'image/png', sizes: '192x192', href: '/favicon-192.png' },
        { rel: 'apple-touch-icon', sizes: '180x180', href: '/apple-touch-icon.png' },
        { rel: 'preconnect', href: 'https://fonts.googleapis.com' },
        { rel: 'preconnect', href: 'https://fonts.gstatic.com', crossorigin: '' },
        {
          rel: 'stylesheet',
          href: 'https://fonts.googleapis.com/css2?family=Geist:wght@500;600;700&family=Inter:wght@400;500;600&display=swap'
        }
      ],
      script: [
        {
          innerHTML: `try{var t=localStorage.getItem('theme');if(!t){t=window.matchMedia('(prefers-color-scheme:dark)').matches?'dark':'light'}document.documentElement.dataset.theme=t}catch(e){document.documentElement.dataset.theme='light'}`
        }
      ]
    },
    pageTransition: false,
    layoutTransition: false
  }
})
