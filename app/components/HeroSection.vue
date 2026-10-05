<template>
  <section id="top" class="hero">
    <div class="hero__copy">
      <h1 ref="headline" class="hero__headline font-display">
        {{ site.headline }}
      </h1>
      <div ref="actions" class="hero__actions">
        <MagneticButton :href="site.calendly" external>Schedule an intro</MagneticButton>
        <MagneticButton variant="secondary" :href="`mailto:${site.email}`">Send email</MagneticButton>
        <MagneticButton variant="secondary" :href="site.resumeHref" :download="site.resumeFileName">Download resume</MagneticButton>
      </div>
    </div>
    <HeroCards />
  </section>
</template>

<script setup lang="ts">
import { site } from '~/data/site'

const headline = ref<HTMLElement | null>(null)
const actions = ref<HTMLElement | null>(null)
const { $gsap, $SplitText } = useNuxtApp()
const { unfolded } = useBoot()
let played = false

const playIntro = async () => {
  const gsap = $gsap
  const SplitText = $SplitText
  if (played || !gsap || !headline.value) return
  played = true
  if (!SplitText || prefersReducedMotion()) {
    gsap.set([headline.value, actions.value], { opacity: 1, y: 0 })
    return
  }

  await document.fonts?.ready.catch(() => undefined)
  const split = new SplitText(headline.value, { type: 'words,chars', wordsClass: 'word' })
  gsap.set(headline.value, { opacity: 1 })
  gsap.from(split.chars, {
    yPercent: 120,
    rotateZ: 8,
    opacity: 0,
    stagger: 0.016,
    duration: 1.1,
    ease: 'power4.out'
  })
  gsap.fromTo(actions.value, {
    y: 36,
    opacity: 0
  }, {
    y: 0,
    opacity: 1,
    duration: 0.95,
    ease: 'power3.out',
    delay: 0.32
  })
}

onMounted(() => {
  if ($gsap && actions.value && !prefersReducedMotion()) {
    $gsap.set(actions.value, { opacity: 0, y: 36 })
  }
  watch(unfolded, (value) => {
    if (value) playIntro()
  }, { immediate: true })
})
</script>

<style scoped>
.hero {
  width: min(1009px, 100%);
  margin: 0 auto;
  padding-top: 92px;
}

.hero__copy {
  width: min(696px, calc(100% - 40px));
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  gap: 24px;
  align-items: flex-start;
}

.hero__headline {
  font-size: 32px;
  line-height: 42px;
  font-weight: 600;
  color: var(--text);
  overflow: hidden;
  opacity: 0;
}

.hero__headline :deep(.word) {
  overflow: hidden;
  display: inline-block;
  vertical-align: top;
  padding-bottom: 0.12em;
  margin-bottom: -0.12em;
}

.hero__actions {
  display: flex;
  gap: 16px;
  align-items: flex-start;
  flex-wrap: wrap;
  will-change: transform, opacity;
}

@media (max-width: 899px) {
  .hero {
    padding-top: 79px;
  }

  .hero__copy {
    width: min(680px, calc(100% - 32px));
  }

  .hero__headline {
    font-size: 24px;
    line-height: 32px;
  }
}
</style>
