<template>
  <main class="page">
    <section class="block">
      <header class="block__copy">
        <p class="block__kicker">Interaction</p>
        <h1 class="block__title font-display">Command search</h1>
        <p class="block__body">
          Press F or click the input to open. Type to filter, Esc to close.
        </p>
      </header>
      <div class="stage stage--search" aria-label="Vercel command search">
        <CommandSearch />
      </div>
      <p class="credit">
        After
        <a href="https://skiper-ui.com/v1/skiper92" target="_blank" rel="noopener noreferrer">Skiper UI 92</a>.
        <NuxtLink to="/interaction/2032/command-search">Details</NuxtLink>
      </p>
    </section>

    <section class="block">
      <header class="block__copy">
        <h2 class="block__title font-display">Play button</h2>
        <p class="block__body">
          A circular control that springs open into a mini player.
        </p>
      </header>
      <div class="stage" aria-label="Apple play button">
        <ApplePlayButton />
      </div>
      <p class="credit">
        After
        <a href="https://skiper-ui.com/v1/skiper3" target="_blank" rel="noopener noreferrer">Skiper UI 3</a>.
        <NuxtLink to="/interaction/2032/play-button">Details</NuxtLink>
      </p>
    </section>

    <section class="block">
      <header class="block__copy">
        <h2 class="block__title font-display">Card expand</h2>
        <p class="block__body">
          Four equal cards to start. Click one to expand it; the others shrink into a row. Click outside to reset.
        </p>
      </header>
      <div class="stage" aria-label="Minimal card expand">
        <ExpandableCard />
      </div>
      <p class="credit">
        After
        <a href="https://skiper-ui.com/v1/skiper23" target="_blank" rel="noopener noreferrer">Skiper UI 23</a>.
        Inspired by Family and
        <a href="https://www.jakub.kr" target="_blank" rel="noopener noreferrer">jakub.kr</a>.
        <NuxtLink to="/interaction/2032/card-expand">Details</NuxtLink>
      </p>
    </section>

    <section class="block block--wide">
      <header class="block__copy">
        <h2 class="block__title font-display">Hover expand</h2>
        <p class="block__body">
          Hover or click a strip. It widens into a square; the others stay thin.
        </p>
      </header>
      <div class="stage stage--hover" aria-label="Hover expand gallery">
        <HoverExpand />
      </div>
      <p class="credit">
        After
        <a href="https://skiper-ui.com/v1/skiper52" target="_blank" rel="noopener noreferrer">Skiper UI 52</a>.
        Landscape photographs.
        <NuxtLink to="/interaction/2032/hover-expand">Details</NuxtLink>
      </p>
    </section>

    <section class="block block--wide">
      <header class="block__copy">
        <h2 class="block__title font-display">Creative carousel</h2>
        <p class="block__body">
          Drag or swipe. The active slide stays facing you; neighbors fold away in 3D.
        </p>
      </header>
      <div class="stage stage--carousel" aria-label="Creative carousel">
        <ClientOnly>
          <CreativeCarousel />
        </ClientOnly>
      </div>
      <p class="credit">
        After
        <a href="https://skiper-ui.com/v1/skiper50" target="_blank" rel="noopener noreferrer">Skiper UI 50</a>.
        Built with
        <a href="https://swiperjs.com/" target="_blank" rel="noopener noreferrer">Swiper</a>.
        Landscape photographs.
        <NuxtLink to="/interaction/2032/creative-carousel">Details</NuxtLink>
      </p>
    </section>

    <section class="block">
      <header class="block__copy">
        <h2 class="block__title font-display">OTP input</h2>
        <p class="block__body">
          Type a code. Digits roll in behind a caret that slides from slot to slot.
        </p>
      </header>
      <div class="stage stage--otp" aria-label="OTP input">
        <div class="otp-demo">
          <OtpInput
            :status="otpStatus"
            @change="onOtpChange"
            @complete="onOtpComplete"
          />
          <p class="otp-demo__hint">Enter 123456 to pass. Any other code fails.</p>
        </div>
      </div>
      <p class="credit">
        After
        <a href="https://www.rareui.com/components/otpinput" target="_blank" rel="noopener noreferrer">Rare UI</a>.
        <NuxtLink to="/interaction/2032/otp-input">Details</NuxtLink>
      </p>
    </section>

    <section class="block">
      <header class="block__copy">
        <h2 class="block__title font-display">Scroll the stack</h2>
        <p class="block__body">
          Cards pin as you scroll. The one underneath shrinks and turns while the next card slides up over it.
        </p>
      </header>
      <StickyCards />
      <p class="credit">
        After
        <a href="https://skiper-ui.com/v1/skiper34" target="_blank" rel="noopener noreferrer">Skiper UI 34</a>.
        Landscape photographs.
        Images from
        <a href="https://www.lummi.ai" target="_blank" rel="noopener noreferrer">lummi.ai</a>.
        <NuxtLink to="/interaction/2032/scroll-stack">Details</NuxtLink>
      </p>
    </section>

    <section class="block">
      <header class="block__copy">
        <h2 class="block__title font-display">Bouncy accordion</h2>
        <p class="block__body">
          Click a row. It springs open and splits off the stack. Click it again to fold it back.
        </p>
      </header>
      <div class="stage stage--accordion" aria-label="Bouncy accordion">
        <BouncyAccordion />
      </div>
      <p class="credit">
        After
        <a href="https://skiper-ui.com/v1/skiper103" target="_blank" rel="noopener noreferrer">Skiper UI 103</a>.
        Inspired by
        <a href="https://x.com/dev_ya" target="_blank" rel="noopener noreferrer">Yanis</a>.
        <NuxtLink to="/interaction/2032/bouncy-accordion">Details</NuxtLink>
      </p>
    </section>

    <AppFooter />
  </main>
</template>

<script setup lang="ts">
type OtpStatus = 'idle' | 'success' | 'error'

useSiteSeo({
  title: 'Interaction - Christian Anyikamadu',
  description: 'Frontend interaction studies by Christian Anyikamadu: command search, motion, OTP, and scroll experiments in Vue.'
})

const otpStatus = ref<OtpStatus>('idle')

const onOtpChange = () => {
  otpStatus.value = 'idle'
}

const onOtpComplete = (code: string) => {
  otpStatus.value = code === '123456' ? 'success' : 'error'
}
</script>

<style scoped>
.page {
  width: 100%;
}

.block {
  width: min(896px, calc(100% - 40px));
  margin: 0 auto;
  padding-top: 88px;
}

.block:first-child {
  padding-top: 72px;
}

.block--wide {
  width: min(1152px, calc(100% - 40px));
}

.block__copy {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 12px;
  width: 100%;
  text-align: start;
}

.block__kicker {
  font-size: 12px;
  line-height: 18px;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: var(--text-muted);
}

.block__title {
  font-size: 40px;
  line-height: 52px;
  font-weight: 600;
  color: var(--text);
}

.block__body {
  width: 100%;
  color: var(--text-muted);
}

.stage {
  width: 100%;
  margin-top: 40px;
  min-height: 420px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 32px;
  background: #0a0a0a;
}

.stage--search {
  min-height: 720px;
  align-items: center;
  background: #121212;
}

.stage--hover {
  min-height: 420px;
  padding: 32px 20px;
  overflow-x: auto;
}

.stage--carousel {
  min-height: 500px;
  padding: 40px 0 24px;
  overflow: visible;
}

.stage--otp {
  min-height: 420px;
}

.stage--accordion {
  min-height: 520px;
  background: #121212;
}

.otp-demo {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 24px;
}

.otp-demo__hint {
  font-size: 14px;
  line-height: 22px;
  color: #a1a1a1;
  text-align: center;
}

.credit {
  width: 100%;
  margin-top: 16px;
  font-size: 12px;
  line-height: 18px;
  color: var(--text-footer);
  text-align: start;
}

.credit a {
  color: var(--text-nav);
  text-decoration: underline;
  text-decoration-style: dotted;
  text-underline-offset: 3px;
}

@media (max-width: 899px) {
  .block {
    width: min(373px, calc(100% - 40px));
    padding-top: 64px;
  }

  .block:first-child {
    padding-top: 56px;
  }

  .block__title {
    font-size: 32px;
    line-height: 40px;
  }

  .stage {
    min-height: 360px;
    border-radius: 24px;
  }

  .stage--search {
    min-height: 700px;
  }
}
</style>
