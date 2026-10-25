export const site = {
  name: 'Christian Anyikamadu',
  title: 'Frontend Engineer',
  location: 'Lagos, Nigeria',
  phone: '+2348142993740',
  phoneDisplay: '+234 814 299 3740',
  headline: 'Frontend Engineer who ships fintech, procurement, SaaS, and marketplace products from idea to production',
  description: 'Frontend engineer in Lagos with 4 years of experience shipping Vue, Nuxt, React, and Next.js products across fintech, procurement, SaaS, and marketplaces.',
  ogImage: '/og.jpg',
  email: 'anyikamaduchris@gmail.com',
  gmail: 'https://mail.google.com/mail/?view=cm&fs=1&to=anyikamaduchris@gmail.com',
  calendly: 'https://calendly.com/anyikamaduchris/30min',
  resumeHref: '/Christian Anyikamadu Frontend Engineer Resume 1.0.pdf?v=3',
  resumeFileName: 'Christian Anyikamadu Frontend Engineer Resume 1.0.pdf',
  socials: [
    { label: 'LinkedIn', href: 'https://www.linkedin.com/in/chris-anyikamadu-b3997820a' },
    { label: 'Github', href: 'https://github.com/chrixempire' }
  ],
  nav: [
    { label: 'Home', href: '#top' },
    { label: 'Works', href: '#works' },
    { label: 'Interaction', href: '/interaction' }
  ]
}

export const hoverImages = [
  { src: '/images/studies/ridge.jpg', alt: 'Ridge at dusk', code: 'Ridge' },
  { src: '/images/studies/field.jpg', alt: 'Open field', code: 'Field' },
  { src: '/images/studies/forest.jpg', alt: 'Forest path', code: 'Forest' },
  { src: '/images/studies/fog.jpg', alt: 'Fog over hills', code: 'Fog' },
  { src: '/images/studies/shore.jpg', alt: 'Shoreline', code: 'Shore' },
  { src: '/images/studies/night.jpg', alt: 'Night sky', code: 'Night' },
  { src: '/images/studies/peak.jpg', alt: 'Mountain peak', code: 'Peak' }
]

export const carouselImages = hoverImages.map(({ src, alt }) => ({ src, alt }))

export const stackImages = [
  ...hoverImages,
  { src: '/images/studies/valley.jpg', alt: 'Green valley' },
  { src: '/images/studies/falls.jpg', alt: 'Waterfall' }
]

export const techStack = [
  { label: 'Vue.js', src: '/icons/stack/vue.svg' },
  { label: 'Nuxt.js', src: '/icons/stack/nuxt.svg' },
  { label: 'React', src: '/icons/stack/react.svg' },
  { label: 'Next.js', src: '/icons/stack/next.svg', invertDark: true },
  { label: 'TypeScript', src: '/icons/stack/typescript.svg' },
  { label: 'JavaScript', src: '/icons/stack/javascript.svg' },
  { label: 'Pinia', src: '/icons/stack/pinia.svg' },
  { label: 'Tailwind', src: '/icons/stack/tailwind.svg' },
  { label: 'REST APIs', src: '/icons/stack/swagger.svg' },
  { label: 'Vite', src: '/icons/stack/vite.svg' }
]

export const experience = [
  {
    dates: 'April 2025  –  Present',
    role: 'Frontend Engineer, Acumen Digital, Lagos',
    logo: '/icons/companies/acumen.png',
    logoInset: true,
    logoWide: false,
    summary: 'Shipped production frontend across fintech, foreign exchange, procurement, lending, and marketplace products, from requirements through release.'
  },
  {
    dates: 'November 2022  –  March 2025',
    role: 'Frontend Engineer, Independent Purchasing Company – Africa',
    logo: '/icons/companies/ipc.png',
    logoInset: false,
    logoWide: false,
    summary: 'Led frontend across customer apps, admin dashboards, and marketing sites, and helped grow the engineering team from 3 to 10.'
  },
  {
    dates: 'July 2026  –  Present',
    role: 'Frontend Engineer (Contract), Bayana NGO',
    logo: '/icons/companies/bayana.svg',
    logoInset: true,
    logoWide: false,
    summary: 'Led frontend for Bayana, connecting verified NGOs with volunteers and donors. Shipped events, community, messaging, and broadcasts from requirements through production.'
  },
  {
    dates: 'August 2025  –  Present',
    role: 'Volunteer Frontend Engineer, Quality',
    logo: '/icons/companies/quality.svg',
    logoInset: true,
    logoWide: false,
    summary: 'Building frontend for Quality, a real-time feedback platform for teams, with responsive Next.js interfaces, reusable components, and live API features.'
  },
  {
    dates: 'April 2025  –  December 2025',
    role: 'Frontend Engineer, PostHearts',
    logo: '/icons/companies/posthearts.png',
    logoInset: false,
    logoWide: false,
    summary: 'Built the React frontend for PostHearts, a digital letter-making platform, including editor, creation, and sharing across web and mobile.'
  }
]

export const products = [
  {
    title: 'GoSource',
    description: 'Food procurement platform spanning website, user app, and admin back office. Drove nearly $70K in revenue in two months and 3x customer growth.',
    tools: 'VUE + NUXT + TYPESCRIPT',
    href: 'https://dashboard.gosource.app/',
    external: true,
    color: 'var(--card-b)',
    video: '/videos/gosource.mp4',
    poster: '/videos/gosource.jpg'
  },
  {
    title: 'Kaorex',
    description: 'Peer-to-peer foreign exchange marketplace with escrow, trading, live chat, reviews, compliance, and real-time transaction flows.',
    tools: 'VUE + REST + WEBSOCKETS',
    href: 'https://fx-p2p-frontend-qa.vercel.app/auth/sign-in',
    external: true,
    color: 'var(--card-c)',
    video: '/videos/kaorex.mp4',
    poster: '/videos/kaorex.jpg'
  },
  {
    title: 'Daash',
    description: 'SaaS ecosystem for daily business operations, including architectural direction and an internal payments integration across multiple methods.',
    tools: 'VUE + NUXT + TYPESCRIPT',
    href: 'https://app.daashapp.co/',
    external: true,
    color: 'var(--card-d)',
    video: '/videos/daash.mp4',
    poster: '/videos/daash.jpg'
  },
  {
    title: 'Octupus',
    description: 'Nigerian prediction-market platform covering market discovery, categories, trending markets, and a content/blog experience.',
    tools: 'VUE + NUXT + TYPESCRIPT',
    href: 'https://sabi-web-qa.vercel.app/auth/login',
    external: true,
    color: 'var(--card-e)',
    video: '/videos/octupus.mp4',
    poster: '/videos/octupus.jpg'
  },
  {
    title: 'Quality',
    description: 'Real-time feedback platform for teams, currently tested by Moniepoint engineers, with reusable interfaces and live collaboration.',
    tools: 'VUE + NUXT + APIS',
    href: 'https://usequality.app/',
    external: true,
    color: 'var(--card-a)',
    video: '/videos/quality.mp4',
    poster: '/videos/quality.jpg'
  },
  {
    title: 'PostHearts',
    description: 'Digital letter-making product with an interactive editor for typography, backgrounds, photos, stickers, and sharing on web and mobile.',
    tools: 'VUE + NUXT + TYPESCRIPT',
    href: 'https://posthearts.app/',
    external: true,
    color: 'var(--card-c)',
    video: '/videos/posthearts.mp4',
    poster: '/videos/posthearts.jpg'
  },
  {
    title: 'Bayana',
    description: 'Platform connecting verified NGOs with volunteers and donors for events, community, messaging, and broadcasts.',
    tools: 'REACT + NEXT.JS',
    href: 'https://app.joinbayana.com/',
    external: true,
    color: 'var(--card-d)',
    video: '/videos/bayana.mp4',
    poster: '/videos/bayana.jpg'
  }
]

export const testimonials = [
  {
    quote: 'Christian does great work and responds to feedback very well. Highly recommend working with him.',
    name: 'Daniel Osonuga',
    role: 'Product Designer @ IPC-Africa',
    color: 'var(--card-a)'
  },
  {
    quote: 'I highly recommend Christian to anyone looking for a top-tier developer who not only delivers quality work but also makes the collaboration smooth and enjoyable.',
    name: 'Temitope Agboola',
    role: 'Software Engineer @ Passpoint',
    color: 'var(--card-b)'
  },
  {
    quote: 'A pleasure to work with. His work is clean, very responsive, and he gives you exactly what’s designed. He pays attention to the details.',
    name: 'Semilore Adesiyun',
    role: 'Designer @ Acumen Digital',
    color: 'var(--card-c)'
  },
  {
    quote: 'Enjoyed working with him. He makes the job easier and faster, very proactive and timely.',
    name: 'Josh Anaba',
    role: 'Senior Frontend Engineer',
    color: 'var(--card-d)'
  },
  {
    quote: 'I highly recommend working with him. I’ve collaborated with him on a couple of projects. He’s great with interaction and always delivers what you design.',
    name: 'Ayomide Daniel',
    role: 'Designer @ Risevest',
    color: 'var(--card-e)'
  },
  {
    quote: 'A great guy. I strongly recommend him. He’s very good at what he does, detailed to the letter, and your go-to when the code has issues.',
    name: 'Odunsaya Derin',
    role: 'Frontend Engineer @ Gobank',
    color: 'var(--card-f)'
  }
]

export const heroCards = [
  { color: 'var(--card-a)', rotate: -15, image: '/images/hero/01.jpeg', position: 'center 22%' },
  { color: 'var(--card-c)', rotate: 15, image: '/images/hero/02.jpeg', position: 'center 18%' },
  { color: 'var(--card-b)', rotate: -15, image: '/images/hero/03.jpeg', position: 'center 20%' },
  { color: 'var(--card-d)', rotate: 15, image: '/images/hero/04.jpeg', position: 'center 12%' }
]
