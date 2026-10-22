<template>
  <span class="preview" :class="`preview--${slug}`" aria-hidden="true">
    <span v-if="slug === 'command-search'" class="pill">Find</span>
    <span v-else-if="slug === 'play-button'" class="orb" />
    <span v-else-if="slug === 'card-expand'" class="quad">
      <i /><i /><i /><i />
    </span>
    <span v-else-if="slug === 'hover-expand'" class="strips">
      <i /><i class="is-wide" /><i /><i />
    </span>
    <span v-else-if="slug === 'creative-carousel'" class="fan">
      <i /><i /><i />
    </span>
    <span v-else-if="slug === 'otp-input'" class="slots">
      <i>1</i><i>2</i><i>3</i><i /><i /><i />
    </span>
    <span v-else-if="slug === 'scroll-stack'" class="pile">
      <i /><i /><i />
    </span>
    <span v-else class="rows">
      <i /><i class="is-open" /><i />
    </span>
  </span>
</template>

<script setup lang="ts">
defineProps<{ slug: string }>()
</script>

<style scoped>
.preview {
  display: grid;
  place-items: center;
  width: 100%;
  height: 100%;
}

.pill,
.orb,
.quad,
.strips,
.fan,
.slots,
.pile,
.rows {
  display: flex;
  align-items: center;
}

.pill {
  width: 72px;
  height: 16px;
  border-radius: 999px;
  background: #111111;
  color: #ffffff;
  font-size: 8px;
  line-height: 16px;
  justify-content: center;
}

.orb {
  width: 28px;
  height: 28px;
  border-radius: 50%;
  background: #111111;
}

.quad {
  display: grid;
  grid-template-columns: 28px 28px;
  gap: 4px;
}

.quad i,
.strips i,
.fan i,
.slots i,
.pile i,
.rows i {
  display: block;
  background: #d9d9d9;
}

.quad i {
  width: 28px;
  height: 18px;
}

.quad i:first-child {
  grid-column: 1 / -1;
  width: 60px;
  background: #111111;
}

.strips {
  gap: 3px;
  height: 46px;
}

.strips i {
  width: 8px;
  height: 46px;
}

.strips .is-wide {
  width: 36px;
  background: #111111;
}

.fan {
  gap: 4px;
}

.fan i {
  width: 18px;
  height: 28px;
  background: #d0d0d0;
}

.fan i:nth-child(2) {
  height: 36px;
  background: #111111;
}

.slots {
  gap: 3px;
}

.slots i {
  width: 12px;
  height: 16px;
  color: #111111;
  font-size: 8px;
  font-style: normal;
  line-height: 16px;
  text-align: center;
}

.pile {
  position: relative;
  width: 64px;
  height: 58px;
}

.pile i {
  position: absolute;
  left: 8px;
  top: 20px;
  width: 48px;
  height: 16px;
  border: 0;
  border-radius: 2px;
  background: #111111;
}

.pile i:nth-child(1) {
  z-index: 1;
  transform: rotate(-16deg) translateY(-14px);
}

.pile i:nth-child(2) {
  z-index: 2;
  transform: rotate(-4deg) translateY(0);
}

.pile i:nth-child(3) {
  z-index: 3;
  transform: rotate(10deg) translateY(14px);
}

.rows {
  flex-direction: column;
  gap: 3px;
  width: 64px;
}

.rows i {
  width: 100%;
  height: 8px;
}

.rows .is-open {
  height: 18px;
  background: #111111;
}

[data-theme='dark'] .quad i,
[data-theme='dark'] .strips i,
[data-theme='dark'] .fan i,
[data-theme='dark'] .slots i,
[data-theme='dark'] .rows i {
  background: #333333;
}

[data-theme='dark'] .pile i {
  background: #ededed;
}

[data-theme='dark'] .pill,
[data-theme='dark'] .orb,
[data-theme='dark'] .quad i:first-child,
[data-theme='dark'] .strips .is-wide,
[data-theme='dark'] .fan i:nth-child(2),
[data-theme='dark'] .rows .is-open {
  background: #ededed;
  color: #111111;
}

[data-theme='dark'] .slots i {
  color: #ededed;
}
</style>
