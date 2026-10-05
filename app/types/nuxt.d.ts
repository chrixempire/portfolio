import type { SplitText } from 'gsap/SplitText'
import type { ScrollTrigger } from 'gsap/ScrollTrigger'
import type Lenis from 'lenis'
import type gsap from 'gsap'

declare module '#app' {
  interface NuxtApp {
    $gsap: typeof gsap
    $ScrollTrigger: typeof ScrollTrigger
    $SplitText: typeof SplitText
    $lenis: Lenis
  }
}

export {}
