import Lenis from 'lenis'
import 'lenis/dist/lenis.css'

// Momentum scrolling for the whole site: each wheel tick or touch flick launches a glide
// that decelerates on an exponential ease-out, so input keeps coasting after it stops.
// Skipped when the user asks for reduced motion.
export const lenis = window.matchMedia('(prefers-reduced-motion: reduce)').matches
  ? null
  : new Lenis({
      autoRaf: true,
      allowNestedScroll: true,
      duration: 1.2,
      easing: (t) => Math.min(1, 1.001 - Math.pow(2, -10 * t)),
      wheelMultiplier: 1,
      // Touch flicks get the same coasting glide instead of the browser's native stop.
      syncTouch: true,
      touchInertiaExponent: 1.7,
    })

// Programmatic scrolls go through Lenis so they don't fight its animation.
export function scrollToTarget(target, options = {}) {
  if (lenis) return lenis.scrollTo(target, options)
  if (typeof target === 'number') window.scrollTo({ top: target, behavior: 'smooth' })
  else target?.scrollIntoView({ behavior: 'smooth' })
}

// Drop leftover momentum so a fling on one page doesn't keep scrolling the next one.
export function resetScrollMomentum() {
  if (!lenis) return
  lenis.stop()
  lenis.start()
}
