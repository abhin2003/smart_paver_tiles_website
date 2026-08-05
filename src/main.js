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
    duration: 0.8,
    ease: 'power2.in',
    delay: 0.5
  })
  .to('#preloader', {
    yPercent: -100,
    duration: 1.2,
    ease: 'power4.inOut'
  })
}

// --- Smooth Scrolling (Lenis) ---
const lenis = new Lenis({
  lerp: 0.05, // Slower, heavier feel for luxury
  smoothWheel: true,
})

lenis.on('scroll', ScrollTrigger.update)

gsap.ticker.add((time) => {
  lenis.raf(time * 1000)
})
gsap.ticker.lagSmoothing(0)

// --- GSAP Animations ---
const initAnimations = () => {
  
  // Fade up text elements (Staggered)
  const revealElements = gsap.utils.toArray('.gs-reveal-up')
  
  revealElements.forEach(elem => {
    gsap.from(elem, {
      y: 60,
      opacity: 0,
      duration: 1.2,
      ease: 'power3.out',
      scrollTrigger: {
        trigger: elem,
        start: 'top 90%',
        toggleActions: 'play none none none'
      }
    })
  })

  // Parallax Backgrounds (Hero, Showcase, Footer)
  gsap.utils.toArray('.gs-parallax').forEach(bg => {
    const speed = bg.dataset.speed || 0.2;
    gsap.to(bg, {
      yPercent: speed * 100,
      ease: 'none',
      scrollTrigger: {
        trigger: bg.parentElement,
        start: 'top bottom',
        end: 'bottom top',
        scrub: true
      }
    })
  })
  
  // Editorial Visual Parallax (moves inside container)
  const editorialVisual = document.querySelector('.gs-parallax-img');
  if(editorialVisual) {
    gsap.to(editorialVisual, {
      yPercent: 20,
      ease: 'none',
      scrollTrigger: {
        trigger: '.editorial-visual-wrapper',
        start: 'top bottom',
        end: 'bottom top',
        scrub: true
      }
    })
  }
  
  // Horizontal Scroll Portfolio (Desktop Only) - REMOVED
  // User requested native side-scroll instead of scroll-hijacking
  
  // Navbar blur/bg on scroll
  const nav = document.getElementById('navbar')
  ScrollTrigger.create({
    start: 'top -50',
    onUpdate: (self) => {
      if(self.direction === 1) {
        gsap.to(nav, { yPercent: -100, duration: 0.4, ease: 'power2.out' })
      } else {
        gsap.to(nav, { yPercent: 0, duration: 0.4, ease: 'power2.out', backgroundColor: 'rgba(18, 17, 16, 0.9)', backdropFilter: 'blur(10px)' })
      }
      if(self.progress === 0) {
        gsap.to(nav, { backgroundColor: 'transparent', backdropFilter: 'none' })
      }
    }
  })
}

// --- Catalog Interactions ---
const initCatalogInteractions = () => {
  const catalogItems = document.querySelectorAll('.catalog-item');
  const previewImg = document.getElementById('catalog-preview-img');
  
  if(!catalogItems.length || !previewImg) return;
  
  catalogItems.forEach(item => {
    item.addEventListener('click', () => {
      // Remove active from all
      catalogItems.forEach(i => i.classList.remove('active'));
      // Add active to current
      item.classList.add('active');
      
      // Change image with fade effect
      const newImg = item.getAttribute('data-img');
      if (previewImg.src.indexOf(newImg) === -1) { // Only if different
        gsap.to(previewImg, {
          opacity: 0,
          duration: 0.3,
          onComplete: () => {
            previewImg.src = newImg;
            gsap.to(previewImg, {
              opacity: 1,
              duration: 0.3
            })
          }
        })
      }
    })
  })
}

// Start
document.addEventListener('DOMContentLoaded', () => {
  const yearEl = document.getElementById('year')
  if (yearEl) yearEl.textContent = new Date().getFullYear()
})

window.addEventListener('load', () => {
  init();
  initCatalogInteractions();
})
