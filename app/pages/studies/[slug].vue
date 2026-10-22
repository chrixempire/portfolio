<template>
  <DraftFrame>
    <article v-if="entry" class="study">
      <p class="crumbs">
        <NuxtLink to="/">Home</NuxtLink>
        <span aria-hidden="true">/</span>
        <NuxtLink to="/studies">Studies</NuxtLink>
        <span aria-hidden="true">/</span>
        <span>{{ entry.title }}</span>
      </p>

      <h1 class="study__title">{{ entry.title }}</h1>
      <p class="study__lead">{{ entry.idea }}</p>

      <div
        v-if="entry.slug !== 'scroll-stack'"
        class="stage"
        :class="{
          'stage--search': entry.slug === 'command-search',
          'stage--wide': entry.slug === 'hover-expand',
          'stage--carousel': entry.slug === 'creative-carousel'
        }"
      >
        <CommandSearch v-if="entry.slug === 'command-search'" />
        <ApplePlayButton v-else-if="entry.slug === 'play-button'" />
        <ExpandableCard v-else-if="entry.slug === 'card-expand'" />
        <HoverExpand v-else-if="entry.slug === 'hover-expand'" />
        <CreativeCarousel v-else-if="entry.slug === 'creative-carousel'" />
        <BouncyAccordion v-else-if="entry.slug === 'bouncy-accordion'" />
        <div v-else-if="entry.slug === 'otp-input'" class="otp">
          <OtpInput
            :status="otpStatus"
            @change="otpStatus = 'idle'"
            @complete="onOtpComplete"
          />
          <p class="otp__hint">Enter 123456 to pass. Any other code fails.</p>
        </div>
      </div>
      <StickyCards v-else />

      <h2>How it works</h2>
      <p v-for="paragraph in entry.how" :key="paragraph">{{ paragraph }}</p>

      <h2>Code</h2>
      <pre class="code"><code>{{ snippets[entry.slug] }}</code></pre>

      <p class="sources">
        <a
          v-for="source in entry.sources"
          :key="source.href"
          :href="source.href"
          target="_blank"
          rel="noopener noreferrer"
        >{{ source.label }}</a>
      </p>
    </article>
  </DraftFrame>
</template>

<script setup lang="ts">
import { interactionBySlug } from '~/data/interactions'

const route = useRoute()
const slug = computed(() => String(route.params.slug || ''))
const entry = computed(() => interactionBySlug(slug.value))

watch(entry, (value) => {
  if (!value) {
    throw createError({ statusCode: 404, statusMessage: 'Study not found', fatal: true })
  }
}, { immediate: true })

const title = computed(() => entry.value ? `${entry.value.title} — Christian Anyikamadu` : 'Study')
const description = computed(() => entry.value?.idea ?? '')

useSiteSeo({ title, description, path: computed(() => `/studies/${slug.value}`) })

type OtpStatus = 'idle' | 'success' | 'error'
const otpStatus = ref<OtpStatus>('idle')
const onOtpComplete = (code: string) => {
  otpStatus.value = code === '123456' ? 'success' : 'error'
}

const snippets: Record<string, string> = {
  'command-search': `.search {
  width: 192px;
  margin-left: -96px;
  transition: width 0.35s cubic-bezier(0.22, 1, 0.36, 1);
}

.search.is-open {
  width: 384px;
  height: var(--open-h);
}`,
  'play-button': `.player__pill {
  width: 60px;
  transition: width 0.55s cubic-bezier(0.34, 1.4, 0.64, 1);
}

.player__pill.is-open {
  width: 330px;
}`,
  'card-expand': `<motion.article layout layout-id="card-gosource" />`,
  'hover-expand': `.strip { width: 64px; transition: width 0.45s ease; }
.strip.is-on { width: 320px; }`,
  'creative-carousel': `<motion.div
  :animate="pose(index)"
  :transition="{ type: 'spring', bounce: 0.18, duration: 0.6 }"
/>`,
  'otp-input': `.otp__caret {
  transform: translate(calc(var(--caret-x) - 1px), -50%);
  transition: transform 0.38s cubic-bezier(0.22, 1, 0.36, 1);
}`,
  'scroll-stack': `const scale = Math.max(0, 1 - (scrollY - pinnedAt) / 10000)
const rotate = (1 - scale) * 100`,
  'bouncy-accordion': `<motion.li
  :animate="{ height: open ? measured : 45 }"
  :transition="{ type: 'spring', bounce: 0.35, duration: 0.7 }"
/>`
}
</script>

<style scoped>
.study {
  padding-top: 28px;
}

.crumbs {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  color: var(--muted);
  font-size: 13px;
  font-weight: 500;
  line-height: 20px;
}

.crumbs a {
  color: inherit;
  text-decoration: underline;
  text-underline-offset: 3px;
}

.study__title {
  margin-top: 22px;
  font-size: 22px;
  font-weight: 500;
  line-height: 28px;
}

.study__lead,
.study p {
  margin-top: 12px;
  font-size: 14px;
  font-weight: 400;
  line-height: 24px;
}

.study h2 {
  margin-top: 32px;
  font-size: 14px;
  font-weight: 500;
  line-height: 22px;
}

.stage {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 280px;
  margin-top: 22px;
  padding: 36px 16px;
  border: 1px solid var(--line);
  background: #fafafa;
}

.stage--search {
  align-items: flex-start;
  min-height: 560px;
  padding-top: 48px;
}

.stage--wide {
  overflow-x: auto;
}

.stage--carousel {
  min-height: 520px;
}

[data-theme='dark'] .stage {
  background: #0c0c0c;
}

.otp {
  display: grid;
  justify-items: center;
  gap: 12px;
}

.otp__hint {
  color: var(--muted);
  font-size: 13px;
}

.code {
  margin-top: 12px;
  padding: 16px;
  overflow-x: auto;
  border: 1px solid var(--line);
  background: #111111;
  color: #ededed;
  font-family: ui-monospace, SFMono-Regular, Menlo, monospace;
  font-size: 12px;
  font-weight: 400;
  line-height: 20px;
  white-space: pre;
}

.sources {
  display: flex;
  flex-wrap: wrap;
  gap: 8px 16px;
}

.sources a {
  color: var(--muted);
  text-decoration: underline;
  text-underline-offset: 3px;
}
</style>
