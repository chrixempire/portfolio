<template>
  <header ref="root" class="header">
    <div class="header__inner">
      <NuxtLink to="/" class="brand" @click="onBrandClick">
        <img
          class="brand__avatar"
          src="/images/portrait.jpeg"
          :alt="`${site.name}, ${site.title}`"
          width="48"
          height="48"
        >
        <div class="brand__meta">
          <p class="brand__name">{{ site.name }}</p>
          <p class="brand__title">{{ site.title }} · {{ site.location }}</p>
          <span class="brand__badge">Available for work</span>
        </div>
      </NuxtLink>

      <nav class="nav" aria-label="Primary">
        <template v-for="item in site.nav" :key="item.href">
          <NuxtLink
            v-if="isRoute(item.href)"
            :to="item.href"
            class="nav__link"
            :class="{ 'is-active': isActive(item.href) }"
          >
            {{ item.label }}
            <span class="nav__line" />
          </NuxtLink>
          <button
            v-else
            class="nav__link"
            :class="{ 'is-active': isActive(item.href) }"
            type="button"
            @click="scrollTo(item.href)"
          >
            {{ item.label }}
            <span class="nav__line" />
          </button>
        </template>
        <span class="nav__link nav__link--email">
          <a class="nav__mail" :href="site.gmail" target="_blank" rel="noopener noreferrer">Email</a>
          <button
            class="nav__copy"
            type="button"
            :aria-label="copied ? 'Email copied' : 'Copy email'"
            @click="copyEmail"
          >
            <img :src="copied ? '/icons/check.svg' : '/icons/copy.svg'" alt="" width="10" height="10">
          </button>
          <span class="nav__line" />
        </span>
        <ThemeToggle />
      </nav>

      <div class="header__mobile-toggle">
        <NuxtLink
          class="mobile-link"
          :to="route.path === '/interaction' ? '/' : '/interaction'"
        >
          {{ route.path === '/interaction' ? 'Home' : 'Interaction' }}
        </NuxtLink>
        <ThemeToggle />
      </div>
    </div>
  </header>
</template>

<script setup lang="ts">
import { site } from '~/data/site'

const route = useRoute()
const root = ref<HTMLElement | null>(null)
const { $lenis, $gsap } = useNuxtApp()
const { unfolded } = useBoot()
let played = false

const copied = ref(false)
const isRoute = (href: string) => href.startsWith('/')
const isActive = (href: string) => {
  if (href === '/interaction') return route.path === '/interaction'
  if (href === '#top') return route.path === '/'
  return false
}

const onBrandClick = (event: MouseEvent) => {
  if (route.path !== '/') return
  event.preventDefault()
  $lenis?.scrollTo(0, { duration: 1.2 })
}

const scrollTo = async (href: string) => {
  const target = href === '#top' ? 0 : href
  if (route.path !== '/') {
    await navigateTo('/')
    await nextTick()
    window.setTimeout(() => {
      $lenis?.scrollTo(target, { offset: -24, duration: 1.2 })
    }, 80)
    return
  }
  $lenis?.scrollTo(target, { offset: -24, duration: 1.2 })
}

const copyEmail = async () => {
  try {
    await navigator.clipboard.writeText(site.email)
    copied.value = true
    window.setTimeout(() => { copied.value = false }, 1800)
  } catch {
    copied.value = false
  }
}

const playIntro = () => {
  const gsap = $gsap
  if (played || !gsap || !root.value) return
  played = true
  if (prefersReducedMotion()) {
    gsap.set(root.value.querySelector('.header__inner'), { y: 0, opacity: 1 })
    return
  }

  gsap.to(root.value.querySelector('.header__inner'), {
    y: 0,
    opacity: 1,
    duration: 0.9,
    ease: 'power4.out'
  })
}

const bindHover = () => {
  const gsap = $gsap
  if (!gsap || !root.value || !hasFinePointer() || prefersReducedMotion()) return

  root.value.querySelectorAll<HTMLElement>('.nav__link').forEach((link) => {
    const icon = link.querySelector<HTMLElement>('.nav__copy')
    link.addEventListener('mouseenter', () => {
      gsap.to(link, { color: 'var(--text)', y: -2, duration: 0.28, ease: 'power3.out' })
      if (icon) gsap.to(icon, { scale: 1.15, rotate: 8, duration: 0.3, ease: 'power3.out' })
    })
    link.addEventListener('mouseleave', () => {
      const active = link.classList.contains('is-active')
      gsap.to(link, { color: active ? 'var(--text)' : 'var(--text-nav)', y: 0, duration: 0.3, ease: 'power3.out' })
      if (icon) gsap.to(icon, { scale: 1, rotate: 0, duration: 0.3, ease: 'power3.out' })
    })
  })

  const avatar = root.value.querySelector('.brand__avatar')
  const badge = root.value.querySelector('.brand__badge')
  if (avatar) {
    root.value.querySelector('.brand')?.addEventListener('mouseenter', () => {
      gsap.to(avatar, { scale: 1.08, rotate: 8, duration: 0.35, ease: 'power3.out' })
      if (badge) gsap.to(badge, { y: -2, duration: 0.3, ease: 'power3.out' })
    })
    root.value.querySelector('.brand')?.addEventListener('mouseleave', () => {
      gsap.to(avatar, { scale: 1, rotate: 0, duration: 0.4, ease: 'power3.out' })
      if (badge) gsap.to(badge, { y: 0, duration: 0.3, ease: 'power3.out' })
    })
  }
}

const syncNavStyles = () => {
  const gsap = $gsap
  if (!gsap || !root.value) return
  root.value.querySelectorAll<HTMLElement>('.nav__link').forEach((link) => {
    const line = link.querySelector<HTMLElement>('.nav__line')
    const active = link.classList.contains('is-active')
    gsap.set(link, { color: active ? 'var(--text)' : 'var(--text-nav)', y: 0 })
    if (line) gsap.set(line, { clearProps: 'transform' })
  })
}

onMounted(() => {
  const gsap = $gsap
  if (gsap && root.value && !prefersReducedMotion()) {
    gsap.set(root.value.querySelector('.header__inner'), { y: -36, opacity: 0 })
  }
  bindHover()
  watch(unfolded, (value) => {
    if (value) playIntro()
  }, { immediate: true })
  watch(() => route.path, async () => {
    await nextTick()
    syncNavStyles()
  }, { immediate: true })
})
</script>

<style scoped>
.header {
  position: relative;
  z-index: 20;
}

.header__inner {
  display: flex;
  align-items: center;
  justify-content: space-between;
  width: min(696px, calc(100% - 40px));
  margin: 0 auto;
  padding-top: 40px;
}

.brand {
  display: flex;
  align-items: center;
  gap: 8px;
}

.brand__avatar {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  flex-shrink: 0;
  display: block;
  object-fit: cover;
  object-position: center 18%;
  background: var(--card-d);
}

.brand__meta {
  display: flex;
  flex-direction: column;
  gap: 6px;
  justify-content: center;
}

.brand__name {
  font-size: 14px;
  line-height: 22px;
  font-weight: 500;
  color: var(--text);
  white-space: nowrap;
}

.brand__title {
  font-size: 12px;
  line-height: 18px;
  color: var(--text-muted);
  white-space: nowrap;
}

.brand__badge {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  height: 18px;
  padding: 0 6px;
  border-radius: 6px;
  background: var(--available);
  color: #fff;
  font-size: 10px;
  line-height: 18px;
  font-weight: 500;
  text-transform: uppercase;
  width: fit-content;
}

.nav {
  display: none;
  align-items: center;
  gap: 32px;
}

.nav__link {
  position: relative;
  color: var(--text-nav);
  font-size: 14px;
  line-height: 22px;
  font-weight: 500;
  white-space: nowrap;
}

.nav__link.is-active {
  color: var(--text);
}

.nav__link--email {
  display: inline-flex;
  align-items: center;
  gap: 6px;
}

.nav__line {
  position: absolute;
  left: 0;
  bottom: -4px;
  width: 100%;
  height: 1px;
  background: var(--text);
  transform: scaleX(0);
  transform-origin: left center;
  transition: transform 0.3s ease;
}

.nav__link:hover .nav__line,
.nav__link.is-active .nav__line {
  transform: scaleX(1);
}

.nav__mail {
  color: inherit;
}

.nav__copy {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 16px;
  height: 16px;
  border-radius: 4px;
  background: var(--icon-bg-soft);
  overflow: clip;
}

.nav__copy img {
  width: 10px;
  height: 10px;
}

[data-theme='dark'] .nav__copy img {
  filter: invert(1);
}

.header__mobile-toggle {
  display: flex;
  align-items: center;
  gap: 16px;
}

.mobile-link {
  color: var(--text-nav);
  font-size: 14px;
  line-height: 22px;
  font-weight: 500;
}

@media (min-width: 900px) {
  .nav {
    display: flex;
  }

  .header__mobile-toggle {
    display: none;
  }
}

@media (max-width: 899px) {
  .header__inner {
    width: min(680px, calc(100% - 32px));
    padding-top: 36px;
  }

  .brand__title {
    white-space: normal;
  }
}
</style>
