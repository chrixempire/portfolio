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
    idea: 'Closed, it is a small find field. Open, it becomes suggestions, settings, help, and docs.',
    how: [
      'The closed bar is 192 by 32, with a 6px radius. Its left edge stays fixed, and a CSS transition grows it to the right to 384px, sets the height from the list, and rounds the corners to 12px.',
      'The bar stretches to 48px and the F key becomes Esc. Closing reverses the same transition and clears the query.',
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
    idea: 'It starts as a circle, then springs wider into a player with a track and a play mark.',
    how: [
      'The pill is 60px wide. Clicking it eases the width to 330px. Clicking again eases it shut.',
      'The track and the play icon are Vue transitions, so they only mount once the pill is open.',
      'On first view the closed pill is already there. Reduced motion skips the width animation.'
    ],
    sources: [
      { label: 'Skiper UI 3', href: 'https://skiper-ui.com/v1/skiper3' }
    ],
    stage: 'default'
  },
  {
    slug: 'card-expand',
    title: 'Card expand',
    prompt: 'Four equal cards to start. The round menu opens one; the others shrink into a row. Click outside to reset.',
    idea: 'One account card opens, and the other three compress into a row under it.',
    how: [
      'Closed, the four cards sit in two rows inside a 360 by 300 frame. Each card is 160 by 125, with a 24px radius and a 16px gap.',
      'The round menu opens a card. That card grows to the full 360 by 180, and the other three share a 100px row underneath. The icon, name, and balance travel with the card on the layout spring.',
      'A click outside closes the open card and springs the grid back.'
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
    idea: 'Thin landscape stills sit in a row. The one under the pointer opens into a square, and the label only appears on that strip.',
    how: [
      'Each strip is 64 by 320. The active one grows to 320 by 320 with a CSS transition on width. The others stay thin.',
      'Hover, focus, or a click sets the active index. The gradient and the code label fade in only on the open strip.',
      'On a small screen the strips shrink and the row scrolls sideways so the open square still fits.'
    ],
    sources: [
      { label: 'Skiper UI 52', href: 'https://skiper-ui.com/v1/skiper52' }
    ],
    stage: 'hover',
    wide: true
  },
  {
    slug: 'creative-carousel',
    title: 'Creative carousel',
    prompt: 'Drag or swipe. The active slide stays facing you; neighbors fold away in 3D.',
    idea: 'Landscape stills sit in a loop. The active slide stays flat, and the ones beside it fold back in 3D.',
    how: [
      'Dragging moves the track. On release it eases to the nearest slide. The dots do the same jump.',
      'The slide leaving hinges on its outer edge, shifts 200px back, and rotates 100 degrees. A shadow falls on the one moving left. The incoming slide opens from the other edge.',
      'The active slide stays flat and in front, so it faces you while the neighbors fold away.'
    ],
    sources: [
      { label: 'Skiper UI 50', href: 'https://skiper-ui.com/v1/skiper50' }
    ],
    stage: 'carousel',
    wide: true
  },
  {
    slug: 'otp-input',
    title: 'OTP input',
    prompt: 'Type a code. Digits roll in behind a caret that slides from slot to slot.',
    idea: 'Each digit rolls into its slot, and a caret slides across as you type.',
    how: [
      'There are six fields. The real input is transparent. The digit you see is a separate span, so it can roll in and out instead of just appearing.',
      'A caret sits on the row. When focus moves, a CSS transform slides it to the center of the active empty slot.',
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
    prompt: 'Cards pin as you scroll. The one underneath shrinks and turns while the next card slides up over it.',
    idea: 'Wide landscape cards pin near the top of the screen. Scroll, and the card underneath tips while the next one covers it.',
    how: [
      'Each photo is its own card, the same width as this text, 80vh tall, with a 32px radius. They sit in one column with a 10vh gap, and each card pins 10vh from the top.',
      'The moment a card reaches that pin, further scrolling shrinks the frame and turns it, spread across a long scroll. The photo turns the other way and is scaled to 125%, so the picture stays level and still fills the tilted corners.',
      'The next card slides up and covers the one that is tipping. The card in front stays full size until it reaches the pin.'
    ],
    sources: [
      { label: 'Skiper UI 34', href: 'https://skiper-ui.com/v1/skiper34' }
    ],
    stage: 'stack'
  },
  {
    slug: 'bouncy-accordion',
    title: 'Bouncy accordion',
    prompt: 'Click a row. It springs open and splits off the stack. Click it again to fold it back.',
    idea: 'Closed rows sit in one rounded stack. The row you open springs taller, rounds on its own, and leaves a gap.',
    how: [
      'Each row is 300 by 45, with a 20px radius only on the outer corners of a closed run. Opening one sets its height from the copy, gives it a full 20px radius, and adds 10px of space above and below.',
      'A Motion spring animates the height, margin, and corner radius, overshooting before they settle. The chevron turns with that same bounce, and the copy fades in while a blur clears.',
      'Only one row stays open. Opening another closes the current one on the same spring, and the neighbors rejoin into a single stack.'
    ],
    sources: [
      { label: 'Skiper UI 103', href: 'https://skiper-ui.com/v1/skiper103' },
      { label: 'Yanis', href: 'https://x.com/dev_ya' }
    ],
    stage: 'accordion'
  }
]

export const interactionBySlug = (slug: string) => interactions.find(item => item.slug === slug)
