<template>
  <div ref="root" class="fan" aria-hidden="true">
    <div class="fan__stage">
      <div
        v-for="(card, index) in heroCards"
        :key="index"
        class="fan__item"
        :class="`fan__item--${index}`"
      >
        <div class="fan__float">
          <div class="fan__card">
            <div class="fan__fill" :style="{ background: card.color }">
              <img
                class="fan__photo"
                :src="card.image"
                :style="{ objectPosition: card.position }"
                :width="index === 3 ? 1638 : 1920"
                :height="2560"
                alt=""
                decoding="async"
                fetchpriority="high"
                draggable="false"
              >
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { heroCards } from '~/data/site'

const positions = [0, 222, 444, 667]
const center = 333
const root = ref<HTMLElement | null>(null)
const { $gsap } = useNuxtApp()
const { unfolded } = useBoot()
let played = false

const playFan = () => {
  const gsap = $gsap
  if (played || !gsap || !root.value) return
  played = true

  const items = Array.from(root.value.querySelectorAll<HTMLElement>('.fan__item'))
  const floats = Array.from(root.value.querySelectorAll<HTMLElement>('.fan__float'))
  const cards = Array.from(root.value.querySelectorAll<HTMLElement>('.fan__card'))
  const fills = Array.from(root.value.querySelectorAll<HTMLElement>('.fan__fill'))

  if (prefersReducedMotion()) {
    cards.forEach((card, index) => {
      gsap.set(card, { rotate: heroCards[index].rotate })
    })
    return
  }

  const desktop = window.matchMedia('(min-width: 900px)').matches

  if (desktop) {
    items.forEach((item, index) => {
      gsap.set(item, { x: center - positions[index], y: 48, scale: 0.9, zIndex: index })
      gsap.set(cards[index], { rotate: 0 })
    })

    const tl = gsap.timeline({ delay: 0.12 })
    tl.to(items, {
      x: 0,
      y: 0,
      scale: 1,
      duration: 1.6,
      stagger: 0.09,
      ease: 'expo.inOut'
    }, 0)
    tl.to(cards, {
      rotate: (i: number) => heroCards[i].rotate,
      duration: 1.6,
      stagger: 0.09,
      ease: 'expo.inOut'
    }, 0)
  } else {
    gsap.fromTo(items, {
      y: 80,
      opacity: 0,
      scale: 0.94
    }, {
      y: 0,
      opacity: 1,
      scale: 1,
      duration: 1.2,
      stagger: 0.1,
      ease: 'expo.out'
    })
    cards.forEach((card, index) => {
      gsap.fromTo(card, { rotate: 0 }, {
        rotate: heroCards[index].rotate,
        duration: 1.2,
        delay: index * 0.1,
        ease: 'expo.out'
      })
    })
  }

  floats.forEach((float, index) => {
    gsap.to(float, {
      y: index % 2 === 0 ? -10 : 12,
      duration: 4.2 + index * 0.3,
      yoyo: true,
      repeat: -1,
      ease: 'sine.inOut',
      delay: 1.6 + index * 0.12
    })
  })

  if (!hasFinePointer()) return

  const focus = (active: number | null) => {
    items.forEach((item, index) => {
      const on = active === index
      const back = active !== null && !on
      gsap.to(item, {
        opacity: back ? 0.38 : 1,
        scale: back ? 0.92 : on ? 1.05 : 1,
        zIndex: on ? 20 : index + 1,
        duration: 0.85,
        ease: 'expo.out',
        overwrite: 'auto'
      })
      gsap.to(fills[index], {
        scale: on ? 1.1 : 1,
        filter: back ? 'saturate(0.65)' : 'saturate(1)',
        duration: 0.95,
        ease: 'expo.out',
        overwrite: 'auto'
      })
      gsap.to(cards[index], {
        rotate: heroCards[index].rotate * (on ? 1.18 : 1),
        duration: 1,
        ease: 'expo.out'
      })
      if (!on) gsap.to(fills[index], { x: 0, y: 0, duration: 0.9, ease: 'expo.out' })
    })
  }

  items.forEach((item, index) => {
    const fill = fills[index]
    const xTo = gsap.quickTo(fill, 'x', { duration: 0.95, ease: 'expo.out' })
    const yTo = gsap.quickTo(fill, 'y', { duration: 0.95, ease: 'expo.out' })

    item.addEventListener('mouseenter', () => focus(index))
    item.addEventListener('mousemove', (event) => {
      const rect = item.getBoundingClientRect()
      const x = (event.clientX - (rect.left + rect.width / 2)) / rect.width
      const y = (event.clientY - (rect.top + rect.height / 2)) / rect.height
      xTo(x * 10)
      yTo(y * 8)
    })
  })
  root.value.addEventListener('mouseleave', () => focus(null))
}

onMounted(() => {
  const gsap = $gsap
  if (gsap && root.value && window.matchMedia('(min-width: 900px)').matches) {
    const items = Array.from(root.value.querySelectorAll<HTMLElement>('.fan__item'))
    const cards = Array.from(root.value.querySelectorAll<HTMLElement>('.fan__card'))
    items.forEach((item, index) => {
      gsap.set(item, { x: center - positions[index], y: 48, scale: 0.9, zIndex: index })
      gsap.set(cards[index], { rotate: 0 })
    })
  }

  watch(unfolded, (value) => {
    if (value) playFan()
  }, { immediate: true })
})
</script>

<style scoped>
.fan {
  position: relative;
  width: min(1009px, 100%);
  margin: 48px auto 0;
  container-type: inline-size;
  aspect-ratio: 1009 / 388;
}

.fan__stage {
  position: absolute;
  inset: 0;
  width: 1009px;
  height: 388px;
  transform-origin: top left;
  transform: scale(calc(100cqi / 1009));
}

.fan__item {
  position: absolute;
  top: 0;
  width: 342px;
  height: 388px;
  display: flex;
  align-items: center;
  justify-content: center;
  will-change: transform, opacity;
}

.fan__float {
  will-change: transform;
}

.fan__card {
  width: 266px;
  height: 331px;
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 18px 40px rgba(0, 0, 0, 0.08);
  will-change: transform;
}

.fan__fill {
  width: 118%;
  height: 118%;
  margin: -9%;
  will-change: transform;
  transform: translateZ(0);
}

.fan__photo {
  width: 100%;
  height: 100%;
  max-width: none;
  object-fit: cover;
  backface-visibility: hidden;
  transform: translateZ(0);
}

.fan__item--0 { left: 0; z-index: 1; }
.fan__item--1 { left: 222px; z-index: 3; }
.fan__item--2 { left: 444px; z-index: 2; }
.fan__item--3 { left: 667px; z-index: 4; }

@media (max-width: 899px) {
  .fan {
    width: min(680px, calc(100% - 32px));
    height: auto;
    min-height: 0;
    aspect-ratio: auto;
    margin: 48px auto 0;
    display: block;
  }

  .fan__stage {
    position: relative;
    width: 100%;
    height: auto;
    transform: none;
    display: flex;
    flex-direction: column;
    align-items: center;
  }

  .fan__item {
    position: relative;
    left: auto !important;
    top: auto;
    width: min(340px, 100%);
    height: 380px;
    margin-bottom: -96px;
    cursor: auto;
  }

  .fan__item:last-child {
    margin-bottom: 0;
  }

  .fan__card {
    width: min(268px, 86%);
    height: 334px;
    border-radius: 14.5px;
  }
}
</style>
