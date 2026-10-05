<template>
  <div class="cmd-root">
    <div
      ref="box"
      class="cmd"
      :class="{ 'is-open': open }"
      @click="openSearch"
    >
      <label ref="bar" class="cmd__bar">
        <svg class="cmd__loupe" viewBox="0 0 16 16" fill="none" aria-hidden="true">
          <circle cx="7.2" cy="7.2" r="4.4" stroke="currentColor" stroke-width="1.2" />
          <path d="M10.4 10.4 13.6 13.6" stroke="currentColor" stroke-width="1.2" stroke-linecap="round" />
        </svg>
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
        <span ref="keyChip" class="cmd__key">
          <span ref="keyF" class="cmd__key-txt">F</span>
          <span ref="keyEsc" class="cmd__key-txt">Esc</span>
        </span>
      </label>

      <div ref="panel" class="cmd__body">
        <template v-for="(group, index) in visibleGroups" :key="group.label">
          <div v-if="index > 0" class="cmd__line" />
          <p class="cmd__group">{{ group.label }}</p>
          <button
            v-for="item in group.items"
            :key="item.id"
            class="cmd__row"
            :class="{ 'is-on': item.id === activeId }"
            type="button"
            @mouseenter="activeId = item.id"
            @click.stop="choose(item)"
          >
            <svg v-if="item.icon === 'arrow'" class="cmd__glyph" viewBox="0 0 16 16" fill="none" aria-hidden="true">
              <path d="M2.8 8h9.6M8.6 4.2 13 8l-4.4 3.8" stroke="currentColor" stroke-width="1.2" stroke-linecap="round" stroke-linejoin="round" />
            </svg>
            <svg v-else class="cmd__glyph" viewBox="0 0 16 16" fill="none" aria-hidden="true">
              <circle cx="8" cy="8" r="2" stroke="currentColor" stroke-width="1.2" />
              <path d="M8 2.6v1.3M8 12.1v1.3M2.6 8h1.3M12.1 8h1.3M4.1 4.1l.95.95M11 11l.95.95M4.1 11.9l.95-.95M11 5.05l.95-.95" stroke="currentColor" stroke-width="1.2" stroke-linecap="round" />
            </svg>
            <span class="cmd__name">{{ item.label }}</span>
            <span v-if="item.shortcut" class="cmd__hot">{{ item.shortcut }}</span>
          </button>
        </template>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
type Command = {
  id: string
  label: string
  group: 'Suggestions' | 'Settings'
  icon: 'arrow' | 'gear'
  shortcut?: string
}

const commands: Command[] = [
  { id: 'calendar', label: 'Calendar', group: 'Suggestions', icon: 'arrow' },
  { id: 'emoji', label: 'Search Emoji', group: 'Suggestions', icon: 'arrow' },
  { id: 'calculator', label: 'Calculator', group: 'Suggestions', icon: 'arrow' },
  { id: 'documents', label: 'Documents', group: 'Suggestions', icon: 'arrow' },
  { id: 'images', label: 'Images', group: 'Suggestions', icon: 'arrow' },
  { id: 'music', label: 'Music', group: 'Suggestions', icon: 'arrow' },
  { id: 'profile', label: 'Profile', group: 'Settings', icon: 'gear', shortcut: '⌘P' }
]

const CLOSED_W = 192
const CLOSED_H = 32
const OPEN_W = 386
const OPEN_BAR = 48

const box = ref<HTMLElement | null>(null)
const bar = ref<HTMLElement | null>(null)
const panel = ref<HTMLElement | null>(null)
const keyChip = ref<HTMLElement | null>(null)
const keyF = ref<HTMLElement | null>(null)
const keyEsc = ref<HTMLElement | null>(null)
const input = ref<HTMLInputElement | null>(null)
const open = ref(false)
const query = ref('')
const activeId = ref(commands[0].id)
const { $gsap } = useNuxtApp()
let tween: { kill: () => void } | null = null

const filtered = computed(() => {
  const q = query.value.trim().toLowerCase()
  if (!q) return commands
  return commands.filter(item => item.label.toLowerCase().includes(q))
})

const visibleGroups = computed(() => ([
  { label: 'Suggestions' as const, items: filtered.value.filter(item => item.group === 'Suggestions') },
  { label: 'Settings' as const, items: filtered.value.filter(item => item.group === 'Settings') }
]).filter(group => group.items.length))

const ids = computed(() => filtered.value.map(item => item.id))

watch(filtered, (items) => {
  if (!items.some(item => item.id === activeId.value)) activeId.value = items[0]?.id ?? ''
})

const openHeight = () => OPEN_BAR + (panel.value?.scrollHeight ?? 0)

const morph = (next: boolean) => {
  const gsap = $gsap
  if (!gsap || !box.value) return
  tween?.kill()

  if (!next) gsap.set(box.value, { height: box.value.offsetHeight })

  const reduced = prefersReducedMotion()
  const duration = reduced ? 0 : next ? 0.42 : 0.32
  const ease = reduced ? 'none' : next ? 'back.out(0.55)' : 'power3.inOut'
  const tl = gsap.timeline({
    overwrite: 'auto',
    onComplete: () => {
      if (next && open.value && box.value) gsap.set(box.value, { height: 'auto' })
    }
  })
  tween = tl

  tl.to(box.value, {
    width: next ? OPEN_W : CLOSED_W,
    height: next ? openHeight() : CLOSED_H,
    borderRadius: next ? 16 : 6,
    duration,
    ease
  }, 0)

  if (bar.value) {
    tl.to(bar.value, {
      height: next ? OPEN_BAR : CLOSED_H,
      paddingLeft: next ? 16 : 12,
      paddingRight: next ? 16 : 8,
      duration,
      ease
    }, 0)
  }

  if (keyChip.value && keyF.value && keyEsc.value) {
    if (next) {
      tl.set(keyF.value, { autoAlpha: 0 }, 0)
      tl.set(keyEsc.value, { autoAlpha: 1 }, 0)
      tl.to(keyChip.value, { width: 28, duration: reduced ? 0 : 0.18, ease: 'power2.out' }, 0)
    } else {
      tl.to(keyChip.value, { width: 18, duration: reduced ? 0 : 0.14, ease: 'power2.out' }, duration * 0.7)
      tl.set(keyEsc.value, { autoAlpha: 0 }, duration * 0.75)
      tl.set(keyF.value, { autoAlpha: 1 }, duration * 0.75)
    }
  }
}

const openSearch = () => {
  if (open.value) return
  open.value = true
  nextTick(() => {
    morph(true)
    input.value?.focus()
  })
}

const closeSearch = () => {
  if (!open.value) return
  query.value = ''
  activeId.value = commands[0].id
  open.value = false
  morph(false)
  input.value?.blur()
}

const choose = (_item: Command) => closeSearch()

const move = (delta: number) => {
  if (!ids.value.length) return
  const index = Math.max(0, ids.value.indexOf(activeId.value))
  activeId.value = ids.value[(index + delta + ids.value.length) % ids.value.length]
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
  const gsap = $gsap
  gsap?.set(box.value, {
    xPercent: -50,
    width: CLOSED_W,
    height: CLOSED_H,
    borderRadius: 6
  })
  gsap?.set(bar.value, { height: CLOSED_H, paddingLeft: 12, paddingRight: 8 })
  gsap?.set(keyChip.value, { width: 18 })
  gsap?.set(keyEsc.value, { autoAlpha: 0 })
  gsap?.set(keyF.value, { autoAlpha: 1 })
  window.addEventListener('keydown', onKey)
  document.addEventListener('pointerdown', onPointer)
})

onBeforeUnmount(() => {
  tween?.kill()
  window.removeEventListener('keydown', onKey)
  document.removeEventListener('pointerdown', onPointer)
})
</script>

<style scoped>
.cmd-root {
  position: relative;
  width: 386px;
  height: 32px;
}

.cmd {
  position: absolute;
  top: 0;
  left: 50%;
  box-sizing: border-box;
  width: 192px;
  height: 32px;
  overflow: hidden;
  background: #121212;
  border: 1px solid #2a2a2a;
  border-radius: 6px;
  color: #ededed;
  font-family: Inter, ui-sans-serif, system-ui, sans-serif;
  cursor: text;
  will-change: width, height, border-radius;
}

.cmd__bar {
  display: flex;
  align-items: center;
  gap: 8px;
  box-sizing: border-box;
  height: 32px;
  padding: 0 8px 0 12px;
}

.cmd__loupe {
  width: 14px;
  height: 14px;
  color: #9a9a9a;
  flex-shrink: 0;
}

.cmd__input {
  flex: 1;
  min-width: 0;
  height: 100%;
  border: 0;
  border-radius: 0;
  background: transparent;
  color: #ededed;
  font: inherit;
  font-size: 13px;
  line-height: 18px;
  outline: none;
  appearance: none;
  -webkit-appearance: none;
}

.cmd__input::placeholder {
  color: #8a8a8a;
}

.cmd__key {
  position: relative;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  box-sizing: border-box;
  width: 18px;
  height: 18px;
  overflow: hidden;
  border: 1px solid #2a2a2a;
  border-radius: 5px;
  color: #b3b3b3;
  font-size: 10px;
  line-height: 10px;
  flex-shrink: 0;
}

.cmd__key-txt {
  position: absolute;
  white-space: nowrap;
}

.cmd__body {
  padding: 4px 0 10px;
}

.cmd__line {
  height: 1px;
  margin: 4px 0;
  background: #2a2a2a;
}

.cmd__group {
  padding: 8px 16px 6px;
  color: #6d6d6d;
  font-size: 12px;
  line-height: 16px;
}

.cmd__row {
  display: flex;
  align-items: center;
  gap: 10px;
  width: calc(100% - 16px);
  height: 36px;
  margin: 0 8px;
  padding: 0 12px;
  border: 0;
  background: transparent;
  border-radius: 8px;
  color: #ededed;
  font: inherit;
  font-size: 14px;
  line-height: 20px;
  text-align: start;
  cursor: pointer;
}

.cmd__row.is-on {
  background: #282828;
}

.cmd__glyph {
  width: 14px;
  height: 14px;
  color: #c8c8c8;
  flex-shrink: 0;
}

.cmd__name {
  flex: 1;
}

.cmd__hot {
  color: #8a8a8a;
  font-size: 12px;
}
</style>
