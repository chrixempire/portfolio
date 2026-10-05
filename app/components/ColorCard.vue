<template>
  <div ref="root" class="color-card" :style="{ background: color }" />
</template>

<script setup lang="ts">
withDefaults(defineProps<{
  color?: string
}>(), {
  color: 'var(--card)'
})
</script>

<style scoped>
.color-card {
  width: 100%;
  height: 100%;
  border-radius: inherit;
}
</style>
