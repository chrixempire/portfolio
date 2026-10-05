<template>
  <div class="expand-row" aria-label="Hover expand gallery">
    <button
      v-for="(image, index) in hoverImages"
      :key="image.src"
      class="expand-card"
      :class="{ 'is-on': index === active }"
      type="button"
      :aria-pressed="index === active"
      :aria-label="image.alt"
      @mouseenter="activate(index)"
      @focus="activate(index)"
      @click="activate(index)"
    >
      <img
        class="expand-card__media"
        :src="image.src"
        :alt="image.alt"
      >
      <Transition name="expand-fade">
        <span v-if="index === active" class="expand-card__veil" />
      </Transition>
      <Transition name="expand-fade">
        <span v-if="index === active" class="expand-card__code">{{ image.code }}</span>
      </Transition>
    </button>
  </div>
</template>

<script setup lang="ts">
import { hoverImages } from '~/data/site'

const active = ref(1)

const activate = (index: number) => {
  active.value = index
}
</script>

<style scoped>
.expand-row {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  width: 100%;
}

.expand-card {
  position: relative;
  flex: 0 0 64px;
  width: 64px;
  height: 320px;
  overflow: hidden;
  border-radius: 24px;
  background: #1a1a1a;
  transition: flex-basis 0.3s ease-in-out, width 0.3s ease-in-out;
}

.expand-card.is-on {
  flex-basis: 320px;
  width: 320px;
}

.expand-card__media {
  display: block;
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.expand-card__veil {
  position: absolute;
  inset: 0;
  background: linear-gradient(to top, rgb(0 0 0 / 0.4), transparent);
  pointer-events: none;
}

.expand-card__code {
  position: absolute;
  right: 16px;
  bottom: 16px;
  color: #fff;
  font-size: 14px;
  line-height: 20px;
  pointer-events: none;
}

.expand-fade-enter-active,
.expand-fade-leave-active {
  transition: opacity 0.3s ease;
}

.expand-fade-enter-from,
.expand-fade-leave-to {
  opacity: 0;
}

@media (prefers-reduced-motion: reduce) {
  .expand-card,
  .expand-fade-enter-active,
  .expand-fade-leave-active {
    transition: none;
  }
}

@media (max-width: 899px) {
  .expand-row {
    justify-content: flex-start;
    overflow-x: auto;
    padding: 0 4px;
  }

  .expand-card {
    flex-basis: 32px;
    width: 32px;
    height: 256px;
    border-radius: 16px;
  }

  .expand-card.is-on {
    flex-basis: 192px;
    width: 192px;
  }
}
</style>
