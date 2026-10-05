<template>
  <main class="page">
    <HeroSection />
    <div class="page__sections">
      <TechStack />
      <ExperienceSection />
      <ProductsSection />
      <TestimonialsSection />
    </div>
    <div class="page__bottom">
      <div class="page__landscape" aria-hidden="true">
        <div class="page__landscape-photo">
          <img src="/images/footer-landscape.png" alt="" width="1920" height="1076">
        </div>
        <div class="page__landscape-veil" />
      </div>
      <div class="page__cta">
        <ContactCta />
      </div>
      <AppFooter />
    </div>
  </main>
</template>

<script setup lang="ts">
useSiteSeo()

const { $gsap, $ScrollTrigger } = useNuxtApp()
const { unfolded } = useBoot()
let bound = false

const bindScroll = () => {
  const gsap = $gsap
  const ScrollTrigger = $ScrollTrigger
  if (bound || !gsap || !ScrollTrigger) return
  if (prefersReducedMotion()) return
  bound = true

  gsap.utils.toArray<HTMLElement>('.reveal').forEach((section) => {
    gsap.from(section, {
      y: 56,
      opacity: 0,
      duration: 1.35,
      ease: 'expo.out',
      scrollTrigger: {
        trigger: section,
        start: 'top 86%',
        once: true
      }
    })
  })
}

onMounted(() => {
  watch(unfolded, (value) => {
    if (value) {
      nextTick(() => {
        bindScroll()
        $ScrollTrigger?.refresh()
      })
    }
  }, { immediate: true })
})
</script>

<style scoped>
.page {
  width: 100%;
}

.page__sections {
  width: min(840px, calc(100% - 40px));
  margin: 80px auto 0;
  display: flex;
  flex-direction: column;
  gap: 80px;
}

.page__bottom {
  position: relative;
  margin-top: 80px;
  overflow: hidden;
  background: var(--bg);
}

.page__cta,
.page__bottom :deep(.footer) {
  position: relative;
  z-index: 1;
}

.page__cta {
  width: min(840px, calc(100% - 40px));
  margin: 0 auto;
}

.page__landscape {
  position: absolute;
  left: 0;
  right: 0;
  bottom: 0;
  height: 841px;
  max-height: 100%;
  pointer-events: none;
  mix-blend-mode: luminosity;
  z-index: 0;
}

.page__landscape-photo {
  position: absolute;
  inset: 0;
  overflow: hidden;
  opacity: 0.2;
}

.page__landscape-photo img {
  position: absolute;
  top: 0;
  left: -25.37%;
  width: 125.37%;
  height: 120.36%;
  max-width: none;
  object-fit: cover;
}

.page__landscape-veil {
  position: absolute;
  inset: 0;
  background: var(--footer-veil);
}

@media (max-width: 899px) {
  .page__sections {
    width: min(680px, calc(100% - 32px));
    margin-top: 80px;
    gap: 56px;
  }

  .page__bottom {
    margin-top: 56px;
  }

  .page__cta {
    width: min(680px, calc(100% - 32px));
  }

  .page__landscape {
    height: 444px;
    width: 202.933%;
    left: -62.933%;
    right: auto;
  }
}
</style>
