<template>
  <DraftFrame>
    <section class="board" aria-labelledby="studies-label">
      <header class="board__head">
        <h1 id="studies-label" class="board__title">Studies</h1>
        <p class="board__count">{{ interactions.length }}+</p>
      </header>
      <div class="board__grid">
        <NuxtLink
          v-for="item in interactions"
          :key="item.slug"
          class="card"
          :to="`/studies/${item.slug}`"
          :aria-label="item.title"
        >
          <StudyPreview :slug="item.slug" />
        </NuxtLink>
      </div>
    </section>
  </DraftFrame>
</template>

<script setup lang="ts">
import { interactions } from '~/data/interactions'

useSiteSeo({
  title: 'Studies — Christian Anyikamadu',
  description: 'Interface studies by Christian Anyikamadu.',
  path: '/studies'
})
</script>

<style scoped>
.board {
  padding-top: 36px;
}

.board__head {
  display: flex;
  align-items: baseline;
  gap: 8px;
}

.board__title,
.board__count {
  font-size: 16px;
  font-weight: 500;
  line-height: 22px;
}

.board__count {
  color: var(--muted);
}

.board__grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 16px;
  margin-top: 22px;
}

.card {
  display: block;
  aspect-ratio: 16 / 10;
  border: 1px solid var(--line);
  background: #fafafa;
  overflow: hidden;
}

.card:hover {
  border-color: #cfcfcf;
}

[data-theme='dark'] .card {
  background: #0c0c0c;
}

[data-theme='dark'] .card:hover {
  border-color: #444444;
}

@media (max-width: 700px) {
  .board__grid {
    grid-template-columns: 1fr;
  }
}
</style>
