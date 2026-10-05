<template>
  <button
    ref="root"
    class="toggle"
    type="button"
    :aria-label="theme === 'dark' ? 'Switch to light mode' : 'Switch to dark mode'"
    @mouseenter="onEnter"
    @mouseleave="onLeave"
    @click="onToggle"
  >
    <span class="toggle__thumb" :class="{ 'is-dark': theme === 'dark' }" aria-hidden="true" />
    <span ref="sunRef" class="toggle__icon toggle__icon--sun">
      <img src="/icons/sun.svg" alt="" width="16" height="16">
    </span>
    <span ref="moonRef" class="toggle__icon toggle__icon--moon">
      <img src="/icons/moon.svg" alt="" width="16" height="16">
    </span>
  </button>
</template>

<script setup lang="ts">
const { theme, toggleTheme } = useTheme()
const { $gsap } = useNuxtApp()
const sunRef = ref<HTMLElement | null>(null)
const moonRef = ref<HTMLElement | null>(null)
const root = ref<HTMLElement | null>(null)

const onEnter = () => {
  const gsap = $gsap
  if (!gsap || !root.value || !hasFinePointer() || prefersReducedMotion()) return
  gsap.to(root.value, { scale: 1.08, duration: 0.3, ease: 'power3.out' })
}

const onLeave = () => {
  const gsap = $gsap
  if (!gsap || !root.value) return
  gsap.to(root.value, { scale: 1, duration: 0.35, ease: 'power3.out' })
}

const onToggle = async (event: MouseEvent) => {
  const gsap = $gsap
  if (gsap) {
    const leaving = theme.value === 'light' ? sunRef.value : moonRef.value
    const entering = theme.value === 'light' ? moonRef.value : sunRef.value
    gsap.fromTo(leaving, { rotate: 0, scale: 1 }, { rotate: 180, scale: 0.4, duration: 0.45, ease: 'power3.in' })
    gsap.fromTo(entering, { rotate: -180, scale: 0.4 }, { rotate: 0, scale: 1, duration: 0.55, delay: 0.12, ease: 'power3.out' })
  }
  await toggleTheme(event)
}
</script>

<style scoped>
.toggle {
  position: relative;
  display: flex;
  align-items: center;
  width: 56px;
  height: 32px;
  padding: 4px;
  border-radius: 16px;
  background: var(--toggle-track);
  flex-shrink: 0;
  transform-origin: center center;
  will-change: transform;
}

.toggle__thumb {
  position: absolute;
  top: 4px;
  left: 4px;
  width: 24px;
  height: 24px;
  border-radius: 40px;
  background: var(--toggle-thumb);
  transition: transform 0.55s cubic-bezier(0.76, 0, 0.24, 1);
  z-index: 0;
}

.toggle__thumb.is-dark {
  transform: translateX(24px);
}

.toggle__icon {
  position: relative;
  z-index: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 24px;
  height: 24px;
  border-radius: 40px;
  overflow: clip;
}

.toggle__icon img {
  width: 16px;
  height: 16px;
  object-fit: contain;
}

[data-theme='dark'] .toggle__icon img {
  filter: invert(1);
}
</style>
