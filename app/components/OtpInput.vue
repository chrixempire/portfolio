<template>
  <div
    class="otp"
    :data-status="status"
    :data-size="size"
    :style="scaleVars"
  >
    <div
      ref="row"
      class="otp__row"
      @focusin="onFocusIn"
      @focusout="onFocusOut"
    >
      <div
        v-for="(slot, index) in slots"
        :key="index"
        :ref="el => setCell(index, el)"
        class="otp__cell"
        :data-filled="Boolean(slot)"
      >
        <input
          :ref="el => setInput(index, el)"
          class="otp__slot"
          :class="{
            'is-error': status === 'error',
            'is-idle': status === 'idle'
          }"
          :value="slot"
          :type="mask ? 'password' : 'text'"
          :inputmode="numeric ? 'numeric' : 'text'"
          :autocapitalize="numeric ? 'off' : 'characters'"
          :autocomplete="index === 0 ? 'one-time-code' : 'off'"
          :autofocus="autoFocus && index === 0"
          :disabled="disabled"
          :aria-label="`${numeric ? 'Digit' : 'Character'} ${index + 1} of ${length}`"
          @input="onInput(index, $event)"
          @keydown="onKeyDown(index, $event)"
          @paste="onPaste(index, $event)"
          @pointerdown="onPointerDown(index, $event)"
          @focus="onSlotFocus($event)"
        >

        <svg
          v-if="status === 'success'"
          class="otp__ring"
          aria-hidden="true"
          :viewBox="`0 0 ${scale.px} ${scale.px}`"
        >
          <rect
            class="otp__ring-path"
            :style="{ animationDelay: `${0.15 + index * 0.05}s` }"
            :x="1"
            :y="1"
            :width="scale.px - 2"
            :height="scale.px - 2"
            :rx="scale.radius - 1"
            fill="none"
            stroke="#34C759"
            stroke-width="2"
            pathLength="1"
          />
        </svg>

        <span class="otp__face">
          <Transition name="otp-char" @before-leave="onCharBeforeLeave">
            <span
              v-if="slot"
              :key="slot"
              class="otp__char"
            >
              {{ mask ? '•' : slot }}
            </span>
          </Transition>
        </span>
      </div>

      <span
        v-if="caretVisible"
        ref="caretEl"
        class="otp__caret"
        aria-hidden="true"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
type OtpType = 'numbers' | 'letters' | 'both'
type OtpSize = 'sm' | 'md' | 'lg'
type OtpStatus = 'idle' | 'success' | 'error'

const PATTERNS: Record<OtpType, RegExp> = {
  numbers: /^[0-9]$/,
  letters: /^[a-zA-Z]$/,
  both: /^[a-zA-Z0-9]$/
}

const SIZES: Record<OtpSize, { px: number, radius: number, gap: number, caret: number, text: number }> = {
  sm: { px: 40, radius: 8, gap: 6, caret: 20, text: 16 },
  md: { px: 48, radius: 12, gap: 8, caret: 24, text: 18 },
  lg: { px: 56, radius: 16, gap: 10, caret: 28, text: 20 }
}

const props = withDefaults(defineProps<{
  length?: number
  type?: OtpType
  size?: OtpSize
  status?: OtpStatus
  mask?: boolean
  disabled?: boolean
  autoFocus?: boolean
}>(), {
  length: 6,
  type: 'numbers',
  size: 'md',
  status: 'idle',
  mask: false,
  disabled: false,
  autoFocus: false
})

const emit = defineEmits<{
  change: [value: string]
  complete: [value: string]
}>()


const slots = ref<string[]>(Array.from({ length: props.length }, () => ''))
const cleared = ref(false)
const focused = ref<number | null>(null)
const caretX = ref(0)
const row = ref<HTMLElement | null>(null)
const caretEl = ref<HTMLElement | null>(null)
const cells = ref<(HTMLElement | null)[]>([])
const inputs = ref<(HTMLInputElement | null)[]>([])
const editingAt = ref<number | null>(null)
let caretReady = false

const numeric = computed(() => props.type === 'numbers')
const scale = computed(() => SIZES[props.size])
const caretVisible = computed(() => focused.value !== null && !slots.value[focused.value])
const scaleVars = computed(() => ({
  '--otp-size': `${scale.value.px}px`,
  '--otp-radius': `${scale.value.radius}px`,
  '--otp-gap': `${scale.value.gap}px`,
  '--otp-caret': `${scale.value.caret}px`,
  '--otp-text': `${scale.value.text}px`
}))

const setCell = (index: number, el: Element | ComponentPublicInstance | null) => {
  cells.value[index] = el instanceof HTMLElement ? el : null
}

const setInput = (index: number, el: Element | ComponentPublicInstance | null) => {
  inputs.value[index] = el instanceof HTMLInputElement ? el : null
}

const commit = (next: string[]) => {
  slots.value = next
  const code = next.join('')
  emit('change', code)
  if (next.every(Boolean)) emit('complete', code)
}

const setCharAt = (index: number, char: string) => {
  cleared.value = !char
  commit(slots.value.map((slot, i) => (i === index ? char : slot)))
}

const focusAt = async (index: number) => {
  await nextTick()
  const input = inputs.value[Math.min(Math.max(index, 0), props.length - 1)]
  input?.focus()
  input?.select()
}

const fill = (index: number, chars: string[]) => {
  const room = Math.min(chars.length, props.length - index)
  const next = [...slots.value]
  chars.slice(0, room).forEach((char, i) => {
    next[index + i] = char
  })
  cleared.value = false
  commit(next)
  editingAt.value = null
  focusAt(index + room)
}

const onInput = (index: number, event: Event) => {
  const target = event.target as HTMLInputElement
  const chars = target.value.split('').filter(char => PATTERNS[props.type].test(char))
  if (!chars.length) {
    target.value = slots.value[index]
    return
  }

  const typed =
    chars.length === 1
      ? chars[0]
      : chars.length === 2 && chars[0] === slots.value[index]
        ? chars[1]
        : null

  if (typed === null) {
    fill(index, chars)
    return
  }

  if (slots.value.every(Boolean) && editingAt.value !== index) {
    target.value = slots.value[index]
    return
  }

  setCharAt(index, typed)
  editingAt.value = null
  focusAt(index + 1)
}

const onKeyDown = (index: number, event: KeyboardEvent) => {
  if (event.key === 'ArrowLeft') {
    event.preventDefault()
    editingAt.value = Math.max(index - 1, 0)
    focusAt(index - 1)
    return
  }
  if (event.key === 'ArrowRight') {
    event.preventDefault()
    editingAt.value = Math.min(index + 1, props.length - 1)
    focusAt(index + 1)
    return
  }
  if (event.key !== 'Backspace') return
  event.preventDefault()
  if (slots.value[index]) {
    setCharAt(index, '')
  } else if (index > 0) {
    setCharAt(index - 1, '')
    focusAt(index - 1)
  }
}

const onPaste = (index: number, event: ClipboardEvent) => {
  event.preventDefault()
  const pasted = (event.clipboardData?.getData('text') ?? '')
    .split('')
    .filter(char => PATTERNS[props.type].test(char))
  if (pasted.length) fill(index, pasted)
}

const onPointerDown = (index: number, event: PointerEvent) => {
  const firstEmpty = slots.value.findIndex(slot => !slot)
  const target = firstEmpty === -1 ? index : Math.min(index, firstEmpty)
  editingAt.value = target
  if (target === index) return
  event.preventDefault()
  focusAt(target)
}

const onSlotFocus = (event: FocusEvent) => {
  (event.target as HTMLInputElement).select()
}

const placeCaret = (index: number) => {
  const cell = cells.value[index]
  if (!cell) return
  caretX.value = cell.offsetLeft + cell.offsetWidth / 2
}

const onFocusIn = (event: FocusEvent) => {
  const index = inputs.value.indexOf(event.target as HTMLInputElement)
  if (index < 0) return
  focused.value = index
  placeCaret(index)
}

const onFocusOut = (event: FocusEvent) => {
  if (!row.value?.contains(event.relatedTarget as Node)) {
    focused.value = null
    caretReady = false
  }
}

const onCharBeforeLeave = (el: Element) => {
  el.classList.toggle('is-cleared', cleared.value)
}

watch([caretVisible, caretX], async () => {
  await nextTick()
  row.value?.style.setProperty('--caret-x', `${caretX.value}px`)
})

watch(() => props.status, (status) => {
  const rowEl = row.value
  if (status !== 'error' || !rowEl || prefersReducedMotion()) return
  rowEl.classList.remove('is-shaking')
  void rowEl.offsetWidth
  rowEl.classList.add('is-shaking')
})
</script>

<style scoped>
.otp {
  position: relative;
  display: inline-flex;
}

.otp__row {
  position: relative;
  display: flex;
  align-items: center;
  gap: var(--otp-gap);
}

.otp__cell {
  position: relative;
  width: var(--otp-size);
  height: var(--otp-size);
}

.otp__slot {
  width: var(--otp-size);
  height: var(--otp-size);
  padding: 0;
  border: 0;
  border-radius: var(--otp-radius);
  background: #262626;
  color: transparent;
  caret-color: transparent;
  font-size: var(--otp-text);
  font-weight: 500;
  text-align: center;
  outline: none;
  transition: box-shadow 0.2s;
}

.otp__slot::selection {
  background: transparent;
}

.otp__slot:disabled {
  cursor: not-allowed;
  opacity: 0.5;
}

.otp__slot.is-idle:focus-visible {
  box-shadow: 0 0 0 2px rgb(134 133 147 / 0.5);
}

.otp__slot.is-error {
  box-shadow: 0 0 0 2px rgb(255 59 48 / 0.7);
  transition-delay: 0.15s;
}

.otp__ring {
  pointer-events: none;
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
}

.otp__ring-path {
  stroke-dasharray: 1;
  stroke-dashoffset: 1;
  animation: otp-ring 0.45s ease-out forwards;
}

.otp__face {
  pointer-events: none;
  position: absolute;
  inset: 0;
  display: grid;
  place-items: center;
  overflow: hidden;
}

.otp__char {
  font-size: var(--otp-text);
  font-weight: 600;
  line-height: 1;
  color: #fff;
}

.otp-char-enter-from {
  transform: translateY(110%);
}

.otp-char-enter-active {
  transition: transform 0.45s cubic-bezier(0.34, 1.35, 0.64, 1);
}

.otp-char-leave-active {
  position: absolute;
  transition: transform 0.35s cubic-bezier(0.4, 0, 1, 1);
}

.otp-char-leave-to {
  transform: translateY(-110%);
}

.otp-char-leave-to.is-cleared {
  transform: translateY(110%);
}

.otp__caret {
  pointer-events: none;
  position: absolute;
  top: 50%;
  left: 0;
  width: 2px;
  height: var(--otp-caret);
  border-radius: 999px;
  background: #fff;
  transform: translate(calc(var(--caret-x, 0px) - 1px), -50%);
  transition: transform 0.38s cubic-bezier(0.22, 1, 0.36, 1);
  animation: otp-blink 1.1s linear infinite;
}

.otp__row.is-shaking {
  animation: otp-shake 0.32s ease;
}

@keyframes otp-shake {
  20% { transform: translateX(-5px); }
  40% { transform: translateX(4px); }
  60% { transform: translateX(-2px); }
  100% { transform: translateX(0); }
}

@keyframes otp-ring {
  to {
    stroke-dashoffset: 0;
  }
}

@keyframes otp-blink {
  0%,
  50% {
    opacity: 1;
  }

  50.01%,
  100% {
    opacity: 0;
  }
}

@media (prefers-reduced-motion: reduce) {
  .otp__ring-path,
  .otp__caret {
    animation: none;
  }

  .otp__ring-path {
    stroke-dashoffset: 0;
  }

  .otp-char-enter-from,
  .otp-char-leave-to,
  .otp-char-leave-to.is-cleared {
    transform: none;
  }

  .otp-char-enter-active,
  .otp-char-leave-active {
    transition: none;
  }
}
</style>
