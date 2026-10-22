<template>
  <LayoutGroup>
    <div ref="root" class="wallet">
      <div v-for="(row, rowIndex) in rows" :key="rowIndex" class="wallet__row">
        <motion.article
          v-for="item in row"
          :key="item.id"
          layout
          :layout-id="`card-${item.id}`"
          class="card"
          :class="mode(item.id)"
          :style="{ background: item.color }"
        >
          <div class="card__top">
            <motion.div :layout-id="`icon-${item.id}`" class="icon">
              <svg v-if="item.icon === 'sparkle'" viewBox="0 0 24 24" fill="currentColor">
                <path d="M8.4 8.4 12 2.5l3.6 5.9L21.5 12l-5.9 3.6L12 21.5l-3.6-5.9L2.5 12l5.9-3.6Z" />
              </svg>
              <svg v-else-if="item.icon === 'bookmark'" viewBox="0 0 24 24" fill="currentColor">
                <path d="M7 3.75A2.75 2.75 0 0 0 4.25 6.5v13.1c0 .7.76 1.13 1.36.77L12 16.6l6.39 3.77c.6.36 1.36-.07 1.36-.77V6.5A2.75 2.75 0 0 0 17 3.75H7z" />
              </svg>
              <svg v-else-if="item.icon === 'cloud'" viewBox="0 0 24 24" fill="currentColor">
                <path d="M7.8 18.5h9.3a4.7 4.7 0 0 0 .7-9.35 6 6 0 0 0-11.4 1.7A4.1 4.1 0 0 0 7.8 18.5z" />
              </svg>
              <svg v-else viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8">
                <circle cx="12" cy="7" r="2.1" />
                <path d="M12 9.2V21M8.2 13H12c3.4 0 5.8 1.7 5.8 4.2" />
                <path d="M6.2 17.2A6.6 6.6 0 0 0 12 21a6.6 6.6 0 0 0 5.8-3.8" />
              </svg>
            </motion.div>

            <AnimatePresence>
              <motion.button
                v-if="active !== item.id"
                :key="`dots-${item.id}`"
                type="button"
                class="dots"
                aria-label="Open card"
                :initial="{ opacity: 0, filter: 'blur(2px)' }"
                :animate="{ opacity: 1, filter: 'blur(0px)' }"
                :exit="{ opacity: 0, filter: 'blur(2px)' }"
                @click.stop="toggle(item.id)"
              >
                <svg viewBox="0 0 16 16" aria-hidden="true">
                  <circle cx="3.2" cy="8" r="1.25" />
                  <circle cx="8" cy="8" r="1.25" />
                  <circle cx="12.8" cy="8" r="1.25" />
                </svg>
              </motion.button>
            </AnimatePresence>
          </div>

          <AnimatePresence>
            <motion.button
              v-if="active === item.id"
              key="copy-address"
              layout
              layout-id="copy-address"
              type="button"
              class="copy"
              @click.stop="copyAddress"
            >
              {{ copied ? 'Copied' : 'Copy Address' }}
              <span class="copy__mark" aria-hidden="true">
                <svg viewBox="0 0 16 16" fill="none">
                  <rect x="5.2" y="5.2" width="7.3" height="7.3" rx="1.4" stroke="currentColor" stroke-width="1.3" />
                  <path d="M3.5 10.2V3.9A.9.9 0 0 1 4.4 3h6.3" stroke="currentColor" stroke-width="1.3" />
                </svg>
              </span>
            </motion.button>
          </AnimatePresence>

          <AnimatePresence>
            <motion.span
              v-if="active === item.id"
              key="customize"
              layout
              layout-id="customize"
              class="customize"
            >Customize</motion.span>
          </AnimatePresence>

          <div class="card__meta">
            <motion.p :layout-id="`title-${item.id}`" class="name">{{ item.name }}</motion.p>
            <motion.p :layout-id="`balance-${item.id}`" class="balance">{{ item.balance }}</motion.p>
          </div>
        </motion.article>
      </div>
    </div>
  </LayoutGroup>
</template>

<script setup lang="ts">
import { AnimatePresence, LayoutGroup, motion } from 'motion-v'

const wallets = [
  { id: 'gosource', name: 'GoSource', balance: 'Orders', color: '#1f3d36', icon: 'bookmark' },
  { id: 'kaorex', name: 'Kaorex', balance: 'Escrow', color: '#c45c38', icon: 'cloud' },
  { id: 'bayana', name: 'Bayana', balance: 'Events', color: '#c8963e', icon: 'anchor' },
  { id: 'quality', name: 'Quality', balance: 'Notes', color: '#3e4c6b', icon: 'sparkle' }
] as const

type WalletId = (typeof wallets)[number]['id']

const root = ref<HTMLElement | null>(null)
const active = ref<WalletId | null>(null)
const copied = ref(false)

const rows = computed(() => {
  if (!active.value) return [wallets.slice(0, 2), wallets.slice(2)]
  const open = wallets.filter(item => item.id === active.value)
  const rest = wallets.filter(item => item.id !== active.value)
  return [open, rest]
})

const mode = (id: WalletId) => {
  if (active.value === id) return 'is-open'
  if (active.value) return 'is-shrunk'
  return 'is-closed'
}

const toggle = (id: WalletId) => {
  active.value = active.value === id ? null : id
  copied.value = false
}

const copyAddress = async () => {
  try {
    await navigator.clipboard.writeText('orders.gosource.app')
    copied.value = true
    window.setTimeout(() => { copied.value = false }, 1400)
  } catch {
    copied.value = false
  }
}

const onPointer = (event: MouseEvent) => {
  if (!active.value || !root.value) return
  if (!root.value.contains(event.target as Node)) active.value = null
}

onMounted(() => {
  document.addEventListener('mousedown', onPointer)
})

onBeforeUnmount(() => {
  document.removeEventListener('mousedown', onPointer)
})
</script>

<style scoped>
.wallet {
  display: flex;
  flex-direction: column;
  justify-content: flex-end;
  gap: 16px;
  width: 360px;
  max-width: 100%;
  height: 300px;
}

.wallet__row {
  display: flex;
  gap: 16px;
  width: 100%;
}

.card {
  position: relative;
  display: flex;
  flex: none;
  flex-direction: column;
  align-items: flex-start;
  justify-content: space-between;
  overflow: hidden;
  box-sizing: border-box;
  padding: 12px;
  border-radius: 24px;
  color: #ffffff;
  transform-origin: 50% 50%;
}

.card.is-closed {
  width: 160px;
  height: 125px;
}

.card.is-open {
  width: 100%;
  height: 180px;
}

.card.is-shrunk {
  flex: 1 1 0;
  width: auto;
  min-width: 0;
  height: 100px;
}

.card__top {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  width: 100%;
}

.icon {
  display: flex;
  flex: none;
  color: #ffffff;
}

.is-closed .icon {
  width: 32px;
  height: 32px;
}

.is-open .icon {
  width: 48px;
  height: 48px;
}

.is-shrunk .icon {
  width: 24px;
  height: 24px;
}

.icon svg {
  width: 100%;
  height: 100%;
}

.dots {
  display: flex;
  flex: none;
  align-items: center;
  justify-content: center;
  width: 24px;
  height: 24px;
  padding: 2px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.2);
  color: #ffffff;
  cursor: pointer;
}

.dots:hover {
  background: rgba(255, 255, 255, 0.3);
}

.dots svg {
  width: 16px;
  height: 16px;
  fill: currentColor;
}

.copy {
  position: absolute;
  top: 16px;
  right: 16px;
  display: inline-flex;
  align-items: center;
  gap: 12px;
  color: #ffffff;
  font-size: 16px;
  font-weight: 600;
  letter-spacing: -0.025em;
  line-height: 24px;
  cursor: pointer;
}

.copy__mark {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 16px;
  height: 16px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.2);
}

.copy__mark svg {
  width: 10px;
  height: 10px;
}

.customize {
  position: absolute;
  right: 16px;
  bottom: 16px;
  padding: 4px 8px;
  border-radius: 999px;
  background: rgba(255, 255, 255, 0.2);
  color: #ffffff;
  font-size: 16px;
  font-weight: 600;
  letter-spacing: -0.025em;
  line-height: 24px;
}

.card__meta {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
}

.name,
.balance {
  margin: 0;
  font-weight: 600;
}

.name {
  color: #ffffff;
}

.balance {
  color: rgba(255, 255, 255, 0.5);
}

.is-closed .name {
  font-size: 16px;
  line-height: 24px;
}

.is-closed .balance {
  font-size: 14px;
  line-height: 20px;
}

.is-open .name {
  font-size: 20px;
  line-height: 28px;
}

.is-open .balance {
  font-size: 18px;
  line-height: 28px;
}

.is-shrunk .name {
  font-size: 14px;
  line-height: 20px;
}

.is-shrunk .balance {
  font-size: 12px;
  line-height: 16px;
}
</style>
