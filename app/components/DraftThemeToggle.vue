<template>
  <button
    type="button"
    class="orb"
    aria-label="Toggle theme"
    @click="toggleTheme($event, 'rise')"
  >
    <span class="sr-only">Toggle theme</span>
    <svg viewBox="0 0 240 240" class="orb__mark" :class="{ 'is-dark': theme === 'dark' }" aria-hidden="true">
      <g class="orb__spin">
        <path d="M120 67.5C149.25 67.5 172.5 90.75 172.5 120C172.5 149.25 149.25 172.5 120 172.5" />
        <path d="M120 67.5C90.75 67.5 67.5 90.75 67.5 120C67.5 149.25 90.75 172.5 120 172.5" />
      </g>
      <path
        d="M120 3.75C55.5 3.75 3.75 55.5 3.75 120C3.75 184.5 55.5 236.25 120 236.25C184.5 236.25 236.25 184.5 236.25 120C236.25 55.5 184.5 3.75 120 3.75ZM120 214.5V172.5C90.75 172.5 67.5 149.25 67.5 120C67.5 90.75 90.75 67.5 120 67.5V25.5C172.5 25.5 214.5 67.5 214.5 120C214.5 172.5 172.5 214.5 120 214.5Z"
      />
    </svg>
  </button>
</template>

<script setup lang="ts">
const { theme, toggleTheme } = useTheme()
</script>

<style scoped>
.sr-only {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  white-space: nowrap;
  border: 0;
}

.orb {
  position: relative;
  width: 28px;
  height: 28px;
  padding: 0;
  border: 0;
  border-radius: 999px;
  background: #000000;
  cursor: pointer;
  display: grid;
  place-items: center;
  flex: 0 0 auto;
  box-shadow: none;
  transition: transform 0.3s ease;
}

.orb:focus {
  outline: none;
}

.orb:focus-visible {
  outline: 2px solid currentColor;
  outline-offset: 3px;
}

.orb:active {
  transform: scale(0.95);
}

[data-theme='dark'] .orb {
  background: #ffffff;
}

[data-theme='dark'] .orb__mark path {
  fill: #000000;
}

[data-theme='dark'] .orb__spin path:last-child {
  fill: #ffffff;
}

.orb__mark {
  width: 16px;
  height: 16px;
  overflow: visible;
}

.orb__mark path {
  fill: #ffffff;
}

.orb__spin path:last-child {
  fill: #000000;
}

.orb__spin,
.orb__mark > path {
  transform-origin: 120px 120px;
  transform-box: view-box;
  transition: transform 0.5s cubic-bezier(0.76, 0, 0.24, 1);
}

.orb__mark.is-dark .orb__spin {
  transform: rotate(-180deg);
}

.orb__mark.is-dark > path {
  transform: rotate(180deg);
}
</style>
