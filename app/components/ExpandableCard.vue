<template>
  <div
    ref="root"
    class="wallet"
    :class="active ? 'is-open' : 'is-grid'"
    aria-label="Wallet cards"
  >
    <article
      v-for="item in wallets"
      :key="item.id"
      :data-wallet="item.id"
      class="wallet-card"
      :class="{ 'is-featured': item.id === active }"
      :style="{ '--card': item.color }"
      @click="select(item.id)"
    >
      <div class="wallet-card__inner">
        <div class="wallet-card__top">
          <span class="wallet-card__icon" aria-hidden="true">
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
          </span>

          <button
            v-if="item.id === active"
            class="wallet-card__copy"
            type="button"
            @click.stop="copyAddress"
          >
            {{ copied ? 'Copied' : 'Copy Address' }}
            <svg viewBox="0 0 16 16" fill="none" aria-hidden="true">
              <rect x="5.2" y="5.2" width="7.3" height="7.3" rx="1.4" stroke="currentColor" stroke-width="1.3" />
              <path d="M3.5 10.2V3.9A.9.9 0 0 1 4.4 3h6.3" stroke="currentColor" stroke-width="1.3" />
            </svg>
          </button>
          <span v-else class="wallet-card__dots" aria-hidden="true">
            <i /><i /><i />
          </span>
        </div>

        <div class="wallet-card__bottom">
          <div class="wallet-card__meta">
            <p class="wallet-card__name">{{ item.name }}</p>
            <p class="wallet-card__balance">{{ item.balance }}</p>
          </div>
          <span v-if="item.id === active" class="wallet-card__customize">Customize</span>
        </div>
      </div>
    </article>
  </div>
</template>

<script setup lang="ts">
const wallets = [
  { id: 'gxuri', name: 'Gxuri', balance: '1.03 ETH', color: '#c084fc', icon: 'sparkle' },
  { id: 'savings', name: 'Savings', balance: '25.08 ETH', color: '#111111', icon: 'bookmark' },
  { id: 'staked', name: 'Staked', balance: '0.04 ETH', color: '#2ee6f0', icon: 'cloud' },
  { id: 'spending', name: 'Spending', balance: '0 ETH', color: '#4d8ef7', icon: 'anchor' }
] as const

type WalletId = (typeof wallets)[number]['id']

const root = ref<HTMLElement | null>(null)
const active = ref<WalletId | null>(null)
const copied = ref(false)
const { $gsap } = useNuxtApp()
const { unfolded } = useBoot()
let entered = false

const cards = () => Array.from(root.value?.querySelectorAll<HTMLElement>('[data-wallet]') ?? [])

const flipTo = (id: WalletId | null) => {
  const gsap = $gsap
  if (id === active.value) return

  if (!gsap || prefersReducedMotion()) {
    active.value = id
    return
  }

  const first = new Map(cards().map(node => [node.dataset.wallet, node.getBoundingClientRect()]))
  active.value = id

  nextTick(() => {
    cards().forEach((node) => {
      const before = first.get(node.dataset.wallet)
      if (!before) return
      const after = node.getBoundingClientRect()
      const dx = before.left - after.left
      const dy = before.top - after.top
      const sx = before.width / Math.max(after.width, 1)
      const sy = before.height / Math.max(after.height, 1)
      const inner = node.querySelector<HTMLElement>('.wallet-card__inner')

      gsap.set(node, { transformOrigin: 'top left' })
      gsap.fromTo(node, {
        x: dx,
        y: dy,
        scaleX: sx,
        scaleY: sy
      }, {
        x: 0,
        y: 0,
        scaleX: 1,
        scaleY: 1,
        duration: 0.7,
        ease: 'expo.out',
        overwrite: 'auto'
      })

      if (inner) {
        gsap.set(inner, { transformOrigin: 'top left' })
        gsap.fromTo(inner, {
          scaleX: 1 / sx,
          scaleY: 1 / sy
        }, {
          scaleX: 1,
          scaleY: 1,
          duration: 0.7,
          ease: 'expo.out',
          overwrite: 'auto'
        })
      }
    })
  })
}

const select = (id: WalletId) => flipTo(id)

const copyAddress = async () => {
  try {
    await navigator.clipboard.writeText('gxuri.eth')
    copied.value = true
    window.setTimeout(() => { copied.value = false }, 1400)
  } catch {
    copied.value = false
  }
}

const onPointer = (event: PointerEvent) => {
  if (!active.value || !root.value) return
  if (!root.value.contains(event.target as Node)) flipTo(null)
}

const playIntro = () => {
  const gsap = $gsap
  if (entered || !gsap || !root.value) return
  entered = true
  if (prefersReducedMotion()) return
  gsap.fromTo(cards(), {
    opacity: 0,
    y: 16,
    scale: 0.96
  }, {
    opacity: 1,
    y: 0,
    scale: 1,
    duration: 0.65,
    stagger: 0.04,
    ease: 'expo.out'
  })
}

onMounted(() => {
  watch(unfolded, (value) => {
    if (value) nextTick(playIntro)
  }, { immediate: true })
  document.addEventListener('pointerdown', onPointer)
})

onBeforeUnmount(() => {
  document.removeEventListener('pointerdown', onPointer)
})
</script>

<style scoped>
.wallet {
  display: grid;
  width: min(340px, 100%);
  gap: 12px;
}

.wallet.is-grid {
  grid-template-columns: 1fr 1fr;
}

.wallet.is-open {
  grid-template-columns: 1fr 1fr 1fr;
}

.wallet-card {
  height: 108px;
  overflow: hidden;
  border-radius: 22px;
  background: var(--card);
  color: #fff;
  cursor: pointer;
  will-change: transform;
}

.wallet.is-open .wallet-card.is-featured {
  grid-column: 1 / -1;
  order: -1;
  height: 168px;
  border-radius: 28px;
  cursor: default;
}

.wallet.is-open .wallet-card:not(.is-featured) {
  height: 92px;
  border-radius: 20px;
}

.wallet-card__inner {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  padding: 14px 16px 12px;
  transform-origin: top left;
}

.wallet-card.is-featured .wallet-card__inner {
  padding: 18px 20px 16px;
}

.wallet-card__top,
.wallet-card__bottom {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 10px;
}

.wallet-card__bottom {
  align-items: flex-end;
}

.wallet-card__icon {
  display: flex;
  width: 22px;
  height: 22px;
  color: #fff;
}

.wallet-card__icon svg {
  width: 100%;
  height: 100%;
}

.wallet-card__dots {
  display: flex;
  align-items: center;
  gap: 3px;
  height: 22px;
}

.wallet-card__dots i {
  width: 3.5px;
  height: 3.5px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.88);
}

.wallet-card__copy {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  color: #fff;
  font-size: 13px;
  line-height: 18px;
  font-weight: 500;
}

.wallet-card__copy svg {
  width: 14px;
  height: 14px;
}

.wallet-card__name {
  font-size: 15px;
  line-height: 20px;
  font-weight: 600;
}

.wallet-card__balance {
  font-size: 12px;
  line-height: 18px;
  color: rgba(255, 255, 255, 0.78);
}

.wallet-card.is-featured .wallet-card__name {
  font-size: 16px;
}

.wallet-card__customize {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  height: 32px;
  padding: 0 14px;
  border-radius: 999px;
  background: #fff;
  color: #1f1f1f;
  font-size: 13px;
  font-weight: 600;
}

.wallet.is-open .wallet-card:not(.is-featured) .wallet-card__name {
  font-size: 13px;
  line-height: 18px;
}

.wallet.is-open .wallet-card:not(.is-featured) .wallet-card__balance {
  font-size: 11px;
  line-height: 16px;
}

.wallet.is-open .wallet-card:not(.is-featured) .wallet-card__inner {
  padding: 12px 12px 10px;
}
</style>
