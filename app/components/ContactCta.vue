<template>
  <section class="cta reveal">
    <div class="cta__copy">
      <p class="cta__kicker font-display">Get in touch with me</p>
      <h2 class="cta__title font-display">Got a project we could work on together?</h2>
    </div>
    <div class="cta__actions">
      <MagneticButton :href="site.calendly" external>Schedule an intro</MagneticButton>
      <MagneticButton variant="secondary" :href="`mailto:${site.email}`">Send email</MagneticButton>
    </div>
  </section>
</template>

<script setup lang="ts">
import { site } from '~/data/site'
</script>

<style scoped>
.cta {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 24px;
  width: 100%;
  text-align: center;
}

.cta__copy {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
}

.cta__kicker {
  font-size: 14px;
  line-height: 22px;
  font-weight: 500;
  color: var(--text-muted);
}

.cta__title {
  font-size: 40px;
  line-height: 52px;
  font-weight: 600;
  max-width: 453px;
}

.cta__actions {
  display: flex;
  gap: 16px;
  flex-wrap: wrap;
  justify-content: center;
}

@media (max-width: 899px) {
  .cta__title {
    font-size: 32px;
    line-height: 40px;
    max-width: 100%;
  }
}
</style>
