<template>
  <section id="works" ref="root" class="products reveal">
    <h2 class="products__title font-display">Products I’ve worked on</h2>
    <div class="products__grid">
      <article
        v-for="product in products"
        :key="product.title + product.tools"
        class="product"
        @pointerenter="onEnter"
        @pointerleave="onLeave"
      >
        <a
          class="product__media"
          :href="product.href"
          :target="product.external ? '_blank' : undefined"
          :rel="product.external ? 'noopener noreferrer' : undefined"
        >
          <span class="product__fill" :style="{ background: product.color }">
            <video
              v-if="product.video"
              class="product__video"
              :src="product.video"
              :poster="product.poster || undefined"
              muted
              loop
              playsinline
              preload="metadata"
            />
          </span>
        </a>
        <div class="product__meta">
          <div class="product__copy">
            <a
              class="product__title"
              :href="product.href"
              :class="{ 'is-external': product.external }"
              :target="product.external ? '_blank' : undefined"
              :rel="product.external ? 'noopener noreferrer' : undefined"
            >
              {{ product.title }}
              <span class="product__arrow" :class="{ 'is-external': product.external }">
                <img src="/icons/arrow-up.svg" alt="" width="16" height="16">
              </span>
            </a>
            <p class="product__desc">{{ product.description }}</p>
          </div>
          <p class="product__tools">{{ product.tools }}</p>
        </div>
      </article>
    </div>
  </section>
</template>

<script setup lang="ts">
import { products } from '~/data/site'

const root = ref<HTMLElement | null>(null)
const { $gsap, $ScrollTrigger } = useNuxtApp()
const { unfolded } = useBoot()
let bound = false
const movers = new WeakMap<HTMLElement, { xTo: (value: number) => void, yTo: (value: number) => void }>()

const videoFrom = (event: Event) => {
  const card = event.currentTarget as HTMLElement
  return card.querySelector<HTMLVideoElement>('.product__video')
}

const playVideo = (video: HTMLVideoElement | null) => {
  if (!video) return
  video.preload = 'auto'
  const play = video.play()
  if (play) play.catch(() => {})
}

const stopVideo = (video: HTMLVideoElement | null) => {
  if (!video) return
  video.pause()
  video.currentTime = 0
}

const onEnter = (event: PointerEvent) => {
  const card = event.currentTarget as HTMLElement
  const video = videoFrom(event)
  if (event.pointerType !== 'touch') playVideo(video)

  const gsap = $gsap
  if (!gsap || prefersReducedMotion() || !hasFinePointer()) return
  const fill = card.querySelector<HTMLElement>('.product__fill')
  const arrow = card.querySelector<HTMLElement>('.product__arrow img')
  const title = card.querySelector<HTMLElement>('.product__title')
  if (fill) gsap.to(fill, { scale: 1.08, duration: 1.15, ease: 'expo.out', overwrite: 'auto' })
  if (video) gsap.to(video, { opacity: 1, scale: 1, duration: 0.7, ease: 'expo.out', overwrite: 'auto' })
  if (arrow) gsap.to(arrow, { x: 3, y: -3, duration: 0.7, ease: 'expo.out' })
  if (title) gsap.to(title, { x: 4, duration: 0.7, ease: 'expo.out' })
}

const onLeave = (event: PointerEvent) => {
  const card = event.currentTarget as HTMLElement
  const video = videoFrom(event)
  stopVideo(video)

  const gsap = $gsap
  const mover = movers.get(card)
  if (mover) {
    mover.xTo(0)
    mover.yTo(0)
  }
  if (!gsap || prefersReducedMotion() || !hasFinePointer()) return
  const fill = card.querySelector<HTMLElement>('.product__fill')
  const arrow = card.querySelector<HTMLElement>('.product__arrow img')
  const title = card.querySelector<HTMLElement>('.product__title')
  if (fill) gsap.to(fill, { scale: 1, duration: 1.2, ease: 'expo.out', overwrite: 'auto' })
  if (video) gsap.to(video, { opacity: 0.92, scale: 1.04, duration: 0.8, ease: 'expo.out', overwrite: 'auto' })
  if (arrow) gsap.to(arrow, { x: 0, y: 0, duration: 0.8, ease: 'expo.out' })
  if (title) gsap.to(title, { x: 0, duration: 0.8, ease: 'expo.out' })
}

const bind = () => {
  const gsap = $gsap
  const ScrollTrigger = $ScrollTrigger
  if (bound || !gsap || !root.value) return
  bound = true

  const cards = Array.from(root.value.querySelectorAll<HTMLElement>('.product'))

  if (!prefersReducedMotion() && ScrollTrigger) {
    cards.forEach((card, index) => {
      const media = card.querySelector<HTMLElement>('.product__media')
      const fill = card.querySelector<HTMLElement>('.product__fill')
      const video = card.querySelector<HTMLVideoElement>('.product__video')
      if (!media || !fill) return

      gsap.fromTo(media, {
        clipPath: 'inset(100% 0 0 0 round 16px)'
      }, {
        clipPath: 'inset(0% 0% 0% 0% round 16px)',
        duration: 1.35,
        ease: 'expo.inOut',
        delay: (index % 2) * 0.1,
        scrollTrigger: {
          trigger: card,
          start: 'top 88%',
          once: true
        }
      })

      gsap.fromTo(fill, {
        scale: 1.22
      }, {
        scale: 1,
        duration: 1.7,
        ease: 'expo.out',
        delay: (index % 2) * 0.1,
        scrollTrigger: {
          trigger: card,
          start: 'top 88%',
          once: true
        }
      })

      if (video) {
        gsap.set(video, { opacity: 0.92, scale: 1.04 })
      }

      gsap.from(card.querySelectorAll('.product__meta > *'), {
        y: 18,
        opacity: 0,
        duration: 1,
        stagger: 0.08,
        ease: 'expo.out',
        delay: 0.18 + (index % 2) * 0.1,
        scrollTrigger: {
          trigger: card,
          start: 'top 88%',
          once: true
        }
      })
    })
  }

  if (hasFinePointer() && !prefersReducedMotion()) {
    cards.forEach((card) => {
      const fill = card.querySelector<HTMLElement>('.product__fill')
      if (!fill) return
      const xTo = gsap.quickTo(fill, 'x', { duration: 0.9, ease: 'expo.out' })
      const yTo = gsap.quickTo(fill, 'y', { duration: 0.9, ease: 'expo.out' })
      movers.set(card, { xTo, yTo })

      card.addEventListener('mousemove', (event) => {
        const rect = fill.getBoundingClientRect()
        const x = (event.clientX - (rect.left + rect.width / 2)) / rect.width
        const y = (event.clientY - (rect.top + rect.height / 2)) / rect.height
        xTo(x * 14)
        yTo(y * 10)
      })
    })
  }

  if (!hasFinePointer()) {
    const observer = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        const video = entry.target.querySelector<HTMLVideoElement>('.product__video')
        if (!video) return
        if (entry.isIntersecting && entry.intersectionRatio >= 0.6) playVideo(video)
        else stopVideo(video)
      })
    }, { threshold: [0.6] })
    cards.forEach(card => observer.observe(card))
  }
}

onMounted(() => {
  watch(unfolded, (value) => {
    if (value) nextTick(bind)
  }, { immediate: true })
})
</script>

<style scoped>
.products {
  display: flex;
  flex-direction: column;
  gap: 24px;
  width: 100%;
}

.products__title {
  font-size: 18px;
  line-height: 28px;
  font-weight: 600;
}

.products__grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 20px;
}

.product {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.product__media {
  display: block;
  height: 270px;
  border-radius: 16px;
  overflow: hidden;
  position: relative;
}

.product__fill {
  position: absolute;
  inset: -12%;
  border-radius: 16px;
  will-change: transform;
  transform: translateZ(0);
  overflow: hidden;
}

.product__video {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
  pointer-events: none;
}

.product__meta {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.product__copy {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.product__title {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  font-size: 16px;
  line-height: 24px;
  font-weight: 500;
  color: var(--text);
  width: fit-content;
}

.product__title.is-external {
  text-decoration: underline;
  text-decoration-style: dotted;
  text-underline-offset: 3px;
}

.product__arrow {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 16px;
  height: 16px;
  overflow: clip;
  transform: rotate(90deg);
}

.product__arrow.is-external {
  transform: rotate(45deg);
}

.product__arrow img {
  width: 16px;
  height: 16px;
}

[data-theme='dark'] .product__arrow img {
  filter: invert(1);
}

.product__desc {
  color: var(--text-muted);
  font-size: 14px;
  line-height: 22px;
}

.product__tools {
  font-size: 10px;
  line-height: 18px;
  font-weight: 600;
  text-transform: uppercase;
  color: var(--text);
}

@media (min-width: 900px) {
  .products__grid {
    grid-template-columns: 1fr 1fr;
    gap: 20px;
  }
}

@media (max-width: 899px) {
  .product__title {
    font-size: 14px;
    line-height: 22px;
  }
}
</style>
