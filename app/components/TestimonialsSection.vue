<template>
  <section ref="root" class="feedback reveal">
    <h2 class="feedback__title font-display">Feedbacks from my colleagues and clients</h2>
    <div class="feedback__grid">
      <article
        v-for="item in testimonials"
        :key="item.name + item.quote"
        class="quote"
      >
        <p class="quote__text">{{ item.quote }}</p>
        <div class="quote__person">
          <span class="quote__avatar" :style="{ background: item.color }" aria-hidden="true">
            {{ initials(item.name) }}
          </span>
          <div>
            <p class="quote__name">{{ item.name }}</p>
            <p v-if="item.role" class="quote__role">{{ item.role }}</p>
          </div>
        </div>
      </article>
    </div>
  </section>
</template>

<script setup lang="ts">
import { testimonials } from '~/data/site'

const initials = (name: string) =>
  name
    .split(' ')
    .filter(Boolean)
    .slice(0, 2)
    .map(part => part[0] ?? '')
    .join('')
    .toUpperCase()

const root = ref<HTMLElement | null>(null)
const { $gsap } = useNuxtApp()
const { unfolded } = useBoot()
let bound = false

const bindHover = () => {
  const gsap = $gsap
  if (bound || !gsap || !root.value || !hasFinePointer() || prefersReducedMotion()) return
  bound = true

  const grid = root.value.querySelector<HTMLElement>('.feedback__grid')
  const quotes = Array.from(root.value.querySelectorAll<HTMLElement>('.quote'))
  if (!grid) return

  const focus = (active: HTMLElement | null) => {
    quotes.forEach((quote) => {
      const on = quote === active
      const back = Boolean(active) && !on
      const avatar = quote.querySelector<HTMLElement>('.quote__avatar')
      gsap.to(quote, {
        opacity: back ? 0.38 : 1,
        scale: back ? 0.94 : on ? 1.03 : 1,
        y: back ? 10 : on ? -8 : 0,
        duration: 0.85,
        ease: 'expo.out',
        overwrite: 'auto'
      })
      if (avatar) {
        gsap.to(avatar, {
          scale: on ? 1.12 : 1,
          rotate: on ? 8 : 0,
          filter: back ? 'saturate(0.65)' : 'saturate(1)',
          duration: 0.85,
          ease: 'expo.out'
        })
      }
    })
  }

  quotes.forEach((quote) => {
    quote.addEventListener('mouseenter', () => focus(quote))
  })
  grid.addEventListener('mouseleave', () => focus(null))
}

onMounted(() => {
  watch(unfolded, (value) => {
    if (value) nextTick(bindHover)
  }, { immediate: true })
})
</script>

<style scoped>
.feedback {
  display: flex;
  flex-direction: column;
  gap: 24px;
  width: 100%;
}

.feedback__title {
  font-size: 18px;
  line-height: 28px;
  font-weight: 600;
}

.feedback__grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 24px;
}

.quote {
  display: flex;
  flex-direction: column;
  gap: 16px;
  height: 100%;
  transform-origin: center center;
  will-change: transform, opacity;
}

.quote__text {
  color: var(--text-muted);
  font-size: 14px;
  line-height: 22px;
}

.quote__person {
  display: flex;
  align-items: center;
  gap: 8px;
}

.quote__avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  flex-shrink: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
  line-height: 1;
  font-weight: 600;
  letter-spacing: 0.04em;
  color: var(--text);
  transform-origin: center center;
}

.quote__name {
  font-size: 14px;
  line-height: 22px;
  color: var(--text);
}

.quote__role {
  font-size: 12px;
  line-height: 20px;
  color: var(--text-muted);
}

@media (min-width: 900px) {
  .feedback__grid {
    grid-template-columns: repeat(3, 1fr);
    gap: 20px 20px;
  }

  .quote:nth-child(-n + 3) {
    padding-bottom: 24px;
    border-bottom: 1px solid var(--border);
  }
}
</style>
