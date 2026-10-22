<template>
  <nav class="rail" aria-label="Page sections">
    <ul class="rail__list">
      <li v-for="section in sections" :key="section.id">
        <button
          type="button"
          class="rail__btn"
          :class="{ 'is-on': section.id === shown }"
          :aria-label="section.label"
          :aria-current="section.id === active ? 'true' : undefined"
          @mouseenter="hovered = section.id"
          @mouseleave="hovered = null"
          @focus="hovered = section.id"
          @blur="hovered = null"
          @click="go(section.id)"
        >
          <span v-if="section.id === shown" class="rail__tip">
            <span class="rail__pill">{{ section.label }}</span>
            <svg class="rail__caret" viewBox="0 0 6 5" aria-hidden="true">
              <path d="M1.87.5c.38-.67 1.35-.67 1.73 0L5.33 3.5c.39.67-.09 1.5-.87 1.5H1c-.77 0-1.25-.83-.87-1.5L1.87.5Z" />
            </svg>
          </span>
          <span class="rail__mark" />
        </button>
      </li>
    </ul>
  </nav>
</template>

<script setup lang="ts">
const sections = [
  { id: 'about', label: 'About' },
  { id: 'work', label: 'Work' },
  { id: 'experience', label: 'Experience' }
]

const active = ref(sections[0].id)
const hovered = ref<string | null>(null)
const shown = computed(() => hovered.value || active.value)

const readActive = () => {
  const line = window.innerHeight * 0.38
  let current = sections[0].id
  for (const section of sections) {
    const node = document.getElementById(section.id)
    if (node && node.getBoundingClientRect().top <= line) current = section.id
  }
  active.value = current
}

const go = (id: string) => {
  const node = document.getElementById(id)
  if (!node) return
  const { $lenis } = useNuxtApp()
  if ($lenis) $lenis.scrollTo(node, { offset: -20, duration: 0.7 })
  else node.scrollIntoView({ behavior: 'smooth', block: 'start' })
}

let onScroll: (() => void) | null = null
let observer: IntersectionObserver | null = null

onMounted(() => {
  readActive()
  const { $lenis } = useNuxtApp()
  onScroll = () => readActive()
  if ($lenis && onScroll) $lenis.on('scroll', onScroll)
  window.addEventListener('scroll', readActive, { passive: true })
  document.addEventListener('scroll', readActive, { passive: true })

  observer = new IntersectionObserver(readActive, {
    rootMargin: '-38% 0px -55% 0px',
    threshold: [0, 0.1, 0.5, 1]
  })
  for (const section of sections) {
    const node = document.getElementById(section.id)
    if (node) observer.observe(node)
  }
})

onBeforeUnmount(() => {
  const { $lenis } = useNuxtApp()
  if ($lenis && onScroll) $lenis.off('scroll', onScroll)
  window.removeEventListener('scroll', readActive)
  document.removeEventListener('scroll', readActive)
  observer?.disconnect()
})
</script>

<style scoped>
.rail {
  display: none;
  position: fixed;
  top: 50%;
  right: 36px;
  z-index: 20;
  transform: translateY(-50%);
}

.rail__list {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  margin: 0;
  padding: 0;
  list-style: none;
}

.rail__btn {
  position: relative;
  display: flex;
  align-items: center;
  justify-content: flex-end;
  width: 22px;
  height: 14px;
  padding: 0;
  border: 0;
  background: transparent;
  cursor: pointer;
}

.rail__mark {
  display: block;
  width: 22px;
  height: 4px;
  border-radius: 999px;
  background: #f0f0f0;
}

.rail__btn.is-on .rail__mark {
  background: #707070;
}

.rail__tip {
  position: absolute;
  right: 28px;
  top: 50%;
  display: flex;
  align-items: center;
  transform: translateY(-50%);
  pointer-events: none;
}

.rail__pill {
  padding: 0 8px;
  border-radius: 34px;
  background: #171717;
  color: #c4c4c4;
  font-family: Inter, ui-sans-serif, system-ui, sans-serif;
  font-size: 13px;
  font-weight: 500;
  line-height: 22px;
  white-space: nowrap;
}

.rail__caret {
  width: 6px;
  height: 5px;
  margin-left: -1px;
  transform: rotate(90deg);
  fill: #171717;
}

[data-theme='dark'] .rail__mark {
  background: #2a2a2a;
}

[data-theme='dark'] .rail__btn.is-on .rail__mark {
  background: #ededed;
}

[data-theme='dark'] .rail__pill {
  background: #ffffff;
  color: #333333;
}

[data-theme='dark'] .rail__caret {
  fill: #ffffff;
}

@media (min-width: 1100px) {
  .rail {
    display: block;
  }
}
</style>
