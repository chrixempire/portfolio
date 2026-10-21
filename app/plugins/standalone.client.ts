import { interactionBySlug } from '~/data/interactions'

const LOCK = 'interaction-standalone'
const standalonePath = /^\/interaction\/04\/[^/]+$/

const normalize = (path: string) => {
  const short = path.match(/^\/04\/([^/]+)$/)
  if (short && interactionBySlug(short[1])) return `/interaction/04/${short[1]}`
  return path
}

const lockedTarget = (path: string) => {
  const normalized = normalize(path)
  if (normalized !== path) return normalized

  if (standalonePath.test(path)) {
    sessionStorage.setItem(LOCK, path)
    return
  }

  const locked = sessionStorage.getItem(LOCK)
  if (!locked || locked === path) return
  return locked
}

export default defineNuxtPlugin(() => {
  const router = useRouter()

  router.beforeEach((to) => {
    const next = lockedTarget(to.path)
    if (next) return next
  })

  const next = lockedTarget(router.currentRoute.value.path)
  if (next) navigateTo(next, { replace: true })
})
