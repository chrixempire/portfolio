<template>
  <div v-if="enabled" class="cursor" aria-hidden="true">
    <div ref="gauge" class="cursor__gauge">
      <svg class="cursor__svg" viewBox="0 0 48 48">
        <circle class="cursor__track" cx="24" cy="24" r="20" />
        <circle
          ref="progress"
          class="cursor__progress"
          :class="{ 'is-reverse': reverse }"
          cx="24"
          cy="24"
          r="20"
        />
      </svg>
      <span class="cursor__pct">{{ percent }}<small>%</small></span>
    </div>
  </div>
</template>

<script setup lang="ts">
const RADIUS = 20
const CIRCUMFERENCE = 2 * Math.PI * RADIUS

const enabled = ref(false)
const percent = ref(0)
const reverse = ref(false)
const gauge = ref<HTMLElement | null>(null)
const progress = ref<SVGCircleElement | null>(null)
const { $gsap, $lenis } = useNuxtApp()

let move: ((event: MouseEvent) => void) | null = null
let down: (() => void) | null = null
let up: (() => void) | null = null
let over: ((event: PointerEvent) => void) | null = null
let out: ((event: PointerEvent) => void) | null = null
let onScroll: ((event: { progress?: number, direction?: number, scroll?: number, limit?: number }) => void) | null = null

const setPercent = (value: number) => {
  const next = Math.max(0, Math.min(100, Math.round(value)))
  if (next !== percent.value) percent.value = next
}

onMounted(async () => {
  enabled.value = window.matchMedia('(pointer: fine)').matches && !window.matchMedia('(prefers-reduced-motion: reduce)').matches
  if (!enabled.value) return

  const gsap = $gsap
  if (!gsap) return

  await nextTick()
  if (!gauge.value || !progress.value) return

  gsap.set(progress.value, { strokeDasharray: CIRCUMFERENCE, strokeDashoffset: CIRCUMFERENCE })
  const offsetTo = gsap.quickTo(progress.value, 'strokeDashoffset', { duration: 0.45, ease: 'power3.out' })

  const applyProgress = (scrolled: number) => {
    setPercent(scrolled * 100)
    offsetTo(CIRCUMFERENCE * (1 - scrolled))
  }

  const xGauge = gsap.quickTo(gauge.value, 'x', { duration: 0.4, ease: 'power3' })
  const yGauge = gsap.quickTo(gauge.value, 'y', { duration: 0.4, ease: 'power3' })

  move = (event: MouseEvent) => {
    xGauge(event.clientX)
    yGauge(event.clientY)
  }

  down = () => gsap.to(gauge.value, { scale: 0.86, duration: 0.2 })
  up = () => gsap.to(gauge.value, { scale: 1, duration: 0.3, ease: 'power3.out' })

  const isHot = (target: EventTarget | null) =>
    target instanceof Element && Boolean(target.closest('a, button, .fan__item, .product, .quote, .experience__item, .stack__item'))

  const onOver = (event: PointerEvent) => {
    if (isHot(event.target) && !isHot(event.relatedTarget)) {
      gsap.to(gauge.value, { scale: 1.18, duration: 0.35, ease: 'expo.out' })
    }
  }
  const onOut = (event: PointerEvent) => {
    if (isHot(event.target) && !isHot(event.relatedTarget)) {
      gsap.to(gauge.value, { scale: 1, duration: 0.35, ease: 'expo.out' })
    }
  }
  over = onOver
  out = onOut

  onScroll = (event) => {
    const limit = event.limit ?? Math.max(document.documentElement.scrollHeight - window.innerHeight, 1)
    const scrolled = event.progress ?? Math.min((event.scroll ?? window.scrollY) / limit, 1)
    if (event.direction === -1) reverse.value = true
    if (event.direction === 1) reverse.value = false
    applyProgress(scrolled)
  }

  applyProgress($lenis?.progress ?? 0)
  $lenis?.on('scroll', onScroll)

  window.addEventListener('mousemove', move)
  window.addEventListener('mousedown', down)
  window.addEventListener('mouseup', up)
  document.addEventListener('pointerover', onOver)
  document.addEventListener('pointerout', onOut)
})

onBeforeUnmount(() => {
  if (move) window.removeEventListener('mousemove', move)
  if (down) window.removeEventListener('mousedown', down)
  if (up) window.removeEventListener('mouseup', up)
  if (over) document.removeEventListener('pointerover', over)
  if (out) document.removeEventListener('pointerout', out)
  if (onScroll) $lenis?.off('scroll', onScroll)
})
</script>

<style scoped>
.cursor {
  position: fixed;
  inset: 0;
  pointer-events: none;
  z-index: 90;
}

.cursor__gauge {
  position: absolute;
  top: 0;
  left: 0;
  width: 48px;
  height: 48px;
  margin: -58px 0 0 14px;
  display: flex;
  align-items: center;
  justify-content: center;
  will-change: transform;
}

.cursor__svg {
  position: absolute;
  inset: 0;
  width: 48px;
  height: 48px;
  overflow: visible;
}

.cursor__track,
.cursor__progress {
  fill: none;
  stroke-width: 1.75;
}

.cursor__track {
  stroke: var(--cursor);
  opacity: 0.18;
}

.cursor__progress {
  stroke: var(--cursor);
  stroke-linecap: round;
  transform-origin: 24px 24px;
  transform: rotate(-90deg);
  transition: transform 0.35s cubic-bezier(0.16, 1, 0.3, 1);
}

.cursor__progress.is-reverse {
  transform: rotate(-90deg) scaleX(-1);
}

.cursor__pct {
  position: relative;
  z-index: 1;
  font-size: 10px;
  line-height: 1;
  font-weight: 600;
  letter-spacing: -0.04em;
  font-variant-numeric: tabular-nums;
  color: var(--cursor);
}

.cursor__pct small {
  font-size: 7px;
  font-weight: 600;
  margin-left: 0.5px;
}
</style>
