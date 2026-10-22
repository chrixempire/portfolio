<template>
  <div
    class="creative"
    :class="{ 'is-ready': ready, 'is-dragging': dragging }"
    @pointerdown="onDown"
    @pointermove="onMove"
    @pointerup="onUp"
    @pointercancel="onUp"
  >
    <div class="creative__viewport">
      <article
        v-for="(image, index) in carouselImages"
        :key="image.src"
        class="creative__slide"
        :style="slideStyle(index)"
      >
        <img class="creative__media" :src="image.src" :alt="image.alt">
        <div class="creative__shadow" :style="{ opacity: shadow(index) }" />
      </article>
    </div>
    <div class="creative__dots" role="tablist" aria-label="Slides">
      <button
        v-for="(image, index) in carouselImages"
        :key="`${image.src}-dot`"
        type="button"
        class="creative__dot"
        :class="{ 'is-on': index === nearest }"
        :aria-label="`Show ${image.alt}`"
        @click="go(index)"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { carouselImages } from '~/data/site'

const position = ref(0)
const ready = ref(false)
const dragging = ref(false)
let startX = 0
let startPos = 0

const total = carouselImages.length

const nearest = computed(() => {
  const wrapped = ((Math.round(position.value) % total) + total) % total
  return wrapped
})

const delta = (index: number) => {
  let diff = position.value - index
  diff = ((diff % total) + total) % total
  if (diff > total / 2) diff -= total
  return diff
}

const slideStyle = (index: number) => {
  const progress = Math.min(1, Math.max(-1, delta(index)))
  const amount = Math.abs(progress)
  const zIndex = total - Math.round(Math.abs(delta(index)))
  if (amount < 0.001) {
    return {
      transform: 'translate3d(0, 0, 0) rotateY(0deg)',
      transformOrigin: 'center center',
      zIndex
    }
  }
  if (progress > 0) {
    return {
      transform: `translate3d(${-5 * amount}%, 0, ${-200 * amount}px) rotateY(${100 * amount}deg)`,
      transformOrigin: 'left center',
      zIndex
    }
  }
  return {
    transform: `translate3d(${5 * amount}%, 0, ${-200 * amount}px) rotateY(${-100 * amount}deg)`,
    transformOrigin: 'right center',
    zIndex
  }
}

const shadow = (index: number) => {
  const progress = delta(index)
  return progress > 0 ? Math.min(progress, 1) : 0
}

const go = (index: number) => {
  const current = ((position.value % total) + total) % total
  let diff = index - current
  if (diff > total / 2) diff -= total
  if (diff < -total / 2) diff += total
  position.value += diff
}

const onDown = (event: PointerEvent) => {
  if ((event.target as HTMLElement).closest('.creative__dot')) return
  dragging.value = true
  startX = event.clientX
  startPos = position.value
  ;(event.currentTarget as HTMLElement).setPointerCapture(event.pointerId)
}

const onMove = (event: PointerEvent) => {
  if (!dragging.value) return
  const dx = event.clientX - startX
  position.value = startPos - dx / 300
}

const onUp = () => {
  if (!dragging.value) return
  dragging.value = false
  position.value = Math.round(position.value)
}

onMounted(() => {
  requestAnimationFrame(() => {
    ready.value = true
  })
})
</script>

<style scoped>
.creative {
  width: min(640px, 100%);
  margin: 0 auto;
  cursor: grab;
  user-select: none;
  touch-action: pan-y;
}

.creative.is-dragging {
  cursor: grabbing;
}

.creative__viewport {
  position: relative;
  height: 390px;
  perspective: 1200px;
}

.creative__slide {
  position: absolute;
  top: 0;
  left: 50%;
  width: 300px;
  height: 390px;
  margin-left: -150px;
  overflow: hidden;
  border-radius: 16px;
  background: #111111;
  backface-visibility: hidden;
  will-change: transform;
}

.creative.is-ready .creative__slide {
  transition: transform 0.55s cubic-bezier(0.22, 1, 0.36, 1);
}

.creative.is-dragging .creative__slide {
  transition: none;
}

.creative__media {
  display: block;
  width: 100%;
  height: 100%;
  object-fit: cover;
  pointer-events: none;
}

.creative__shadow {
  position: absolute;
  inset: 0;
  background: #000000;
  pointer-events: none;
}

.creative__dots {
  display: flex;
  justify-content: center;
  gap: 8px;
  margin-top: 18px;
}

.creative__dot {
  width: 8px;
  height: 8px;
  border-radius: 999px;
  background: color-mix(in srgb, var(--ink) 22%, transparent);
}

.creative__dot.is-on {
  background: #3b6cff;
}

@media (max-width: 420px) {
  .creative__viewport,
  .creative__slide {
    height: 320px;
  }

  .creative__slide {
    width: 246px;
    margin-left: -123px;
  }
}
</style>
