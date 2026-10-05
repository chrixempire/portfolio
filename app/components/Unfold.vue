<template>
  <div v-if="visible" class="unfold" aria-hidden="true">
    <div ref="top" class="unfold__panel unfold__panel--top" />
    <div ref="bottom" class="unfold__panel unfold__panel--bottom" />
  </div>
</template>

<script setup lang="ts">
const visible = ref(true)
const top = ref<HTMLElement | null>(null)
const bottom = ref<HTMLElement | null>(null)
const { $gsap } = useNuxtApp()
const { booting, finishUnfold } = useBoot()
let played = false

const play = () => {
  if (played) return
  played = true
  const gsap = $gsap

  if (!gsap || prefersReducedMotion()) {
    visible.value = false
    finishUnfold()
    return
  }

  const tl = gsap.timeline({
    delay: 0.12,
    onComplete: () => {
      visible.value = false
      finishUnfold()
    }
  })

  tl.to(top.value, { yPercent: -110, duration: 1.15, ease: 'power4.inOut' }, 0)
    .to(bottom.value, { yPercent: 110, duration: 1.15, ease: 'power4.inOut' }, 0)
}

onMounted(() => {
  watch(booting, (value) => {
    if (!value) play()
  }, { immediate: true })
})
</script>

<style scoped>
.unfold {
  position: fixed;
  inset: 0;
  z-index: 70;
  pointer-events: none;
  overflow: hidden;
}

.unfold__panel {
  position: absolute;
  left: 0;
  width: 100%;
  height: 52%;
  background: var(--bg);
}

.unfold__panel--top {
  top: 0;
  border-bottom: 1px solid var(--border);
}

.unfold__panel--bottom {
  bottom: 0;
  border-top: 1px solid var(--border);
}
</style>
