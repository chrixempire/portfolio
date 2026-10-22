<template>
  <div ref="track" class="stack-track">
    <article class="stack-card">
      <div ref="frame" class="stack-card__frame">
        <img ref="media" class="stack-card__media" :src="src" :alt="alt">
      </div>
    </article>
  </div>
</template>

<script setup lang="ts">
import { useMotionValue, useTransform } from 'motion-v'

const props = defineProps<{
  src: string
  alt: string
  last?: boolean
}>()

const track = ref<HTMLElement | null>(null)
const frame = ref<HTMLElement | null>(null)
const media = ref<HTMLElement | null>(null)

const progress = useMotionValue(0)
const scale = useTransform(progress, [0, 1], [1, props.last ? 1 : 0.68])
const rotate = useTransform(progress, [0, 1], [0, props.last ? 0 : 16])
const mediaRotate = useTransform(progress, [0, 1], [0, props.last ? 0 : -16])

const paint = () => {
  frame.value?.style.setProperty('--scale', String(scale.get()))
  frame.value?.style.setProperty('--rotate', `${rotate.get()}deg`)
  media.value?.style.setProperty('--media-rotate', `${mediaRotate.get()}deg`)
}

let stop = () => {}

onMounted(() => {
  const target = track.value
  if (!target) return
  const update = () => {
    const rect = target.getBoundingClientRect()
    const pin = window.innerHeight * 0.12
    const cardHeight = window.innerHeight * 0.68
    const travel = Math.max(rect.height - cardHeight - pin, 1)
    const value = Math.min(1, Math.max(0, (pin - rect.top) / travel))
    progress.set(value)
    paint()
  }
  window.addEventListener('scroll', update, { passive: true })
  stop = () => window.removeEventListener('scroll', update)
  update()
})

onUnmounted(() => stop())
</script>

<style scoped>
.stack-track {
  position: relative;
  height: 120vh;
  margin-bottom: -28vh;
}

.stack-card {
  position: sticky;
  top: 12vh;
  width: min(640px, 100%);
  height: 68vh;
  margin: 0 auto;
}

.stack-card__frame {
  --scale: 1;
  --rotate: 0deg;
  width: 100%;
  height: 100%;
  overflow: hidden;
  border-radius: 24px;
  background: #111111;
  transform: scale(var(--scale)) rotate(var(--rotate));
  transform-origin: center top;
}

.stack-card__media {
  --media-rotate: 0deg;
  display: block;
  width: 100%;
  height: 100%;
  object-fit: cover;
  transform: scale(1.12) rotate(var(--media-rotate));
  transform-origin: center;
}
</style>
