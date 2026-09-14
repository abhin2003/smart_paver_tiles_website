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

// --- Smooth Anchor Navigation ---
const initSmoothScrollNav = () => {
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
      const targetId = this.getAttribute('href');
      if (targetId && targetId !== '#') {
        const targetElement = document.querySelector(targetId);
        if (targetElement) {
          e.preventDefault();
          lenis.scrollTo(targetElement, { 
            offset: 0,
            duration: 1.2
          });
        }
      }
    });
  });
};

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
    gsap.fromTo(bg, 
      { yPercent: -speed * 50 },
      {
        yPercent: speed * 50,
        ease: 'none',
        scrollTrigger: {
          trigger: bg.parentElement,
          start: 'top bottom',
          end: 'bottom top',
          scrub: true
        }
      }
    )
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

// --- Catalog Interactions (Typographic Takeover) ---
const initCatalogInteractions = () => {
  const typoItems = document.querySelectorAll('.catalog-typo-item');
  const bgItems = document.querySelectorAll('.catalog-bg-item');
  
  if(!typoItems.length || !bgItems.length) return;
  
  typoItems.forEach(item => {
    item.addEventListener('click', () => {
      // Get target index
      const index = parseInt(item.getAttribute('data-index'));
      
      // Update typo active state (optional since CSS handles hover, but good for tracking)
      typoItems.forEach(i => i.classList.remove('active'));
      item.classList.add('active');
      
      // Update backgrounds
      bgItems.forEach((bg, i) => {
        if (i === index) {
          bg.classList.add('active');
        } else {
          bg.classList.remove('active');
        }
      });
    });
  });
}

// Start
document.addEventListener('DOMContentLoaded', () => {
  const yearEl = document.getElementById('year')
  if (yearEl) yearEl.textContent = new Date().getFullYear()
  
  initSmoothScrollNav();
})

window.addEventListener('load', () => {
  init();
  initCatalogInteractions();
})
