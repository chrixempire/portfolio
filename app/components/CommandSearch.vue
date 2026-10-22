<template>
  <div class="cmd-root">
    <div
      ref="box"
      class="cmd"
      :class="{ 'is-open': open }"
      @click="openSearch"
    >
      <label ref="bar" class="cmd__bar">
        <span ref="iconSlot" class="cmd__slot">
          <svg class="cmd__loupe" viewBox="0 0 24 24" fill="none" aria-hidden="true">
            <circle cx="11" cy="11" r="8" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />
            <path d="m21 21-4.34-4.34" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />
          </svg>
        </span>
        <input
          ref="input"
          v-model="query"
          class="cmd__input"
          type="text"
          placeholder="Find..."
          autocomplete="off"
          spellcheck="false"
          @focus="openSearch"
        >
        <span ref="keySlot" class="cmd__slot cmd__slot--key">
          <span class="cmd__key">{{ open ? 'Esc' : 'F' }}</span>
        </span>
      </label>
      <div class="cmd__rule" />

      <div class="cmd__border" />
      <div ref="panel" class="cmd__body" data-lenis-prevent :inert="!open">
        <template v-for="(group, index) in visibleGroups" :key="group.label">
          <div v-if="index > 0" class="cmd__line" />
          <div class="cmd__group">
            <p class="cmd__label">{{ group.label }}</p>
            <button
              v-for="item in group.items"
              :key="item.id"
              class="cmd__row"
              :class="{ 'is-on': item.id === activeId }"
              type="button"
              @mouseenter="hoverItem(item.id)"
              @click.stop="choose(item)"
            >
              <svg v-if="item.icon === 'arrow'" class="cmd__glyph" viewBox="0 0 24 24" fill="none" aria-hidden="true">
                <path d="M5 12h14" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />
                <path d="m12 5 7 7-7 7" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />
              </svg>
              <svg v-else-if="item.icon === 'cog'" class="cmd__glyph" viewBox="0 0 24 24" fill="none" aria-hidden="true">
                <path d="M12 20a8 8 0 1 0 0-16 8 8 0 0 0 0 16Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />
                <path d="M12 14a2 2 0 1 0 0-4 2 2 0 0 0 0 4Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />
                <path d="M12 2v2" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />
                <path d="M12 22v-2" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />
                <path d="m17 20.66-1-1.73" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />
                <path d="M11 10.27 7 3.34" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />
                <path d="m20.66 17-1.73-1" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />
                <path d="m3.34 7 1.73 1" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />
                <path d="M14 12h8" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />
                <path d="M2 12h2" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />
                <path d="m20.66 7-1.73 1" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />
                <path d="m3.34 17 1.73-1" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />
                <path d="m17 3.34-1 1.73" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />
                <path d="m11 13.73-4 6.93" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />
              </svg>
              <svg v-else-if="item.icon === 'dashed'" class="cmd__glyph" viewBox="0 0 24 24" fill="none" aria-hidden="true">
                <path d="M10.1 2.182a10 10 0 0 1 3.8 0" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />
                <path d="M13.9 21.818a10 10 0 0 1-3.8 0" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />
                <path d="M17.609 3.721a10 10 0 0 1 2.69 2.7" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />
                <path d="M2.182 13.9a10 10 0 0 1 0-3.8" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />
                <path d="M20.279 17.609a10 10 0 0 1-2.7 2.69" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />
                <path d="M21.818 10.1a10 10 0 0 1 0 3.8" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />
                <path d="M3.721 6.391a10 10 0 0 1 2.7-2.69" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />
                <path d="M6.391 20.279a10 10 0 0 1-2.69-2.7" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />
              </svg>
              <svg v-else class="cmd__glyph" viewBox="0 0 24 24" fill="none" aria-hidden="true">
                <path d="M12 7v14" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />
                <path d="M3 18a1 1 0 0 1-1-1V4a1 1 0 0 1 1-1h5a4 4 0 0 1 4 4 4 4 0 0 1 4-4h5a1 1 0 0 1 1 1v13a1 1 0 0 1-1 1h-6a3 3 0 0 0-3 3 3 3 0 0 0-3-3z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />
              </svg>
              <span class="cmd__name">{{ item.label }}</span>
              <span v-if="item.shortcut" class="cmd__hot">{{ item.shortcut }}</span>
            </button>
          </div>
        </template>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { toast } from '~/lib/toast'

type Command = {
  id: string
  label: string
  group: 'Suggestions' | 'Settings' | 'Help' | 'Docs'
  icon: 'arrow' | 'cog' | 'dashed' | 'book'
  shortcut?: string
}

const commands: Command[] = [
  { id: 'calendar', label: 'GoSource', group: 'Suggestions', icon: 'arrow' },
  { id: 'emoji', label: 'Kaorex', group: 'Suggestions', icon: 'arrow' },
  { id: 'calculator', label: 'Daash', group: 'Suggestions', icon: 'arrow' },
  { id: 'documents', label: 'Octupus', group: 'Suggestions', icon: 'arrow' },
  { id: 'images', label: 'Quality', group: 'Suggestions', icon: 'arrow' },
  { id: 'music', label: 'Bayana', group: 'Suggestions', icon: 'arrow' },
  { id: 'profile', label: 'Resume', group: 'Settings', icon: 'cog', shortcut: '⌘P' },
  { id: 'billing', label: 'Schedule', group: 'Settings', icon: 'cog', shortcut: '⌘B' },
  { id: 'settings', label: 'LinkedIn', group: 'Settings', icon: 'cog', shortcut: '⌘S' },
  { id: 'notifications', label: 'GitHub', group: 'Settings', icon: 'cog', shortcut: '⌘N' },
  { id: 'messages', label: 'Email', group: 'Settings', icon: 'cog', shortcut: '⌘M' },
  { id: 'security', label: 'Phone', group: 'Settings', icon: 'cog', shortcut: '⌘T' },
  { id: 'faq', label: 'Questions', group: 'Help', icon: 'dashed' },
  { id: 'support', label: 'Write to me', group: 'Help', icon: 'dashed' },
  { id: 'docs', label: 'Case notes', group: 'Docs', icon: 'book' },
  { id: 'tutorials', label: 'Build notes', group: 'Docs', icon: 'book' }
]

const CLOSED_W = 192
const CLOSED_H = 32
const OPEN_W = 384
const BAR_H = 48
const RULE = 1
const LIST_MAX = 300

const box = ref<HTMLElement | null>(null)
const bar = ref<HTMLElement | null>(null)
const iconSlot = ref<HTMLElement | null>(null)
const keySlot = ref<HTMLElement | null>(null)
const panel = ref<HTMLElement | null>(null)
const input = ref<HTMLInputElement | null>(null)
const open = ref(false)
const query = ref('')
const activeId = ref(commands[0].id)

const filtered = computed(() => {
  const q = query.value.trim().toLowerCase()
  if (!q) return commands
  return commands.filter(item => item.label.toLowerCase().includes(q))
})

const visibleGroups = computed(() => ([
  { label: 'Suggestions' as const, items: filtered.value.filter(item => item.group === 'Suggestions') },
  { label: 'Settings' as const, items: filtered.value.filter(item => item.group === 'Settings') },
  { label: 'Help' as const, items: filtered.value.filter(item => item.group === 'Help') },
  { label: 'Docs' as const, items: filtered.value.filter(item => item.group === 'Docs') }
]).filter(group => group.items.length))

const ids = computed(() => filtered.value.map(item => item.id))

watch(filtered, (items) => {
  if (!items.some(item => item.id === activeId.value)) activeId.value = items[0]?.id ?? ''
  if (!open.value) return
  nextTick(syncHeight)
})

const openHeight = () => BAR_H + RULE + Math.min(panel.value?.scrollHeight ?? 0, LIST_MAX)

const syncHeight = () => {
  if (!box.value || !open.value) return
  box.value.style.setProperty('--open-h', `${openHeight()}px`)
}

const openSearch = () => {
  if (open.value) return
  open.value = true
  nextTick(() => {
    syncHeight()
    input.value?.focus()
  })
}

const closeSearch = () => {
  if (!open.value) return
  query.value = ''
  activeId.value = commands[0].id
  open.value = false
  if (panel.value?.contains(document.activeElement)) {
    (document.activeElement as HTMLElement).blur()
  }
  if (box.value) box.value.scrollTop = 0
  if (panel.value) panel.value.scrollTop = 0
  input.value?.blur()
}

const choose = (item: Command) => {
  closeSearch()
  toast.add({ type: 'success', title: `Selected ${item.label}`, timeout: 3200 })
}

const hoverItem = (id: string) => {
  activeId.value = id
  revealActive()
}

const revealActive = () => {
  nextTick(() => {
    const scroller = panel.value
    const row = scroller?.querySelector('.cmd__row.is-on')
    if (!scroller || !(row instanceof HTMLElement)) return
    const scrollerRect = scroller.getBoundingClientRect()
    const rowRect = row.getBoundingClientRect()
    const gutter = 4
    if (rowRect.top < scrollerRect.top + gutter) scroller.scrollTop -= scrollerRect.top + gutter - rowRect.top
    else if (rowRect.bottom > scrollerRect.bottom - gutter) scroller.scrollTop += rowRect.bottom - (scrollerRect.bottom - gutter)
  })
}

const move = (delta: number) => {
  if (!ids.value.length) return
  const index = Math.max(0, ids.value.indexOf(activeId.value))
  activeId.value = ids.value[(index + delta + ids.value.length) % ids.value.length]
  revealActive()
}

const onWheel = (event: WheelEvent) => {
  const scroller = panel.value
  if (!open.value || !scroller || !scroller.contains(event.target as Node)) return
  if (scroller.scrollHeight <= scroller.clientHeight) return
  event.preventDefault()
  event.stopPropagation()
  scroller.scrollTop += event.deltaY
}

const onKey = (event: KeyboardEvent) => {
  if (event.key === 'Escape' && open.value) {
    event.preventDefault()
    closeSearch()
    return
  }
  if ((event.key === 'f' || event.key === 'F') && !open.value && !event.metaKey && !event.ctrlKey && !event.altKey) {
    event.preventDefault()
    openSearch()
    return
  }
  if (!open.value) return
  if ((event.metaKey || event.ctrlKey) && !event.altKey && !event.shiftKey && event.key.length === 1) {
    const item = filtered.value.find(entry => entry.shortcut === `⌘${event.key.toUpperCase()}`)
    if (item) {
      event.preventDefault()
      choose(item)
      return
    }
  }
  if (event.key === 'ArrowDown') { event.preventDefault(); move(1) }
  if (event.key === 'ArrowUp') { event.preventDefault(); move(-1) }
  if (event.key === 'Enter') {
    const item = filtered.value.find(entry => entry.id === activeId.value)
    if (item) { event.preventDefault(); choose(item) }
  }
}

const onPointer = (event: PointerEvent) => {
  if (!open.value || !box.value) return
  if (!box.value.contains(event.target as Node)) closeSearch()
}

onMounted(() => {
  window.addEventListener('keydown', onKey)
  document.addEventListener('pointerdown', onPointer)
  panel.value?.addEventListener('wheel', onWheel, { passive: false })
})

onBeforeUnmount(() => {
  window.removeEventListener('keydown', onKey)
  document.removeEventListener('pointerdown', onPointer)
  panel.value?.removeEventListener('wheel', onWheel)
})
</script>

<style scoped>
.cmd-root {
  position: relative;
  width: 192px;
  height: 32px;
}

.cmd {
  position: absolute;
  top: 0;
  left: 50%;
  margin-left: -96px;
  box-sizing: border-box;
  width: 192px;
  height: 32px;
  overflow: clip;
  background: #121212;
  border-radius: 6px;
  transition:
    width 0.45s cubic-bezier(0.34, 1.15, 0.64, 1),
    height 0.45s cubic-bezier(0.34, 1.15, 0.64, 1),
    margin-left 0.45s cubic-bezier(0.34, 1.15, 0.64, 1),
    left 0.45s cubic-bezier(0.34, 1.15, 0.64, 1),
    border-radius 0.45s ease;
  color: #ededed;
  font-family: Inter, ui-sans-serif, system-ui, sans-serif;
  font-size: 14px;
  font-weight: 400;
  line-height: 20px;
  cursor: text;
  transform-origin: top left;
  will-change: width, height, border-radius;
}

.cmd.is-open {
  width: 384px;
  height: var(--open-h, 360px);
  border-radius: 12px;
  box-shadow:
    0 4px 6px -1px rgb(0 0 0 / 0.1),
    0 2px 4px -2px rgb(0 0 0 / 0.1);
}

.cmd__border {
  position: absolute;
  inset: 0;
  z-index: 2;
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: inherit;
  pointer-events: none;
}

.cmd__bar {
  display: flex;
  align-items: center;
  box-sizing: border-box;
  height: 32px;
  transition: height 0.45s cubic-bezier(0.34, 1.15, 0.64, 1);
}

.cmd.is-open .cmd__bar {
  height: 48px;
}

.cmd__slot {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 32px;
  height: 32px;
  flex-shrink: 0;
  transition:
    width 0.45s cubic-bezier(0.34, 1.15, 0.64, 1),
    height 0.45s cubic-bezier(0.34, 1.15, 0.64, 1);
}

.cmd.is-open .cmd__slot {
  width: 48px;
  height: 48px;
}

.cmd.is-open .cmd__slot--key {
  padding-right: 4px;
}

.cmd__loupe {
  width: 16px;
  height: 16px;
  color: #ededed;
}

.cmd__input {
  flex: 1;
  min-width: 0;
  height: 20px;
  padding: 0;
  border: 0;
  border-radius: 0;
  background: transparent;
  color: #ededed;
  font: inherit;
  font-size: 14px;
  font-weight: 400;
  line-height: 20px;
  outline: none;
  appearance: none;
  -webkit-appearance: none;
}

.cmd__input::placeholder {
  color: rgba(237, 237, 237, 0.4);
  font-weight: 400;
}

.cmd.is-open .cmd__input::placeholder {
  color: #4f4f4e;
}

.cmd__key {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  box-sizing: border-box;
  width: 22px;
  height: 22px;
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 4px;
  color: #ededed;
  font-size: 12px;
  font-weight: 400;
  line-height: 16px;
  letter-spacing: 0;
}

.cmd.is-open .cmd__key {
  width: auto;
  padding: 2px 4px;
  letter-spacing: -0.6px;
}

.cmd__rule {
  height: 0;
  background: rgba(255, 255, 255, 0.1);
}

.cmd.is-open .cmd__rule {
  height: 1px;
}

.cmd__body {
  max-height: 300px;
  overflow-x: hidden;
  overflow-y: auto;
  overscroll-behavior: contain;
  scroll-padding: 4px;
  scrollbar-width: thin;
  scrollbar-color: rgba(255, 255, 255, 0.22) transparent;
}

.cmd__body::-webkit-scrollbar {
  width: 8px;
}

.cmd__body::-webkit-scrollbar-thumb {
  background: rgba(255, 255, 255, 0.22);
  border-radius: 8px;
}

.cmd__line {
  height: 1px;
  background: rgba(255, 255, 255, 0.1);
}

.cmd__group {
  padding: 4px;
}

.cmd__label {
  margin: 0;
  padding: 6px 8px;
  color: #4f4f4e;
  font-size: 12px;
  font-weight: 500;
  line-height: 16px;
}

.cmd__row {
  display: flex;
  align-items: center;
  gap: 8px;
  box-sizing: border-box;
  width: 100%;
  height: 32px;
  margin: 0;
  padding: 6px 8px;
  border: 0;
  border-radius: 4px;
  background: transparent;
  color: #ededed;
  font: inherit;
  font-size: 14px;
  font-weight: 400;
  line-height: 20px;
  text-align: start;
  cursor: pointer;
}

.cmd__row.is-on {
  background: rgba(255, 255, 255, 0.1);
}

.cmd__glyph {
  width: 16px;
  height: 16px;
  color: #4f4f4e;
  flex-shrink: 0;
}

.cmd__name {
  flex: 1;
  font-weight: 400;
}

.cmd__hot {
  margin-left: auto;
  color: #4f4f4e;
  font-size: 12px;
  font-weight: 400;
  line-height: 16px;
  letter-spacing: 0.1em;
}

@media (max-width: 680px) {
  .cmd-root {
    width: min(384px, 100%);
    min-width: 0;
  }

  .cmd.is-open {
    left: 0;
    width: 100%;
    margin-left: 0;
  }
}
</style>
