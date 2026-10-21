<template>
  <div class="shell">
    <div class="page-sky" />
    <div ref="flashRef" class="theme-flash" aria-hidden="true" />
    <CustomCursor />
    <Preloader v-if="!skipLoader" v-model="booting" />
    <Unfold v-if="!skipLoader" />
    <div class="site">
      <AppHeader />
      <NuxtPage />
    </div>
    <Toaster />
  </div>
</template>

<script setup lang="ts">
const route = useRoute()
const { booting, finishBoot, finishUnfold } = useBoot()
const { initTheme, applyTheme } = useTheme()
const { $gsap, $lenis, $ScrollTrigger } = useNuxtApp()
const flashRef = ref<HTMLElement | null>(null)
const skipLoader = computed(() => route.query.skipLoader === '1')

const onTheme = (event: Event) => {
  const gsap = $gsap
  if (!gsap || !flashRef.value) return
  const detail = (event as CustomEvent<{ x: number, y: number }>).detail
  const x = `${((detail?.x ?? window.innerWidth) / window.innerWidth) * 100}%`
  const y = `${((detail?.y ?? 48) / window.innerHeight) * 100}%`
  document.documentElement.style.setProperty('--flash-x', x)
  document.documentElement.style.setProperty('--flash-y', y)
  gsap.fromTo(flashRef.value, { opacity: 0.7 }, { opacity: 0, duration: 0.9, ease: 'power2.out' })
  gsap.fromTo('.fan__fill, .product__fill, .sticky-card__media, .experience__media, .quote__avatar, .brand__avatar', {
    scale: 0.96,
    filter: 'saturate(1.4)'
  }, {
    scale: 1,
    filter: 'saturate(1)',
    duration: 0.8,
    stagger: 0.03,
    ease: 'power3.out'
  })
}

watch(() => route.path, (path, previous) => {
  if (!previous || path === previous) return
  nextTick(() => {
    $lenis?.scrollTo(0, { immediate: true })
    $ScrollTrigger?.refresh()
  })
})

onMounted(() => {
  const requested = route.query.theme
  if (requested === 'dark' || requested === 'light') applyTheme(requested)
  else initTheme()

  if (skipLoader.value) {
    finishBoot()
    finishUnfold()
  }
  window.addEventListener('theme-change', onTheme)
})

onBeforeUnmount(() => {
  window.removeEventListener('theme-change', onTheme)
})
</script>

<style scoped>
.shell {
  min-height: 100vh;
  background: var(--bg);
  color: var(--text);
}
</style>
