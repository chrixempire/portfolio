<template>
  <div ref="root" class="nameband" aria-hidden="true">
    <div class="nameband__mask">
      <div ref="track" class="nameband__track">
        <span
          v-for="index in 3"
          :key="index"
          class="nameband__name font-display"
        >
          <span
            v-for="word in site.name.split(' ')"
            :key="word"
            class="nameband__word"
          >{{ word }}</span>
        </span>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { site } from '~/data/site'

const root = ref<HTMLElement | null>(null)
const track = ref<HTMLElement | null>(null)
const { $gsap, $SplitText, $lenis, $ScrollTrigger } = useNuxtApp()
const { unfolded } = useBoot()
let bound = false

const bind = async () => {
  const gsap = $gsap
  const SplitText = $SplitText
  if (bound || !gsap || !root.value || !track.value) return
  bound = true

  if (prefersReducedMotion()) return

  await document.fonts?.ready.catch(() => undefined)

  const words = Array.from(track.value.querySelectorAll<HTMLElement>('.nameband__word'))
  if (SplitText) {
    const split = new SplitText(words, { type: 'chars', charsClass: 'nameband__char', reduceWhiteSpace: false })
    gsap.set(split.chars, { yPercent: 110, opacity: 0 })
    gsap.to(split.chars, {
      yPercent: 0,
      opacity: 1,
      duration: 1.15,
      stagger: 0.028,
      ease: 'expo.out',
      scrollTrigger: {
        trigger: root.value,
        start: 'top 92%',
        once: true
      }
    })
  }

  const loop = track.value.scrollWidth / 3
  const tween = gsap.to(track.value, {
    x: -loop,
    duration: 42,
    ease: 'none',
    repeat: -1,
    delay: 0.7
  })

  const onScroll = (event: { velocity?: number }) => {
    const speed = 1 + Math.min(Math.abs(event.velocity ?? 0) * 0.4, 2.8)
    tween.timeScale(speed)
  }
  $lenis?.on('scroll', onScroll)

  $ScrollTrigger?.refresh()
}

onMounted(() => {
  watch(unfolded, (value) => {
    if (value) nextTick(bind)
  }, { immediate: true })
})
</script>

<style scoped>
.nameband {
  width: 100%;
  overflow: hidden;
  padding: 36px 0 20px;
  mask-image: linear-gradient(90deg, transparent 0%, #000 7%, #000 93%, transparent 100%);
}

.nameband__mask {
  overflow: hidden;
}

.nameband__track {
  display: flex;
  width: max-content;
  will-change: transform;
}

.nameband__name {
  display: inline-flex;
  align-items: baseline;
  gap: 0.7em;
  padding-right: 1.1em;
  overflow: hidden;
}

.nameband__word {
  display: inline-flex;
  overflow: hidden;
  font-size: clamp(64px, 12.5vw, 152px);
  line-height: 0.9;
  font-weight: 700;
  letter-spacing: -0.04em;
  color: var(--text);
  white-space: nowrap;
  padding-bottom: 0.06em;
}

.nameband__word :deep(.nameband__char) {
  display: inline-block;
  will-change: transform;
}

@media (max-width: 899px) {
  .nameband {
    padding: 20px 0 12px;
  }

  .nameband__word {
    font-size: clamp(44px, 16vw, 80px);
    letter-spacing: -0.035em;
  }

  .nameband__name {
    gap: 0.5em;
    padding-right: 0.8em;
  }
}
</style>
