export function useBoot() {
  const booting = useState('booting', () => true)
  const unfolded = useState('unfolded', () => false)

  const finishBoot = () => {
    booting.value = false
  }

  const finishUnfold = () => {
    unfolded.value = true
  }

  return { booting, unfolded, finishBoot, finishUnfold }
}

export function prefersReducedMotion() {
  return import.meta.client && window.matchMedia('(prefers-reduced-motion: reduce)').matches
}

export function hasFinePointer() {
  return import.meta.client && window.matchMedia('(pointer: fine)').matches
}
