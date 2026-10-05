<template>
  <section ref="root" class="stack reveal">
    <h2 class="stack__title font-display">My tech stack</h2>
    <div class="stack__viewport">
      <div ref="track" class="stack__track">
        <figure
          v-for="(item, index) in doubled"
          :key="index"
          class="stack__item"
        >
          <img
            class="stack__logo"
            :class="{ 'is-invert': item.invertDark }"
            :src="item.src"
            :alt="item.label"
            width="32"
            height="32"
          >
          <figcaption class="stack__label">{{ item.label }}</figcaption>
        </figure>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import { techStack } from '~/data/site'

const doubled = [...techStack, ...techStack]
const root = ref<HTMLElement | null>(null)
const track = ref<HTMLElement | null>(null)
const { $gsap } = useNuxtApp()
const { unfolded } = useBoot()
let bound = false

const bind = () => {
  const gsap = $gsap
  if (bound || !gsap || !track.value || !root.value) return
  bound = true
  if (prefersReducedMotion()) return

  const width = track.value.scrollWidth / 2
  const tween = gsap.to(track.value, {
    x: -width,
    duration: 22,
    ease: 'none',
    repeat: -1
  })

  const viewport = root.value.querySelector<HTMLElement>('.stack__viewport')
  if (viewport && hasFinePointer()) {
    viewport.addEventListener('mouseenter', () => tween.pause())
    viewport.addEventListener('mouseleave', () => tween.resume())
  }

  if (!hasFinePointer()) return

  root.value.querySelectorAll<HTMLElement>('.stack__item').forEach((item) => {
    item.addEventListener('mouseenter', () => {
      gsap.to(item, { y: -6, duration: 0.35, ease: 'expo.out' })
    })
    item.addEventListener('mouseleave', () => {
      gsap.to(item, { y: 0, duration: 0.4, ease: 'expo.out' })
    })
  })
}

onMounted(() => {
  watch(unfolded, (value) => {
    if (value) nextTick(bind)
  }, { immediate: true })
})
</script>

<style scoped>
.stack {
  display: flex;
  flex-direction: column;
  gap: 24px;
  width: 100%;
}

.stack__title {
  font-size: 18px;
  line-height: 28px;
  font-weight: 600;
  color: var(--text);
}

.stack__viewport {
  overflow: hidden;
  width: 100%;
}

.stack__track {
  display: flex;
  align-items: center;
  gap: 40px;
  width: max-content;
  will-change: transform;
}

.stack__item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  margin: 0;
  flex-shrink: 0;
  min-width: 72px;
}

.stack__logo {
  width: 32px;
  height: 32px;
  object-fit: contain;
  display: block;
}

.stack__label {
  font-size: 11px;
  line-height: 16px;
  font-weight: 600;
  color: var(--text-muted);
  white-space: nowrap;
}

[data-theme='dark'] .stack__logo.is-invert {
  filter: invert(1);
}
</style>
