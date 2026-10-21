<template>
  <ul ref="list" class="bounce">
    <li
      v-for="item in items"
      :key="item.id"
      class="bounce__item"
      :class="{ 'is-open': item.id === openId }"
    >
      <button
        class="bounce__head"
        type="button"
        :aria-expanded="item.id === openId"
        @click="toggle(item.id)"
      >
        <svg class="bounce__icon" viewBox="0 0 24 24" fill="none" aria-hidden="true">
          <template v-if="item.icon === 'book'">
            <path d="M12 7v14" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round" />
            <path d="M3 18a1 1 0 0 1-1-1V4a1 1 0 0 1 1-1h5a4 4 0 0 1 4 4 4 4 0 0 1 4-4h5a1 1 0 0 1 1 1v13a1 1 0 0 1-1 1h-6a3 3 0 0 0-3 3 3 3 0 0 0-3-3z" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round" />
          </template>
          <template v-else-if="item.icon === 'award'">
            <circle cx="12" cy="8" r="6" stroke="currentColor" stroke-width="1.75" />
            <path d="M15.477 12.89 17 22l-5-3-5 3 1.523-9.11" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round" />
          </template>
          <template v-else-if="item.icon === 'calendar'">
            <path d="M8 2v4M16 2v4" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" />
            <rect x="3" y="4" width="18" height="18" rx="2" stroke="currentColor" stroke-width="1.75" />
            <path d="M3 10h18" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" />
          </template>
          <template v-else-if="item.icon === 'cart'">
            <circle cx="8" cy="21" r="1" fill="currentColor" />
            <circle cx="19" cy="21" r="1" fill="currentColor" />
            <path d="M2.05 2.05h2l2.66 12.42a2 2 0 0 0 2 1.58h9.78a2 2 0 0 0 1.95-1.57l1.65-7.43H5.12" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round" />
          </template>
          <template v-else-if="item.icon === 'alert'">
            <path d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round" />
            <path d="M12 9v4" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" />
            <path d="M12 17h.01" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" />
          </template>
          <template v-else>
            <path d="M19 7V4a1 1 0 0 0-1-1H5a2 2 0 0 0 0 4h15a1 1 0 0 1 1 1v4h-3a2 2 0 0 0 0 4h3a1 1 0 0 0 1-1v-2a1 1 0 0 0-1-1" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round" />
            <path d="M3 5v14a2 2 0 0 0 2 2h15v-7" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round" />
          </template>
        </svg>
        <span class="bounce__label">{{ item.label }}</span>
        <svg class="bounce__chevron" viewBox="0 0 24 24" fill="none" aria-hidden="true">
          <path d="m6 9 6 6 6-6" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />
        </svg>
      </button>
      <p class="bounce__copy">{{ item.copy }}</p>
    </li>
  </ul>
</template>

<script setup lang="ts">
type Icon = 'book' | 'award' | 'calendar' | 'cart' | 'alert' | 'wallet'

type Row = {
  id: string
  label: string
  copy: string
  icon: Icon
}

const items: Row[] = [
  { id: 'type', label: 'Type Shit', copy: 'Fast, accurate typing with real-time validation and helpful hints.', icon: 'book' },
  { id: 'star', label: 'Star Great', copy: 'Mark favorites and rate items with smooth micro-interactions.', icon: 'award' },
  { id: 'schedule', label: 'Schedule', copy: 'Plan tasks with timelines, reminders, and conflict detection.', icon: 'calendar' },
  { id: 'buy', label: 'Buy Stuff', copy: 'Streamlined checkout with secure payments and transparent pricing.', icon: 'cart' },
  { id: 'alert', label: 'Triangle Warning', copy: 'Surface critical alerts with accessible, non-intrusive messaging.', icon: 'alert' },
  { id: 'account', label: 'Account bal', copy: 'Track balances, recent activity, and spending insights at a glance.', icon: 'wallet' }
]

const CLOSED_H = 45

const list = ref<HTMLElement | null>(null)
const openId = ref('')
const { $gsap } = useNuxtApp()

const rows = () => [...(list.value?.children ?? [])] as HTMLElement[]

const radiusFor = (index: number, open: boolean) => {
  if (open) return '20px'
  const prevClosed = index > 0 && openId.value !== items[index - 1].id
  const nextClosed = index < items.length - 1 && openId.value !== items[index + 1].id
  if (prevClosed && nextClosed) return '0px'
  if (!prevClosed && nextClosed) return '20px 20px 0px 0px'
  if (prevClosed && !nextClosed) return '0px 0px 20px 20px'
  return '20px'
}

const layout = () => {
  const gsap = $gsap
  if (!gsap) return
  const reduced = prefersReducedMotion()
  rows().forEach((el, index) => {
    const open = items[index].id === openId.value
    const copy = el.querySelector('.bounce__copy') as HTMLElement | null
    gsap.to(el, {
      height: open ? CLOSED_H + (copy?.offsetHeight ?? 0) : CLOSED_H,
      marginTop: open ? 10 : 0,
      marginBottom: open ? 10 : 0,
      borderRadius: radiusFor(index, open),
      duration: reduced ? 0 : 0.7,
      ease: reduced ? 'none' : 'elastic.out(1, 0.7)',
      overwrite: 'auto'
    })
  })
}

const toggle = (id: string) => {
  openId.value = openId.value === id ? '' : id
  layout()
}

onMounted(() => {
  const gsap = $gsap
  rows().forEach((el, index) => {
    gsap?.set(el, {
      height: CLOSED_H,
      marginTop: 0,
      marginBottom: 0,
      borderRadius: radiusFor(index, false)
    })
  })
})
</script>

<style scoped>
.bounce {
  width: 300px;
  margin: 0;
  padding: 0;
  list-style: none;
}

.bounce__item {
  position: relative;
  height: 45px;
  overflow: hidden;
  background: #080808;
  color: #ededed;
}

.bounce__item:first-child {
  border-radius: 20px 20px 0 0;
}

.bounce__item:last-child {
  border-radius: 0 0 20px 20px;
}

.bounce__item:hover {
  background: #222;
}

.bounce__item:hover .bounce__label {
  opacity: 1;
}

.bounce__item:hover .bounce__icon {
  color: #ededed;
}

.bounce__head {
  display: flex;
  align-items: center;
  gap: 8px;
  width: 100%;
  height: 45px;
  padding: 0 40px 0 20px;
  color: inherit;
  font: inherit;
  text-align: start;
  cursor: pointer;
}

.bounce__icon {
  width: 20px;
  height: 20px;
  color: rgba(237, 237, 237, 0.8);
  flex-shrink: 0;
}

.bounce__label {
  font-family: Inter, ui-sans-serif, system-ui, sans-serif;
  font-size: 14px;
  font-weight: 400;
  line-height: 20px;
  letter-spacing: -0.025em;
  opacity: 0.75;
}

.bounce__chevron {
  position: absolute;
  top: 14px;
  right: 16px;
  width: 16px;
  height: 16px;
  color: #ededed;
  transition: transform 0.45s cubic-bezier(0.34, 1.35, 0.64, 1);
}

.bounce__item.is-open .bounce__chevron {
  transform: rotate(180deg);
}

.bounce__copy {
  margin: 0;
  padding: 0 20px 8px;
  color: #ededed;
  font-family: Inter, ui-sans-serif, system-ui, sans-serif;
  font-size: 14px;
  font-weight: 400;
  line-height: 20px;
  opacity: 0;
  filter: blur(6px);
  transition: opacity 0.35s ease, filter 0.35s ease;
}

.bounce__item.is-open .bounce__copy {
  opacity: 0.6;
  filter: blur(0);
}
</style>
