<template>
  <div class="creative" data-lenis-prevent>
    <div ref="root" class="swiper creative__swiper">
      <div class="swiper-wrapper">
        <div
          v-for="image in carouselImages"
          :key="image.src"
          class="swiper-slide"
        >
          <img
            class="creative__media"
            :src="image.src"
            :alt="image.alt"
          >
        </div>
      </div>
      <div class="swiper-pagination" />
    </div>
  </div>
</template>

<script setup lang="ts">
import Swiper from 'swiper'
import { EffectCreative, Pagination } from 'swiper/modules'
import { carouselImages } from '~/data/site'
import 'swiper/css'
import 'swiper/css/effect-creative'
import 'swiper/css/pagination'

const root = ref<HTMLElement | null>(null)
let instance: Swiper | null = null

const effect = {
  prev: {
    shadow: true,
    origin: 'left center',
    translate: ['-5%', 0, -200] as [string, number, number],
    rotate: [0, 100, 0] as [number, number, number]
  },
  next: {
    origin: 'right center',
    translate: ['5%', 0, -200] as [string, number, number],
    rotate: [0, -100, 0] as [number, number, number]
  }
}

onMounted(() => {
  if (!root.value) return

  instance = new Swiper(root.value, {
    modules: [EffectCreative, Pagination],
    effect: 'creative',
    grabCursor: true,
    slidesPerView: 'auto',
    centeredSlides: true,
    loop: true,
    watchSlidesProgress: true,
    pagination: {
      el: root.value.querySelector('.swiper-pagination') as HTMLElement,
      clickable: true
    },
    creativeEffect: effect
  })
})

onBeforeUnmount(() => {
  instance?.destroy()
  instance = null
})
</script>

<style>
.creative {
  width: 100%;
}

.creative__swiper {
  width: 100%;
  height: 440px;
  overflow: visible;
  padding-bottom: 50px;
  --swiper-pagination-color: #ededed;
  --swiper-pagination-bullet-inactive-color: #ededed;
  --swiper-pagination-bullet-inactive-opacity: 0.28;
  --swiper-pagination-bullet-size: 8px;
}

.creative__swiper .swiper-slide {
  width: 300px;
  height: 390px;
  overflow: hidden;
  border-radius: 25px;
  background: #1a1a1a;
}

.creative__media {
  display: block;
  width: 100%;
  height: 100%;
  object-fit: cover;
  transform: scale(1.05);
}

@media (max-width: 899px) {
  .creative__swiper {
    height: 360px;
  }

  .creative__swiper .swiper-slide {
    width: 240px;
    height: 310px;
  }
}
</style>
