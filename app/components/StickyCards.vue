<template>
  <section ref="root" class="sticky-stack" aria-label="Scroll reveal cards">
    <article
      v-for="(src, index) in stackImages"
      :key="src"
      class="sticky-card"
    >
      <img
        class="sticky-card__media"
        :src="src"
        :alt="`Scroll card ${index + 1}`"
      >
    </article>
  </section>
</template>

<script setup lang="ts">
import { stackImages } from '~/data/site'

const root = ref<HTMLElement | null>(null)
const { $gsap, $ScrollTrigger } = useNuxtApp()
const { unfolded } = useBoot()
let ctx: { revert: () => void } | null = null
let bound = false

const bind = () => {
  const gsap = $gsap
  const ScrollTrigger = $ScrollTrigger
  if (bound || !gsap || !ScrollTrigger || !root.value) return
  bound = true

  if (prefersReducedMotion()) return

  ctx = gsap.context(() => {
    const cards = Array.from(root.value!.querySelectorAll<HTMLElement>('.sticky-card'))

    cards.forEach((card, index) => {
      const media = card.querySelector<HTMLElement>('.sticky-card__media')
      if (media) gsap.set(media, { scale: 1.25 })

      if (index === cards.length - 1) return

      gsap.to(card, {
        scale: 0,
        rotate: 100,
        ease: 'none',
        scrollTrigger: {
          trigger: card,
          start: 'top 10%',
          end: '+=10000',
          scrub: true
        }
      })

      gsap.to(media, {
        rotate: -100,
        ease: 'none',
        scrollTrigger: {
          trigger: card,
          start: 'top 10%',
          end: '+=10000',
          scrub: true
        }
      })
    })
  }, root.value)

  ScrollTrigger.refresh()
}

onMounted(() => {
  watch(unfolded, (value) => {
    if (value) nextTick(bind)
  }, { immediate: true })
})

onBeforeUnmount(() => {
  ctx?.revert()
  $ScrollTrigger?.refresh()
})
</script>

<style scoped>
.sticky-stack {
  position: relative;
  display: flex;
  width: 100%;
  flex-direction: column;
  align-items: center;
  gap: 10vh;
  padding: 40px 0 28vh;
}

.sticky-card {
  position: sticky;
  top: 10vh;
  width: min(896px, 100%);
  height: 80vh;
  overflow: hidden;
  border-radius: 32px;
  background: var(--card);
  will-change: transform;
}

.sticky-card__media {
  display: block;
  width: 100%;
  height: 100%;
  object-fit: cover;
  will-change: transform;
}

@media (max-width: 899px) {
  .sticky-card {
    height: 72vh;
    border-radius: 24px;
  }
}
</style>
