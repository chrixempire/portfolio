export type ThemeName = 'light' | 'dark'

export function useTheme() {
  const theme = useState<ThemeName>('theme', () => 'light')
  const transitioning = useState('theme-transitioning', () => false)

  const applyTheme = (next: ThemeName) => {
    theme.value = next
    if (!import.meta.client) return
    document.documentElement.dataset.theme = next
    localStorage.setItem('theme', next)
    const meta = document.querySelector('meta[name="theme-color"]')
    if (meta) meta.setAttribute('content', next === 'dark' ? '#000000' : '#ffffff')
  }

  const initTheme = () => {
    if (!import.meta.client) return
    const stored = localStorage.getItem('theme') as ThemeName | null
    const next = stored || (window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light')
    applyTheme(next)
  }

  const toggleTheme = async (event?: MouseEvent) => {
    if (!import.meta.client || transitioning.value) return
    const next: ThemeName = theme.value === 'light' ? 'dark' : 'light'
    const reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches
    const x = event?.clientX ?? window.innerWidth - 48
    const y = event?.clientY ?? 48

    const commit = () => applyTheme(next)

    if (reduced || typeof document.startViewTransition !== 'function') {
      commit()
      window.dispatchEvent(new CustomEvent('theme-change', { detail: { x, y } }))
      return
    }

    transitioning.value = true
    const transition = document.startViewTransition(commit)

    try {
      await transition.ready
      const endRadius = Math.hypot(
        Math.max(x, window.innerWidth - x),
        Math.max(y, window.innerHeight - y)
      )
      document.documentElement.animate(
        {
          clipPath: [
            `circle(0px at ${x}px ${y}px)`,
            `circle(${endRadius}px at ${x}px ${y}px)`
          ]
        },
        {
          duration: 900,
          easing: 'cubic-bezier(0.76, 0, 0.24, 1)',
          pseudoElement: '::view-transition-new(root)'
        }
      )
      await transition.finished
    } finally {
      transitioning.value = false
      window.dispatchEvent(new CustomEvent('theme-change', { detail: { x, y } }))
    }
  }

  return { theme, transitioning, initTheme, toggleTheme, applyTheme }
}
