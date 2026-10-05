import { site } from '~/data/site'

type SiteSeoOptions = {
  title?: string
  description?: string
  path?: string
}

export function useSiteSeo(options: SiteSeoOptions = {}) {
  const requestURL = useRequestURL()
  const route = useRoute()

  const origin = computed(() => requestURL.origin.replace(/\/$/, ''))
  const path = computed(() => options.path ?? route.path)
  const canonical = computed(() => {
    const suffix = path.value === '/' ? '/' : path.value
    return `${origin.value}${suffix}`
  })
  const title = options.title ?? `${site.name} - ${site.title}`
  const description = options.description ?? site.description
  const image = computed(() => `${origin.value}${site.ogImage}`)
  const imageAlt = `${site.name}, ${site.title}`

  useSeoMeta({
    title,
    description,
    author: site.name,
    robots: 'index, follow',
    ogType: 'website',
    ogTitle: title,
    ogDescription: description,
    ogUrl: canonical,
    ogImage: image,
    ogImageSecureUrl: image,
    ogImageType: 'image/jpeg',
    ogImageWidth: 1200,
    ogImageHeight: 630,
    ogImageAlt: imageAlt,
    ogLocale: 'en_US',
    ogSiteName: site.name,
    twitterCard: 'summary_large_image',
    twitterTitle: title,
    twitterDescription: description,
    twitterImage: image,
    twitterImageAlt: imageAlt
  })

  useHead({
    link: [
      { rel: 'canonical', href: canonical }
    ],
    script: [
      {
        type: 'application/ld+json',
        innerHTML: computed(() => JSON.stringify({
          '@context': 'https://schema.org',
          '@graph': [
            {
              '@type': 'Person',
              '@id': `${origin.value}/#person`,
              name: site.name,
              jobTitle: site.title,
              url: `${origin.value}/`,
              email: `mailto:${site.email}`,
              telephone: site.phone,
              image: `${origin.value}/images/portrait-square.jpeg`,
              address: {
                '@type': 'PostalAddress',
                addressLocality: 'Lagos',
                addressCountry: 'NG'
              },
              sameAs: site.socials.map(social => social.href),
              knowsAbout: [
                'Frontend Engineering',
                'Vue.js',
                'Nuxt',
                'React',
                'Next.js',
                'TypeScript'
              ]
            },
            {
              '@type': 'WebSite',
              '@id': `${origin.value}/#website`,
              url: `${origin.value}/`,
              name: `${site.name} - ${site.title}`,
              description: site.description,
              inLanguage: 'en',
              publisher: { '@id': `${origin.value}/#person` }
            },
            {
              '@type': 'WebPage',
              '@id': `${canonical.value}#webpage`,
              url: canonical.value,
              name: title,
              description,
              inLanguage: 'en',
              isPartOf: { '@id': `${origin.value}/#website` },
              about: { '@id': `${origin.value}/#person` }
            }
          ]
        }))
      }
    ]
  })
}
