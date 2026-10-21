export type ToastType = 'success'

export type ToastInput = {
  type?: ToastType
  title: string
  description?: string
  timeout?: number
}

export type ToastSwipe = 'down' | 'right'

export type ToastRecord = {
  id: number
  type: ToastType
  title: string
  description?: string
  timeout: number
  starting: boolean
  ending: boolean
  swipe?: ToastSwipe
}

const items = ref<ToastRecord[]>([])
const timers = new Map<number, number>()
let seed = 0

const remove = (id: number) => {
  items.value = items.value.filter(item => item.id !== id)
  const timer = timers.get(id)
  if (timer) {
    window.clearTimeout(timer)
    timers.delete(id)
  }
}

export const toast = {
  add(input: ToastInput) {
    const id = ++seed
    const record: ToastRecord = {
      id,
      type: input.type ?? 'success',
      title: input.title,
      description: input.description,
      timeout: input.timeout ?? 3200,
      starting: true,
      ending: false
    }

    const next = [...items.value, record]
    next.slice(0, Math.max(0, next.length - 3)).forEach((item) => {
      const timer = timers.get(item.id)
      if (timer) window.clearTimeout(timer)
      timers.delete(item.id)
    })
    items.value = next.slice(-3)

    nextTick(() => {
      requestAnimationFrame(() => {
        const current = items.value.find(item => item.id === id)
        if (current) current.starting = false
      })
    })

    timers.set(id, window.setTimeout(() => toast.close(id), record.timeout))
    return id
  },
  close(id: number, swipe?: ToastSwipe) {
    const current = items.value.find(item => item.id === id)
    if (!current || current.ending) return
    current.ending = true
    if (swipe) current.swipe = swipe
    const timer = timers.get(id)
    if (timer) {
      window.clearTimeout(timer)
      timers.delete(id)
    }
    window.setTimeout(() => remove(id), 500)
  }
}

export function useToasts() {
  return items
}
