export function debounce(fn, delay = 300) {
  let timeoutId = null

  return function (...args) {
    clearTimeout(timeoutId)

    timeoutId = setTimeout(() => {
      fn(...args)
    }, delay)
  }
}
