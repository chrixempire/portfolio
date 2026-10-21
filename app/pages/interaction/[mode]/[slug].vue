<template>
  <main v-if="entry" class="page">
    <article class="sheet" :class="{ 'sheet--wide': entry.wide }">
      <header class="intro">
        <p class="kicker">Interaction</p>
        <h1 class="title font-display">{{ entry.title }}</h1>
        <p class="prompt">{{ entry.prompt }}</p>
      </header>

      <section
        v-if="entry.stage === 'stack'"
        class="notes notes--before"
        :aria-label="`${entry.title} notes`"
      >
        <h2 class="notes__label">Where it came from</h2>
        <p class="notes__body">{{ entry.idea }}</p>
        <p class="sources">
          <a
            v-for="source in entry.sources"
            :key="source.href"
            :href="source.href"
            target="_blank"
            rel="noopener noreferrer"
          >{{ source.label }}</a>
        </p>

        <h2 class="notes__label">How I built it</h2>
        <p v-for="paragraph in entry.how" :key="paragraph" class="notes__body">
          {{ paragraph }}
        </p>
      </section>

      <div
        v-if="entry.stage !== 'stack'"
        class="stage"
        :class="`stage--${entry.stage}`"
        :aria-label="entry.title"
      >
        <CommandSearch v-if="entry.slug === 'command-search'" />
        <ApplePlayButton v-else-if="entry.slug === 'play-button'" />
        <ExpandableCard v-else-if="entry.slug === 'card-expand'" />
        <HoverExpand v-else-if="entry.slug === 'hover-expand'" />
        <ClientOnly v-else-if="entry.slug === 'creative-carousel'">
          <CreativeCarousel />
        </ClientOnly>
        <BouncyAccordion v-else-if="entry.slug === 'bouncy-accordion'" />
        <div v-else-if="entry.slug === 'otp-input'" class="otp-demo">
          <OtpInput
            :status="otpStatus"
            @change="onOtpChange"
            @complete="onOtpComplete"
          />
          <p class="otp-demo__hint">Enter 123456 to pass. Any other code fails.</p>
        </div>
      </div>
    </article>

    <StickyCards v-if="entry.stage === 'stack'" />

    <section v-if="entry.stage !== 'stack'" class="notes" :aria-label="`${entry.title} notes`">
      <h2 class="notes__label">Where it came from</h2>
      <p class="notes__body">{{ entry.idea }}</p>
      <p class="sources">
        <a
          v-for="source in entry.sources"
          :key="source.href"
          :href="source.href"
          target="_blank"
          rel="noopener noreferrer"
        >{{ source.label }}</a>
      </p>

      <h2 class="notes__label">How I built it</h2>
      <p v-for="paragraph in entry.how" :key="paragraph" class="notes__body">
        {{ paragraph }}
      </p>
    </section>

    <div v-if="mode === '04'" class="study-bottom">
      <div class="study-bottom__landscape" aria-hidden="true">
        <div class="study-bottom__photo">
          <img src="/images/footer-landscape.png" alt="" width="1920" height="1076">
        </div>
        <div class="study-bottom__veil" />
      </div>
      <AppFooter />
    </div>
    <AppFooter v-else />
  </main>
</template>

<script setup lang="ts">
import { interactionBySlug } from '~/data/interactions'

type OtpStatus = 'idle' | 'success' | 'error'

const route = useRoute()
const mode = computed(() => String(route.params.mode || ''))
const slug = computed(() => String(route.params.slug || ''))
const entry = computed(() => {
  if (mode.value !== '2032' && mode.value !== '04') return undefined
  return interactionBySlug(slug.value)
})

watch(entry, (value) => {
  if (!value) {
    throw createError({ statusCode: 404, statusMessage: 'Interaction not found', fatal: true })
  }
}, { immediate: true })

const title = computed(() => entry.value ? `${entry.value.title} - Christian Anyikamadu` : 'Interaction')
const description = computed(() => entry.value?.idea ?? '')

useSiteSeo({ title, description })

const otpStatus = ref<OtpStatus>('idle')

const onOtpChange = () => {
  otpStatus.value = 'idle'
}

const onOtpComplete = (code: string) => {
  otpStatus.value = code === '123456' ? 'success' : 'error'
}

watch(slug, () => {
  otpStatus.value = 'idle'
})
</script>

<style scoped>
.page {
  width: 100%;
}

.sheet {
  width: min(896px, calc(100% - 40px));
  margin: 0 auto;
  padding-top: 48px;
}

.sheet--wide {
  width: min(1152px, calc(100% - 40px));
}

.intro {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
  width: min(640px, 100%);
  margin: 0 auto;
  text-align: center;
}

.kicker {
  font-size: 12px;
  line-height: 18px;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: var(--text-muted);
}

.title {
  font-size: 40px;
  line-height: 52px;
  font-weight: 600;
  color: var(--text);
}

.prompt {
  color: var(--text-muted);
}

.stage {
  width: 100%;
  margin-top: 40px;
  min-height: 420px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 32px;
  background: #0a0a0a;
}

.stage--search {
  min-height: 720px;
  background: #121212;
}

.stage--hover {
  min-height: 420px;
  padding: 32px 20px;
  overflow-x: auto;
}

.stage--carousel {
  min-height: 500px;
  padding: 40px 0 24px;
  overflow: visible;
}

.stage--otp {
  min-height: 420px;
}

.stage--accordion {
  min-height: 520px;
  background: #121212;
}

.otp-demo {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 24px;
}

.otp-demo__hint {
  font-size: 14px;
  line-height: 22px;
  color: #a1a1a1;
  text-align: center;
}

.notes {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
  width: min(640px, calc(100% - 40px));
  margin: 48px auto 0;
  text-align: center;
}

.notes--before {
  width: min(640px, 100%);
  margin: 36px auto 8px;
}

.notes__label {
  margin-top: 16px;
  font-size: 12px;
  line-height: 18px;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  font-weight: 500;
  color: var(--text-muted);
}

.notes__body {
  color: var(--text);
}

.sources {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 8px 16px;
}

.sources a {
  color: var(--text-nav);
  text-decoration: underline;
  text-decoration-style: dotted;
  text-underline-offset: 3px;
}

.study-bottom {
  position: relative;
  margin-top: 48px;
  min-height: 520px;
  display: flex;
  flex-direction: column;
  justify-content: flex-end;
  overflow: hidden;
  background: var(--bg);
}

.study-bottom :deep(.footer) {
  position: relative;
  z-index: 1;
}

.study-bottom__landscape {
  position: absolute;
  left: 0;
  right: 0;
  bottom: 0;
  height: 841px;
  max-height: 100%;
  pointer-events: none;
  mix-blend-mode: luminosity;
}

.study-bottom__photo {
  position: absolute;
  inset: 0;
  overflow: hidden;
  opacity: 0.2;
}

.study-bottom__photo img {
  position: absolute;
  top: 0;
  left: -25.37%;
  width: 125.37%;
  height: 120.36%;
  max-width: none;
  object-fit: cover;
}

.study-bottom__veil {
  position: absolute;
  inset: 0;
  background: var(--footer-veil);
}

@media (max-width: 899px) {
  .sheet,
  .sheet--wide {
    width: min(373px, calc(100% - 40px));
  }

  .title {
    font-size: 32px;
    line-height: 40px;
  }

  .stage {
    min-height: 360px;
    border-radius: 24px;
  }

  .stage--search {
    min-height: 700px;
  }

  .study-bottom {
    min-height: 444px;
  }

  .study-bottom__landscape {
    height: 444px;
    width: 202.933%;
    left: -62.933%;
    right: auto;
  }
}
</style>
