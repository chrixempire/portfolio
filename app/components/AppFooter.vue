<template>
  <footer ref="root" class="footer">
    <div class="footer__inner">
      <div class="footer__top">
        <div class="footer__hello">
          <p class="footer__label">Say hello</p>
          <a class="footer__email" :href="`tel:${site.phone}`">{{ site.phoneDisplay }}</a>
          <span class="footer__email-row">
            <a class="footer__email" :href="site.gmail" target="_blank" rel="noopener noreferrer">{{ site.email }}</a>
            <button
              class="footer__copy"
              type="button"
              :aria-label="copied ? 'Email copied' : 'Copy email'"
              @click="copyEmail"
            >
              <img :src="copied ? '/icons/check.svg' : '/icons/copy.svg'" alt="" width="10" height="10">
            </button>
          </span>
          <a v-if="!isStudy" class="footer__schedule" :href="site.calendly" target="_blank" rel="noopener noreferrer">
            Schedule an intro
          </a>
        </div>
        <div class="footer__socials">
          <a
            v-for="social in site.socials"
            :key="social.label"
            class="footer__social"
            :href="social.href"
            target="_blank"
            rel="noopener noreferrer"
          >
            {{ social.label }}
          </a>
        </div>
      </div>
    </div>
    <NameBand v-if="!isStudy" />
    <p class="footer__copywrite">
      Maintain by {{ site.name }} © 2026 - All rights reserved
    </p>
  </footer>
</template>

<script setup lang="ts">
import { site } from '~/data/site'

const route = useRoute()
const isStudy = computed(() => /^\/interaction\/04\/[^/]+/.test(route.path))
const root = ref<HTMLElement | null>(null)
const copied = ref(false)
const { $gsap } = useNuxtApp()
const { unfolded } = useBoot()
let bound = false

const copyEmail = async () => {
  try {
    await navigator.clipboard.writeText(site.email)
    copied.value = true
    setTimeout(() => { copied.value = false }, 1800)
  } catch {
    copied.value = false
  }
}

const bindHover = () => {
  const gsap = $gsap
  if (bound || !gsap || !root.value || !hasFinePointer() || prefersReducedMotion()) return
  bound = true

  const hoverLink = (el: HTMLElement, extra?: HTMLElement | null) => {
    el.addEventListener('mouseenter', () => {
      gsap.to(el, { y: -3, color: 'var(--text)', duration: 0.55, ease: 'expo.out' })
      if (extra) gsap.to(extra, { scale: 1.15, rotate: 10, duration: 0.55, ease: 'expo.out' })
    })
    el.addEventListener('mouseleave', () => {
      gsap.to(el, { y: 0, color: 'var(--text-nav)', duration: 0.6, ease: 'expo.out' })
      if (extra) gsap.to(extra, { scale: 1, rotate: 0, duration: 0.55, ease: 'expo.out' })
    })
  }

  const email = root.value.querySelector<HTMLElement>('.footer__email-row')
  if (email) hoverLink(email, root.value.querySelector('.footer__copy'))
  root.value.querySelectorAll<HTMLElement>('.footer__social, .footer__schedule').forEach((link) => hoverLink(link))
}

onMounted(() => {
  watch(unfolded, (value) => {
    if (value) nextTick(bindHover)
  }, { immediate: true })
})
</script>

<style scoped>
.footer {
  position: relative;
  width: 100%;
  margin: 0 auto;
  padding: 64px 0 48px;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.footer__inner {
  width: min(840px, calc(100% - 40px));
}

.footer__top {
  display: flex;
  align-items: flex-end;
  justify-content: space-between;
  width: 100%;
  gap: 24px;
}

.footer__hello {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.footer__label,
.footer__copywrite {
  font-size: 14px;
  line-height: 22px;
  color: var(--text-footer);
}

.footer__email-row {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  width: fit-content;
}

.footer__email,
.footer__schedule {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  color: var(--text-nav);
  text-decoration: underline;
  text-decoration-style: dotted;
  text-underline-offset: 3px;
  width: fit-content;
}

.footer__copy {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 16px;
  height: 16px;
  border-radius: 4px;
  background: var(--icon-bg);
  overflow: clip;
}

.footer__copy img {
  width: 10px;
  height: 10px;
}

[data-theme='dark'] .footer__copy img,
[data-theme='dark'] .product__arrow img {
  filter: invert(1);
}

.footer__socials {
  display: flex;
  gap: 16px;
}

.footer__social {
  color: var(--text-nav);
  text-decoration: underline;
  text-decoration-style: dotted;
  text-underline-offset: 3px;
}

.footer__copywrite {
  text-align: center;
  width: 100%;
  padding-top: 24px;
}

@media (max-width: 899px) {
  .footer__inner {
    width: min(373px, calc(100% - 40px));
  }

  .footer__top {
    flex-direction: column;
    align-items: flex-start;
    gap: 16px;
  }

  .footer__socials {
    flex-direction: column;
    gap: 16px;
  }

  .footer__email,
  .footer__social,
  .footer__schedule {
    color: var(--text);
  }
}
</style>
