<template>
  <component
    :is="tag"
    ref="root"
    class="btn"
    :class="[`btn--${variant}`, { 'is-block': block }]"
    v-bind="attrs"
    @mouseenter="onEnter"
    @mousemove="onMove"
    @mouseleave="onLeave"
  >
    <span ref="label" class="btn__label">
      <slot />
    </span>
  </component>
</template>

<script setup lang="ts">
const props = withDefaults(defineProps<{
  variant?: 'primary' | 'secondary'
  href?: string
  block?: boolean
  external?: boolean
  download?: string | boolean
}>(), {
  variant: 'primary',
  block: false,
  external: false
})

const tag = computed(() => (props.href ? 'a' : 'button'))
const attrs = computed(() => {
  if (props.href) {
    const href = encodeURI(props.href)
    const next: Record<string, string> = props.external
      ? { href, target: '_blank', rel: 'noopener noreferrer' }
      : { href }
    if (props.download) {
      next.download = typeof props.download === 'string' ? props.download : ''
    }
    return next
  }
  return { type: 'button' }
})

const root = ref<HTMLElement | null>(null)
const label = ref<HTMLElement | null>(null)
const { $gsap } = useNuxtApp()

let xTo: ((v: number) => void) | null = null
let yTo: ((v: number) => void) | null = null
let lxTo: ((v: number) => void) | null = null
let lyTo: ((v: number) => void) | null = null

onMounted(() => {
  const gsap = $gsap
  if (!gsap || !root.value || !label.value) return
  xTo = gsap.quickTo(root.value, 'x', { duration: 0.7, ease: 'expo.out' })
  yTo = gsap.quickTo(root.value, 'y', { duration: 0.7, ease: 'expo.out' })
  lxTo = gsap.quickTo(label.value, 'x', { duration: 0.75, ease: 'expo.out' })
  lyTo = gsap.quickTo(label.value, 'y', { duration: 0.75, ease: 'expo.out' })
})

const onEnter = () => {
  const gsap = $gsap
  if (!gsap || !root.value || !hasFinePointer() || prefersReducedMotion()) return
  gsap.to(root.value, { scale: 1.045, duration: 0.7, ease: 'expo.out' })
}

const onMove = (event: MouseEvent) => {
  if (!root.value || !hasFinePointer()) return
  const rect = root.value.getBoundingClientRect()
  const x = event.clientX - (rect.left + rect.width / 2)
  const y = event.clientY - (rect.top + rect.height / 2)
  xTo?.(x * 0.22)
  yTo?.(y * 0.28)
  lxTo?.(x * 0.1)
  lyTo?.(y * 0.12)
}

const onLeave = () => {
  const gsap = $gsap
  xTo?.(0)
  yTo?.(0)
  lxTo?.(0)
  lyTo?.(0)
  if (gsap && root.value) gsap.to(root.value, { scale: 1, duration: 0.8, ease: 'expo.out' })
}
</script>

<style scoped>
.btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  height: 40px;
  padding: 8px 16px;
  border-radius: 48px;
  font-size: 14px;
  line-height: 22px;
  font-weight: 600;
  white-space: nowrap;
  will-change: transform;
}

.btn--primary {
  background: var(--btn-primary-bg);
  color: var(--btn-primary-text);
}

.btn--secondary {
  background: var(--btn-secondary-bg);
  color: var(--btn-secondary-text);
  border: 1px solid var(--btn-secondary-border);
}

.btn__label {
  display: inline-block;
  will-change: transform;
}
</style>
