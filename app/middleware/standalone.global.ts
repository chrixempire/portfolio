import { interactionBySlug } from '~/data/interactions'

const LOCK = 'interaction-standalone'
const standalonePath = /^\/interaction\/04\/[^/]+$/

export default defineNuxtRouteMiddleware((to) => {
  const previous = to.path.match(/^\/interaction\/(0|1)\/([^/]+)$/)
  if (previous && interactionBySlug(previous[2])) {
    const mode = previous[1] === '0' ? '2032' : '04'
    return navigateTo(`/interaction/${mode}/${previous[2]}`, { redirectCode: 302, replace: true })
  }

  const legacy = to.path.match(/^\/interaction\/([^/]+)$/)
  if (legacy && interactionBySlug(legacy[1])) {
    return navigateTo(`/interaction/04/${legacy[1]}`, { redirectCode: 302, replace: true })
  }

  if (import.meta.server) return

  if (standalonePath.test(to.path)) {
    sessionStorage.setItem(LOCK, to.path)
    return
  }

  const locked = sessionStorage.getItem(LOCK)
  if (!locked || locked === to.path) return
  return navigateTo(locked, { replace: true })
})
