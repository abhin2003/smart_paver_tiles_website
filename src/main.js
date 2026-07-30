import './style.css'
import gsap from 'gsap'
import { ScrollTrigger } from 'gsap/ScrollTrigger'
import Lenis from 'lenis'

gsap.registerPlugin(ScrollTrigger)

// --- Preloader & Initialization ---
const init = () => {
  const tl = gsap.timeline({
    onComplete: () => {
      document.getElementById('preloader').style.display = 'none'
      initAnimations()
    }
  })

  tl.to('.preloader-logo', {
    opacity: 0,
    y: -20,
    duration: 0.5,
    ease: 'power2.in',
    delay: 0.2
  })
  .to('#preloader', {
    yPercent: -100,
    duration: 0.8,
    ease: 'power3.inOut'
  })
}

// --- Smooth Scrolling (Lenis) ---
const lenis = new Lenis({
  lerp: 0.08,
  smoothWheel: true,
})

lenis.on('scroll', ScrollTrigger.update)

gsap.ticker.add((time) => {
  lenis.raf(time * 1000)
})

gsap.ticker.lagSmoothing(0)


// --- GSAP Animations ---
const initAnimations = () => {
  // Simple fade up for elements with .gs-reveal
  gsap.utils.toArray('.gs-reveal').forEach(elem => {
    gsap.from(elem, {
      y: 50,
      opacity: 0,
      duration: 1,
      ease: 'power3.out',
      scrollTrigger: {
        trigger: elem,
        start: 'top 85%',
        toggleActions: 'play none none none'
      }
    })
  })
  
  // Parallax effect on image placeholders (optional, adds premium feel)
  gsap.utils.toArray('.image-placeholder').forEach(img => {
    gsap.to(img, {
      yPercent: 10,
      ease: 'none',
      scrollTrigger: {
        trigger: img,
        start: 'top bottom',
        end: 'bottom top',
        scrub: true
      }
    })
  })
}

// Start
document.addEventListener('DOMContentLoaded', () => {
  const yearEl = document.getElementById('year')
  if (yearEl) yearEl.textContent = new Date().getFullYear()
})

window.addEventListener('load', init)
