<template>
  <div class="ledger">
    <header class="top">
      <nav class="menu" aria-label="Site">
        <NuxtLink to="/" :class="{ 'is-on': route.path === '/' }">Work</NuxtLink>
        <NuxtLink to="/studies" :class="{ 'is-on': route.path.startsWith('/studies') }">Studies</NuxtLink>
      </nav>
      <div class="end">
        <DraftThemeToggle />
      </div>
    </header>
    <slot />
  </div>
</template>

<script setup lang="ts">
const route = useRoute()
</script>

<style>
.ledger {
  --ink: #000000;
  --muted: #6b6b6b;
  --copy: #4a4a4a;
  --line: #e6e6e6;
  --rule: #d4d4d4;
  --still: #f2f2f2;
  width: min(720px, calc(100% - 40px));
  margin: 0 auto;
  padding: 28px 0 88px;
  color: var(--ink);
  font-family: Inter, ui-sans-serif, system-ui, sans-serif;
  font-weight: 500;
  font-size: 14px;
  line-height: 22px;
}

[data-theme='dark'] .ledger {
  --ink: #ffffff;
  --muted: #8a8a8a;
  --copy: #b5b5b5;
  --line: #222222;
  --rule: #333333;
  --still: #111111;
}

.ledger .top,
.ledger .links,
.ledger .quiet,
.ledger .menu,
.ledger .when,
.ledger .phone {
  font-family: Inter, ui-sans-serif, system-ui, sans-serif;
}

.ledger .top {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 16px;
  font-size: 14px;
  font-weight: 500;
  line-height: 21px;
}

.ledger .end {
  display: flex;
  align-items: center;
  gap: 16px;
}

.ledger .menu {
  display: flex;
  gap: 18px;
}

.ledger .menu a {
  color: var(--muted);
}

.ledger .menu a.is-on {
  color: var(--ink);
}

.ledger .quiet {
  color: var(--muted);
  text-decoration: underline;
  text-underline-offset: 3px;
}

.ledger .intro {
  padding-top: 28px;
}

.ledger .portrait {
  width: 56px;
  height: 56px;
  border-radius: 50%;
  object-fit: cover;
}

.ledger .name {
  margin-top: 14px;
  font-size: 14px;
  font-weight: 500;
  line-height: 22px;
  letter-spacing: 0;
}

.ledger .role {
  margin-top: 4px;
  color: var(--muted);
  font-size: 13px;
  font-weight: 500;
  line-height: 19px;
}

.ledger .prose {
  max-width: 62ch;
  margin-top: 14px;
  font-size: 14px;
  font-weight: 500;
  line-height: 24px;
}

.ledger .role + .prose {
  margin-top: 26px;
}

.ledger .links {
  display: flex;
  flex-wrap: wrap;
  gap: 8px 16px;
  margin-top: 16px;
  font-size: 14px;
  font-weight: 500;
  line-height: 22px;
}

.ledger .links a,
.ledger .mail {
  text-decoration: underline;
  text-decoration-color: var(--rule);
  text-underline-offset: 3px;
}

.ledger .links a:hover,
.ledger .row:hover .title,
.ledger .mail:hover {
  text-decoration-color: var(--ink);
}

.ledger .block {
  margin-top: 40px;
}

.ledger .label {
  color: var(--ink);
  font-size: 20px;
  font-weight: 500;
  line-height: 22px;
}

.ledger .rows {
  margin-top: 8px;
  list-style: none;
}

.ledger .row,
.ledger .job {
  display: grid;
  grid-template-columns: 32px minmax(0, 1fr) 148px;
  gap: 14px;
  align-items: start;
  padding: 10px 0;
  border-top: 1px solid var(--line);
  color: inherit;
}

.ledger .rows li:last-child .row,
.ledger .rows li:last-child.job {
  border-bottom: 1px solid var(--line);
}

.ledger .job {
  grid-template-columns: 168px minmax(0, 1fr);
}

.ledger .row--study {
  grid-template-columns: minmax(0, 1fr);
}

.ledger .index,
.ledger .when {
  color: var(--muted);
  font-size: 14px;
  font-weight: 500;
  line-height: 22px;
}

.ledger .when {
  padding-top: 2px;
}

.ledger .title {
  display: block;
  font-size: 16px;
  font-weight: 500;
  line-height: 24px;
}

.ledger .row .title {
  display: inline-flex;
  align-items: center;
  gap: 6px;
}

.ledger .point {
  width: 14px;
  height: 14px;
  flex: none;
  fill: none;
  stroke: currentColor;
  stroke-width: 1.4;
  stroke-linecap: round;
  stroke-linejoin: round;
}

.ledger .job .title,
.ledger .row--study .title {
  font-size: 14px;
  font-weight: 500;
  line-height: 22px;
}

.ledger .body {
  display: block;
  margin-top: 4px;
  color: var(--copy);
  font-size: 14px;
  font-weight: 400;
  line-height: 24px;
}

.ledger .row .body {
  font-size: 13px;
  line-height: 20px;
}

.ledger .still {
  width: 148px;
  height: 96px;
  object-fit: cover;
  border-radius: 8px;
  background: var(--still);
  transition: transform 0.35s ease;
}

.ledger .row:hover .still {
  transform: translateY(-2px);
}

.ledger .close {
  margin-top: 40px;
}

.ledger .mail {
  display: inline-block;
  margin-top: 8px;
  font-size: 14px;
  font-weight: 500;
  line-height: 22px;
  letter-spacing: 0;
  text-underline-offset: 3px;
}

.ledger .phone {
  margin-top: 4px;
  color: var(--muted);
  font-size: 14px;
  font-weight: 500;
  line-height: 22px;
}

.ledger .row:focus-visible,
.ledger .links a:focus-visible,
.ledger .mail:focus-visible,
.ledger .quiet:focus-visible,
.ledger .menu a:focus-visible {
  outline: 2px solid var(--ink);
  outline-offset: 3px;
}

@media (max-width: 700px) {
  .ledger .row,
  .ledger .job {
    grid-template-columns: 24px minmax(0, 1fr);
  }

  .ledger .still {
    grid-column: 2;
    width: 100%;
    height: 160px;
  }

  .ledger .job {
    grid-template-columns: 1fr;
    gap: 4px;
  }

}
</style>
