<template>
  <div class="player">
    <motion.button
      class="player__pill"
      type="button"
      :animate="{ width: open ? 330 : 60 }"
      :initial="{ width: 60 }"
      :transition="{ type: 'spring', bounce: 0.18, duration: 0.55 }"
      :aria-expanded="open"
      aria-label="Toggle play button"
      @click="toggle"
    >
      <div class="player__track">
        <Transition name="player-dots">
          <div v-if="open" class="player__dots">
            <span class="player__bar" />
            <span class="player__dot" />
            <span class="player__dot" />
            <span class="player__dot" />
            <span class="player__dot" />
          </div>
        </Transition>
      </div>
      <Transition name="player-icon">
        <div v-if="open" class="player__control">
          <svg
            class="player__play"
            viewBox="-1 0 12 14"
            fill="none"
            xmlns="http://www.w3.org/2000/svg"
            aria-hidden="true"
          >
            <path d="M0.9375 13.2422C1.25 13.2422 1.51562 13.1172 1.82812 12.9375L10.9375 7.67188C11.5859 7.28906 11.8125 7.03906 11.8125 6.625C11.8125 6.21094 11.5859 5.96094 10.9375 5.58594L1.82812 0.3125C1.51562 0.132812 1.25 0.015625 0.9375 0.015625C0.359375 0.015625 0 0.453125 0 1.13281V12.1172C0 12.7969 0.359375 13.2422 0.9375 13.2422Z" />
          </svg>
        </div>
      </Transition>
    </motion.button>

    <button class="player__toggle" type="button" @click="toggle">
      Toggle
    </button>
  </div>
</template>

<script setup lang="ts">
import { motion } from 'motion-v'

const open = ref(false)

const toggle = () => {
  open.value = !open.value
}
</script>

<style scoped>
.player {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 40px;
}

.player__pill {
  display: flex;
  align-items: center;
  justify-content: space-between;
  max-width: calc(100vw - 80px);
  height: 60px;
  overflow: hidden;
  border-radius: 999px;
  background: transparent;
}

.player__track,
.player__control {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 100%;
  border-radius: 999px;
  background: color-mix(in srgb, var(--ink) 16%, transparent);
  flex-shrink: 0;
}

.player__track {
  width: 260px;
}

.player__control {
  width: 60px;
}

.player__dots {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
}

.player__bar {
  width: 60px;
  height: 10px;
  border-radius: 999px;
  background: color-mix(in srgb, var(--ink) 22%, transparent);
}

.player__dot {
  width: 10px;
  height: 10px;
  border-radius: 999px;
  background: color-mix(in srgb, var(--ink) 22%, transparent);
}

.player__play {
  width: 20px;
  height: 20px;
  fill: color-mix(in srgb, var(--ink) 72%, transparent);
}

.player__toggle {
  padding: 4px 28px;
  border-radius: 999px;
  background: color-mix(in srgb, var(--ink) 10%, transparent);
  color: var(--ink);
  font-size: 14px;
  line-height: 22px;
  font-weight: 500;
}

.player__toggle:active {
  transform: scale(0.95);
}

.player-dots-enter-active {
  transition: opacity 0.35s ease 0.2s;
}

.player-dots-enter-from,
.player-dots-leave-to {
  opacity: 0;
}

.player-dots-leave-active {
  transition: opacity 0.12s ease;
}

.player-icon-enter-active {
  transition:
    opacity 0.4s ease 0.12s,
    transform 0.45s cubic-bezier(0.22, 1, 0.36, 1) 0.08s,
    filter 0.4s ease 0.12s;
}

.player-icon-enter-from,
.player-icon-leave-to {
  opacity: 0;
  transform: scale(0.6);
  filter: blur(6px);
}

.player-icon-leave-active {
  transition: opacity 0.12s ease, transform 0.12s ease, filter 0.12s ease;
}

@media (prefers-reduced-motion: reduce) {
  .player-icon-enter-active,
  .player-icon-leave-active,
  .player-dots-enter-active,
  .player-dots-leave-active {
    transition: none;
  }
}
</style>
