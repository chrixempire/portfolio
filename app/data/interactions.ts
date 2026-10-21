export type InteractionSource = {
  label: string
  href: string
}

export type InteractionEntry = {
  slug: string
  title: string
  prompt: string
  idea: string
  how: string[]
  sources: InteractionSource[]
  stage: 'search' | 'default' | 'hover' | 'carousel' | 'otp' | 'stack' | 'accordion'
  wide?: boolean
}

export const interactions: InteractionEntry[] = [
  {
    slug: 'command-search',
    title: 'Command search',
    prompt: 'Press F or click the input to open. Type to filter, Esc to close.',
    idea: 'I took this from Skiper UI 92, the Vercel command menu. Closed, it is a small find field. Open, it becomes suggestions, settings, help, and docs.',
    how: [
      'The closed bar is 192 by 32, with a 6px radius. Its left edge stays fixed, and a GSAP timeline grows it to the right to 384px, sets the height from the list, and rounds the corners to 12px.',
      'The bar stretches to 48px and the F key becomes Esc. Closing runs the timeline backward and clears the query.',
      'Typing filters every group by label. Arrow keys move the highlight, Enter chooses a row, and Esc or a click outside closes it.'
    ],
    sources: [
      { label: 'Skiper UI 92', href: 'https://skiper-ui.com/v1/skiper92' }
    ],
    stage: 'search'
  },
  {
    slug: 'play-button',
    title: 'Play button',
    prompt: 'A circular control that springs open into a mini player.',
    idea: 'I took this from Skiper UI 3. It starts as a circle, then springs wider into a player with a track and a play mark.',
    how: [
      'The pill is 60px wide. Clicking it tweens the width to 330px with a back-out spring. Clicking again springs it shut.',
      'The track and the play icon are Vue transitions, so they only mount once the pill is open.',
      'On first view it scales up from below. Reduced motion skips the spring and shows the closed pill immediately.'
    ],
    sources: [
      { label: 'Skiper UI 3', href: 'https://skiper-ui.com/v1/skiper3' }
    ],
    stage: 'default'
  },
  {
    slug: 'card-expand',
    title: 'Card expand',
    prompt: 'Four equal cards to start. Click one to expand it; the others shrink into a row. Click outside to reset.',
    idea: 'I took this from Skiper UI 23. The layout is the Family and jakub.kr card: one card opens, and the rest compress into a row under it.',
    how: [
      'Closed, the four cards sit in a two-column grid. Clicking one switches the grid so that card spans the full width and the other three share the row beneath it.',
      'Before the DOM updates I record each card’s box. After the layout changes, GSAP animates from the old box to the new one, and the inner content counter-scales so the type does not stretch during the move.',
      'A click outside clears the open card and runs the same flip back to the grid.'
    ],
    sources: [
      { label: 'Skiper UI 23', href: 'https://skiper-ui.com/v1/skiper23' },
      { label: 'jakub.kr', href: 'https://www.jakub.kr' }
    ],
    stage: 'default'
  },
  {
    slug: 'hover-expand',
    title: 'Hover expand',
    prompt: 'Hover or click a strip. It widens into a square; the others stay thin.',
    idea: 'I took this from Skiper UI 52. Thin image strips sit in a row, and the one you hover opens into a square. The illustrations are by AarzooAly.',
    how: [
      'Each strip is 64 by 320. The active one grows to 320 by 320 with a CSS transition on width. The others stay thin.',
      'Hover, focus, or a click sets the active index. The gradient and the code label fade in only on the open strip.',
      'On a small screen the strips shrink and the row scrolls sideways so the open square still fits.'
    ],
    sources: [
      { label: 'Skiper UI 52', href: 'https://skiper-ui.com/v1/skiper52' },
      { label: 'AarzooAly', href: 'https://x.com/AarzooAly' }
    ],
    stage: 'hover',
    wide: true
  },
  {
    slug: 'creative-carousel',
    title: 'Creative carousel',
    prompt: 'Drag or swipe. The active slide stays facing you; neighbors fold away in 3D.',
    idea: 'I took this from Skiper UI 50 and built it with Swiper. The active slide stays flat. The slides beside it fold back in 3D. The illustrations are by AarzooAly.',
    how: [
      'Swiper runs with the creative effect, centered slides, and loop. Dragging or the pagination dots moves it.',
      'The previous slide is hinged on its left edge, shifted back in z, and rotated 100 degrees. The next slide mirrors that from the right.',
      'The active slide does not rotate, so it stays facing you while the neighbors fold away.'
    ],
    sources: [
      { label: 'Skiper UI 50', href: 'https://skiper-ui.com/v1/skiper50' },
      { label: 'Swiper', href: 'https://swiperjs.com/' },
      { label: 'AarzooAly', href: 'https://x.com/AarzooAly' }
    ],
    stage: 'carousel',
    wide: true
  },
  {
    slug: 'otp-input',
    title: 'OTP input',
    prompt: 'Type a code. Digits roll in behind a caret that slides from slot to slot.',
    idea: 'I took this from the Rare UI OTP input. Each digit rolls into its slot, and a caret slides across as you type.',
    how: [
      'There are six fields. The real input is transparent. The digit you see is a separate span, so it can roll in and out instead of just appearing.',
      'A caret sits on the row. When focus moves, GSAP slides it to the center of the active empty slot.',
      'Enter 123456 and each cell draws a green ring. Any other complete code shakes the row and outlines the cells in red.'
    ],
    sources: [
      { label: 'Rare UI', href: 'https://www.rareui.com/components/otpinput' }
    ],
    stage: 'otp'
  },
  {
    slug: 'scroll-stack',
    title: 'Scroll the stack',
    prompt: 'Cards pin as you scroll, then shrink and rotate to reveal the next one. The last card lands straight.',
    idea: 'I took this from Skiper UI 34. Cards pin in place while you scroll, then spin away to reveal the next one. The photos are from lummi.ai.',
    how: [
      'Each card is sticky at 10vh, so the next one slides up underneath it.',
      'ScrollTrigger scrubs every card except the last from full size down to scale 0 and a 100 degree rotation. The photo inside counter-rotates, so the picture stays readable while the frame spins off.',
      'The last card has no tween. It stays full size and lands straight.'
    ],
    sources: [
      { label: 'Skiper UI 34', href: 'https://skiper-ui.com/v1/skiper34' },
      { label: 'lummi.ai', href: 'https://www.lummi.ai' }
    ],
    stage: 'stack'
  },
  {
    slug: 'bouncy-accordion',
    title: 'Bouncy accordion',
    prompt: 'Click a row. It springs open and splits off the stack. Click it again to fold it back.',
    idea: 'I took this from Skiper UI 103. Closed rows sit in one rounded stack. The row you open springs taller, rounds on its own, and leaves a gap. The idea comes from Yanis.',
    how: [
      'Each row is 300 by 45, with a 20px radius only on the outer corners of a closed run. Opening one sets its height from the copy, gives it a full 20px radius, and adds 10px of space above and below.',
      'A GSAP elastic tween springs the height, margin, and corner radius, overshooting before they settle. The chevron turns with that same bounce, and the copy fades in while a blur clears.',
      'Only one row stays open. Opening another closes the current one on the same tween, and the neighbors rejoin into a single stack.'
    ],
    sources: [
      { label: 'Skiper UI 103', href: 'https://skiper-ui.com/v1/skiper103' },
      { label: 'Yanis', href: 'https://x.com/dev_ya' }
    ],
    stage: 'accordion'
  }
]

export const interactionBySlug = (slug: string) => interactions.find(item => item.slug === slug)
