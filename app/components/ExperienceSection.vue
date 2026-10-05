<template>
  <section ref="root" class="experience reveal">
    <h2 class="experience__title font-display">My experience</h2>
    <ul class="experience__list">
      <li
        v-for="(item, index) in experience"
        :key="item.dates + item.role"
        class="experience__item"
        :class="{ 'is-open': openIndex === index }"
      >
        <button
          class="experience__trigger"
          type="button"
          :aria-expanded="openIndex === index"
          :aria-controls="`experience-panel-${index}`"
          @click="toggle(index)"
        >
          <span class="experience__brand">
            <span
              class="experience__mark"
              :class="{ 'is-inset': item.logoInset, 'is-wide': item.logoWide }"
            >
              <img
                class="experience__logo"
                :src="item.logo"
                :alt="item.role"
                :width="item.logoWide ? 124 : 40"
                height="40"
              >
            </span>
            <span class="experience__copy">
              <span class="experience__dates">{{ item.dates }}</span>
              <span class="experience__role">{{ item.role }}</span>
            </span>
          </span>
          <span class="experience__icon" aria-hidden="true">
            <img src="/icons/arrow-up.svg" alt="" width="16" height="16">
          </span>
        </button>
        <div
          :id="`experience-panel-${index}`"
          class="experience__panel"
          :ref="(el) => setPanel(el, index)"
        >
          <div class="experience__panel-inner">
            <p class="experience__summary">{{ item.summary }}</p>
          </div>
        </div>
      </li>
    </ul>
  </section>
</template>

<script setup lang="ts">
import { experience } from '~/data/site'

const root = ref<HTMLElement | null>(null)
const panels = ref<(HTMLElement | null)[]>([])
const openIndex = ref(0)
const { $gsap } = useNuxtApp()
const { unfolded } = useBoot()
let ready = false

const setPanel = (el: Element | null, index: number) => {
  panels.value[index] = el instanceof HTMLElement ? el : null
}

const animatePanel = (index: number, open: boolean, instant = false) => {
  const gsap = $gsap
  const panel = panels.value[index]
  if (!gsap || !panel) return

  const inner = panel.querySelector<HTMLElement>('.experience__panel-inner')
  const bits = panel.querySelectorAll<HTMLElement>('.experience__summary')

  if (prefersReducedMotion() || instant) {
    gsap.set(panel, { height: open ? 'auto' : 0, overflow: 'hidden' })
    if (inner) gsap.set(inner, { opacity: open ? 1 : 0, y: 0 })
    bits.forEach(bit => gsap.set(bit, { opacity: open ? 1 : 0, y: 0 }))
    return
  }

  if (open) {
    gsap.set(panel, { height: 'auto', overflow: 'hidden' })
    const height = panel.offsetHeight
    gsap.fromTo(panel, { height: 0 }, {
      height,
      duration: 0.72,
      ease: 'expo.out',
      onComplete: () => gsap.set(panel, { height: 'auto' })
    })
    if (inner) {
      gsap.fromTo(inner, { opacity: 0, y: 16 }, {
        opacity: 1,
        y: 0,
        duration: 0.65,
        delay: 0.06,
        ease: 'expo.out'
      })
    }
    if (bits.length) {
      gsap.fromTo(bits, { opacity: 0, y: 14 }, {
        opacity: 1,
        y: 0,
        duration: 0.55,
        delay: 0.12,
        stagger: 0.055,
        ease: 'expo.out'
      })
    }
    return
  }

  gsap.to(panel, { height: 0, duration: 0.5, ease: 'expo.inOut', overflow: 'hidden' })
  if (inner) gsap.to(inner, { opacity: 0, y: 10, duration: 0.32, ease: 'power2.in' })
  if (bits.length) gsap.to(bits, { opacity: 0, y: 6, duration: 0.22, stagger: 0.02, ease: 'power2.in' })
}

const toggle = (index: number) => {
  const previous = openIndex.value
  if (previous === index) {
    openIndex.value = -1
    animatePanel(index, false)
    return
  }

  if (previous !== -1) animatePanel(previous, false)
  openIndex.value = index
  nextTick(() => animatePanel(index, true))
}

onMounted(() => {
  watch(unfolded, (value) => {
    if (!value || ready) return
    ready = true
    nextTick(() => {
      panels.value.forEach((panel, index) => {
        if (!panel) return
        $gsap?.set(panel, { height: index === openIndex.value ? 'auto' : 0, overflow: 'hidden' })
        if (index === openIndex.value) animatePanel(index, true, true)
      })
    })
  }, { immediate: true })
})
</script>

<style scoped>
.experience {
  display: flex;
  flex-direction: column;
  gap: 24px;
  width: 100%;
}

.experience__title {
  font-size: 18px;
  line-height: 28px;
  font-weight: 600;
}

.experience__list {
  width: 100%;
}

.experience__item {
  border-bottom: 1px solid var(--border);
}

.experience__trigger {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  width: 100%;
  padding: 16px 0;
  text-align: left;
}

.experience__brand {
  display: flex;
  align-items: center;
  gap: 14px;
  min-width: 0;
}

.experience__mark {
  width: 40px;
  height: 40px;
  border-radius: 10px;
  flex-shrink: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
  background: #fff;
  transition: transform 0.55s cubic-bezier(0.16, 1, 0.3, 1);
}

.experience__mark.is-inset {
  padding: 8px;
}

.experience__mark.is-wide {
  width: 124px;
  padding: 8px 12px;
}

.experience__item.is-open .experience__mark {
  transform: scale(1.06);
}

.experience__logo {
  width: 100%;
  height: 100%;
  display: block;
  object-fit: cover;
  filter: none;
}

.experience__mark.is-inset .experience__logo,
.experience__mark.is-wide .experience__logo {
  object-fit: contain;
  object-position: center;
}

.experience__copy {
  display: flex;
  flex-direction: column;
  gap: 4px;
  min-width: 0;
}

.experience__dates {
  font-size: 16px;
  line-height: 24px;
  color: var(--text);
}

.experience__role {
  font-size: 14px;
  line-height: 22px;
  color: var(--text-muted);
}

.experience__icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 24px;
  height: 24px;
  flex-shrink: 0;
  transform: rotate(90deg);
  transition: transform 0.55s cubic-bezier(0.16, 1, 0.3, 1);
}

.experience__item.is-open .experience__icon {
  transform: rotate(180deg);
}

.experience__icon img {
  width: 16px;
  height: 16px;
}

[data-theme='dark'] .experience__icon img {
  filter: invert(1);
}

.experience__panel {
  height: 0;
  overflow: hidden;
}

.experience__panel-inner {
  padding: 0 40px 24px 54px;
}

.experience__summary {
  font-size: 14px;
  line-height: 22px;
  color: var(--text-muted);
  max-width: 640px;
}

@media (max-width: 899px) {
  .experience__dates,
  .experience__role,
  .experience__summary {
    font-size: 14px;
    line-height: 22px;
  }

  .experience__mark {
    width: 36px;
    height: 36px;
    border-radius: 9px;
  }

  .experience__mark.is-inset {
    padding: 7px;
  }

  .experience__mark.is-wide {
    width: 110px;
    padding: 8px 10px;
  }

  .experience__panel-inner {
    padding: 0 8px 20px 50px;
  }
}
</style>
