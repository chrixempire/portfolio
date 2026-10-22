<template>
  <section ref="root" class="stack" aria-label="Scroll reveal cards">
    <article
      v-for="image in stackImages"
      :key="image.src"
      class="stack__card"
    >
      <img class="stack__media" :src="image.src" :alt="image.alt">
    </article>
  </section>
</template>

<script setup lang="ts">
import { stackImages } from '~/data/site'

const root = ref<HTMLElement | null>(null)

const layoutTop = (node: HTMLElement) => {
  let y = 0
  let current: HTMLElement | null = node
  while (current) {
    y += current.offsetTop
    current = current.offsetParent as HTMLElement | null
  }
  return y
}

const paint = () => {
  const section = root.value
  if (!section) return
  const height = window.innerHeight
  const y = window.scrollY
  const sectionTop = layoutTop(section)
  const cards = section.querySelectorAll<HTMLElement>('.stack__card')
  cards.forEach((card, index) => {
    const cardTop = sectionTop + height * (0.5 + index * 0.9)
    const start = cardTop - height * 0.1
    const progress = y <= start ? 0 : Math.min(1, (y - start) / 10000)
    const scale = 1 - progress
    const rotate = progress * 100
    card.style.transform = `scale(${scale}) rotate(${rotate}deg)`
    const image = card.querySelector('img')
    if (image) image.style.transform = `rotate(${-rotate}deg)`
  })
}

onMounted(() => {
  paint()
  window.addEventListener('scroll', paint, { passive: true })
  window.addEventListener('resize', paint)
  const { $lenis } = useNuxtApp()
  $lenis?.on?.('scroll', paint)
})

onUnmounted(() => {
  window.removeEventListener('scroll', paint)
  window.removeEventListener('resize', paint)
  const { $lenis } = useNuxtApp()
  $lenis?.off?.('scroll', paint)
})
</script>

<style scoped>
.stack {
  position: relative;
  display: flex;
  flex-direction: column;
  align-items: stretch;
  gap: 10vh;
  width: 100%;
  padding-top: 50vh;
}

.stack__card {
  position: sticky;
  top: 10vh;
  width: 100%;
  height: 80vh;
  overflow: hidden;
  border-radius: 32px;
  background: #e5e5e5;
}

.stack__media {
  width: 100%;
  height: 100%;
  object-fit: cover;
  scale: 1.25;
}
</style>
