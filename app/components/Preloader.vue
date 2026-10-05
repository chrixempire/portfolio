<template>
  <Transition name="preloader">
    <div v-if="visible" class="preloader" aria-hidden="true">
      <div class="preloader__inner">
        <p ref="nameRef" class="preloader__name font-display">{{ site.name }}</p>
        <div class="preloader__bar">
          <span ref="barRef" class="preloader__fill" />
        </div>
      </div>
    </div>
  </Transition>
</template>

<script setup lang="ts">
import { site } from '~/data/site'

const visible = defineModel<boolean>({ default: true })
const nameRef = ref<HTMLElement | null>(null)
const barRef = ref<HTMLElement | null>(null)
const { $gsap } = useNuxtApp()
const { finishBoot } = useBoot()

onMounted(() => {
  const gsap = $gsap
  if (!gsap) {
    visible.value = false
    finishBoot()
    return
  }

  const tl = gsap.timeline({
    onComplete: () => {
      visible.value = false
      finishBoot()
    }
  })

  tl.fromTo(nameRef.value, { y: 24, opacity: 0 }, { y: 0, opacity: 1, duration: 0.6, ease: 'power3.out' })
    .fromTo(barRef.value, { scaleX: 0 }, { scaleX: 1, duration: 0.9, ease: 'power2.inOut' }, '-=0.15')
    .to(nameRef.value, { y: -16, opacity: 0, duration: 0.4, ease: 'power2.in' }, '+=0.15')
})
</script>

<style scoped>
.preloader {
  position: fixed;
  inset: 0;
  z-index: 80;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--bg);
}

.preloader__inner {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 16px;
}

.preloader__name {
  font-size: 18px;
  line-height: 28px;
  font-weight: 600;
}

.preloader__bar {
  width: 120px;
  height: 2px;
  background: var(--surface);
  overflow: hidden;
  border-radius: 2px;
}

.preloader__fill {
  display: block;
  width: 100%;
  height: 100%;
  background: var(--text);
  transform-origin: left center;
}

.preloader-enter-active,
.preloader-leave-active {
  transition: opacity 0.45s ease, transform 0.45s ease;
}

.preloader-leave-to {
  opacity: 0;
  transform: translateY(-8px);
}
</style>
