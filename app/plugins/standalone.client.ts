const LOCK = 'interaction-standalone'
const standalonePath = /^\/interaction\/04\/[^/]+$/

const lockedTarget = (path: string) => {
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
