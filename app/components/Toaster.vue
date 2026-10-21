<template>
  <div class="toaster" aria-live="polite" aria-relevant="additions">
    <article
      v-for="item in toasts"
      :key="item.id"
      class="toast"
      :data-starting-style="item.starting ? '' : undefined"
      :data-ending-style="item.ending ? '' : undefined"
      :data-swipe-direction="item.swipe"
      :style="dragStyle(item.id)"
      role="status"
      @pointerdown="onPointerDown(item.id, $event)"
      @pointermove="onPointerMove(item.id, $event)"
      @pointerup="onPointerUp(item.id)"
      @pointercancel="onPointerUp(item.id)"
    >
      <svg class="toast__icon" viewBox="0 0 24 24" fill="none" aria-hidden="true">
        <circle cx="12" cy="12" r="9" stroke="currentColor" stroke-width="1.8" />
        <path d="m8.5 12.2 2.3 2.3 4.7-5" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" />
      </svg>
      <div class="toast__copy">
        <p class="toast__title">{{ item.title }}</p>
        <p v-if="item.description" class="toast__description">{{ item.description }}</p>
      </div>
      <button class="toast__close" type="button" aria-label="Close" @pointerdown.stop @click.stop="toast.close(item.id)">
        <svg viewBox="0 0 16 16" fill="none" aria-hidden="true">
          <path d="M4 4l8 8M12 4l-8 8" stroke="currentColor" stroke-width="1.4" stroke-linecap="round" />
        </svg>
      </button>
    </article>
  </div>
</template>

<script setup lang="ts">
import { toast, useToasts, type ToastSwipe } from '~/lib/toast'

const toasts = useToasts()

type Drag = {
  id: number
  x: number
  y: number
  dx: number
  dy: number
  pointer: number
}

const drag = ref<Drag | null>(null)

const dragStyle = (id: number) => {
  if (!drag.value || drag.value.id !== id) return undefined
  const x = Math.max(0, drag.value.dx)
  const y = Math.max(0, drag.value.dy)
  return { transform: `translate(${x}px, ${y}px)` }
}

const onPointerDown = (id: number, event: PointerEvent) => {
  if (event.button !== 0) return
  const item = toasts.value.find(entry => entry.id === id)
  if (!item || item.ending) return
  drag.value = { id, x: event.clientX, y: event.clientY, dx: 0, dy: 0, pointer: event.pointerId }
  ;(event.currentTarget as HTMLElement).setPointerCapture(event.pointerId)
}

const onPointerMove = (id: number, event: PointerEvent) => {
  if (!drag.value || drag.value.id !== id || drag.value.pointer !== event.pointerId) return
  drag.value = {
    ...drag.value,
    dx: event.clientX - drag.value.x,
    dy: event.clientY - drag.value.y
  }
}

const onPointerUp = (id: number) => {
  if (!drag.value || drag.value.id !== id) return
  const { dx, dy } = drag.value
  drag.value = null
  let swipe: ToastSwipe | undefined
  if (dx > 72) swipe = 'right'
  else if (dy > 56) swipe = 'down'
  if (swipe) toast.close(id, swipe)
}
</script>

<style scoped>
.toaster {
  position: fixed;
  bottom: 24px;
  left: 50%;
  z-index: 100;
  display: flex;
  flex-direction: column;
  gap: 12px;
  width: min(calc(100% - 2rem), 380px);
  transform: translateX(-50%);
  pointer-events: none;
}

.toast {
  display: flex;
  align-items: center;
  gap: 12px;
  width: 100%;
  padding: 14px 16px;
  border: 1px solid #000;
  border-radius: 10px;
  background: #000;
  color: #fff;
  box-shadow: 0 12px 32px rgba(0, 0, 0, 0.28);
  pointer-events: auto;
  touch-action: none;
  user-select: none;
  transition: transform 500ms cubic-bezier(0.22, 1, 0.36, 1), opacity 500ms;
}

.toast[data-starting-style],
.toast[data-ending-style] {
  transform: translateY(150%);
}

.toast[data-ending-style][data-swipe-direction='right'] {
  transform: translateX(150%);
}

.toast[data-ending-style][data-swipe-direction='down'] {
  transform: translateY(150%);
}

.toast__icon {
  width: 20px;
  height: 20px;
  flex-shrink: 0;
}

.toast__copy {
  display: flex;
  flex: 1;
  flex-direction: column;
  gap: 2px;
  min-width: 0;
}

.toast__title {
  font-size: 14px;
  line-height: 20px;
  font-weight: 500;
}

.toast__description {
  font-size: 13px;
  line-height: 20px;
  color: rgb(255 255 255 / 0.7);
}

.toast__close {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 24px;
  height: 24px;
  flex-shrink: 0;
  color: rgb(255 255 255 / 0.7);
}

.toast__close svg {
  width: 16px;
  height: 16px;
}

.toast__close:hover {
  color: #fff;
}

[data-theme='dark'] .toast {
  border-color: #fff;
  background: #fff;
  color: #111;
  box-shadow: 0 12px 32px rgba(0, 0, 0, 0.45);
}

[data-theme='dark'] .toast__description,
[data-theme='dark'] .toast__close {
  color: rgb(17 17 17 / 0.7);
}

[data-theme='dark'] .toast__close:hover {
  color: #111;
}
</style>
