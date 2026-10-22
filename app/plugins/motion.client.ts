import gsap from 'gsap'
import { ScrollTrigger } from 'gsap/ScrollTrigger'
import { SplitText } from 'gsap/SplitText'
import Lenis from 'lenis'
import 'lenis/dist/lenis.css'

export default defineNuxtPlugin(() => {
  gsap.registerPlugin(ScrollTrigger, SplitText)
  gsap.ticker.lagSmoothing(0)

  gsap.config({ force3D: true, nullTargetWarn: false })

  const lenis = new Lenis({
    autoRaf: false,
    lerp: 0.22,
    wheelMultiplier: 1.15,
    smoothWheel: true
  })

  lenis.on('scroll', ScrollTrigger.update)

  const tick = (time: number) => {
    lenis.raf(time * 1000)
  }

  gsap.ticker.add(tick)

  if (import.meta.hot) {
    import.meta.hot.dispose(() => {
      gsap.ticker.remove(tick)
      lenis.destroy()
      ScrollTrigger.getAll().forEach(trigger => trigger.kill())
    })
  }

  return {
    provide: {
      gsap,
      ScrollTrigger,
      SplitText,
      lenis
    }
  }
})
