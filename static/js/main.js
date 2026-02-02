/**
 * SiraWeb - Main JavaScript
 * Vanilla JS - No Dependencies
 * Performance-optimized with IntersectionObserver, requestAnimationFrame
 */

(function() {
  'use strict';

  // ============================================
  // Utility Functions
  // ============================================
  const $ = (selector, context = document) => context.querySelector(selector);
  const $$ = (selector, context = document) => Array.from(context.querySelectorAll(selector));

  // Check for reduced motion preference
  const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  // ============================================
  // Scroll Progress Bar
  // ============================================
  function initScrollProgress() {
    const progressBar = $('.scroll-progress-bar');
    if (!progressBar) return;

    const updateProgress = () => {
      const windowHeight = document.documentElement.scrollHeight - window.innerHeight;
      const scrolled = (window.scrollY / windowHeight) * 100;
      progressBar.style.width = `${Math.min(scrolled, 100)}%`;
      
      const progressElement = $('.scroll-progress');
      if (progressElement) {
        progressElement.setAttribute('aria-valuenow', Math.round(scrolled));
      }
    };

    // Use passive listener for better performance
    window.addEventListener('scroll', updateProgress, { passive: true });
    updateProgress();
  }

  // ============================================
  // Navbar Sticky & Scroll Effects
  // ============================================
  function initNavbar() {
    const navbar = $('#navbar');
    if (!navbar) return;

    let lastScroll = 0;
    const scrollThreshold = 20; // Réduit pour que la navbar devienne visible plus tôt

    const handleScroll = () => {
      const currentScroll = window.scrollY;
      
      if (currentScroll > scrollThreshold) {
        navbar.classList.add('scrolled');
      } else {
        navbar.classList.remove('scrolled');
      }
      
      lastScroll = currentScroll;
    };

    window.addEventListener('scroll', handleScroll, { passive: true });
    handleScroll();
  }

  // ============================================
  // Mobile Menu
  // ============================================
  function initMobileMenu() {
    const toggle = $('#mobile-menu-toggle');
    const menu = $('#mobile-menu');
    const backdrop = $('#mobile-menu-backdrop');
    if (!toggle || !menu) return;

    // Déplacer le menu mobile et le backdrop dans le body pour éviter les problèmes de z-index
    // Cela garantit qu'ils ne sont pas des enfants du hero
    if (menu && menu.parentElement !== document.body) {
      document.body.appendChild(menu);
    }
    if (backdrop && backdrop.parentElement !== document.body) {
      document.body.appendChild(backdrop);
    }

    const toggleMenu = () => {
      const isExpanded = toggle.getAttribute('aria-expanded') === 'true';
      const newState = !isExpanded;
      
      toggle.setAttribute('aria-expanded', newState);
      menu.setAttribute('aria-hidden', !newState);
      
      if (backdrop) {
        backdrop.setAttribute('aria-hidden', !newState);
        backdrop.classList.toggle('active', newState);
      }
      
      // Prevent body scroll when menu is open
      if (newState) {
        document.body.style.overflow = 'hidden';
        // Prevent scroll on iOS
        document.body.style.position = 'fixed';
        document.body.style.width = '100%';
      } else {
        document.body.style.overflow = '';
        document.body.style.position = '';
        document.body.style.width = '';
      }
    };

    toggle.addEventListener('click', (e) => {
      e.stopPropagation();
      toggleMenu();
    });

    // Close menu when clicking backdrop
    if (backdrop) {
      backdrop.addEventListener('click', () => {
        if (menu.getAttribute('aria-hidden') === 'false') {
          toggleMenu();
        }
      });
    }

    // Close menu when clicking outside (on mobile)
    document.addEventListener('click', (e) => {
      if (!menu.contains(e.target) && !toggle.contains(e.target) && menu.getAttribute('aria-hidden') === 'false') {
        toggleMenu();
      }
    });

    // Close menu on escape key
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape' && menu.getAttribute('aria-hidden') === 'false') {
        toggleMenu();
      }
    });

    // Close button handler
    const closeBtn = $('#mobile-menu-close');
    if (closeBtn) {
      closeBtn.addEventListener('click', (e) => {
        e.stopPropagation();
        if (menu.getAttribute('aria-hidden') === 'false') {
          toggleMenu();
        }
      });
    }

    // Mobile submenu toggles
    const submenuToggles = $$('.mobile-nav-toggle');
    submenuToggles.forEach(toggleBtn => {
      toggleBtn.addEventListener('click', (e) => {
        e.preventDefault();
        e.stopPropagation();
        const targetId = toggleBtn.getAttribute('data-target');
        const submenu = $(`#${targetId}`);
        if (submenu) {
          const isActive = submenu.classList.contains('active');
          
          // Close other submenus if needed (optional - can allow multiple open)
          // submenuToggles.forEach(other => {
          //   if (other !== toggleBtn) {
          //     const otherId = other.getAttribute('data-target');
          //     const otherSubmenu = $(`#${otherId}`);
          //     if (otherSubmenu) {
          //       otherSubmenu.classList.remove('active');
          //       other.classList.remove('active');
          //     }
          //   }
          // });
          
          submenu.classList.toggle('active', !isActive);
          toggleBtn.classList.toggle('active', !isActive);
        }
      });
    });

    // Close menu on regular link click (not submenu toggles)
    const mobileLinks = $$('.mobile-nav-link:not(.mobile-nav-toggle), .mobile-submenu-link');
    mobileLinks.forEach(link => {
      link.addEventListener('click', () => {
        if (menu.getAttribute('aria-hidden') === 'false') {
          toggleMenu();
        }
      });
    });
  }

  // ============================================
  // Smooth Anchor Scrolling
  // ============================================
  function initSmoothScroll() {
    if (prefersReducedMotion) return;

    const anchorLinks = $$('a[href^="#"]');
    
    anchorLinks.forEach(link => {
      link.addEventListener('click', (e) => {
        const href = link.getAttribute('href');
        if (href === '#' || href === '#main-content') return;
        
        const target = $(href);
        if (target) {
          e.preventDefault();
          const offset = 80; // Navbar height
          const targetPosition = target.getBoundingClientRect().top + window.pageYOffset - offset;
          
          window.scrollTo({
            top: targetPosition,
            behavior: 'smooth'
          });
        }
      });
    });
  }

  // ============================================
  // Scroll Reveal Animations
  // ============================================
  function initScrollReveal() {
    if (prefersReducedMotion) {
      // Reveal all elements immediately if reduced motion
      const revealElements = $$('.reveal-fade-up');
      revealElements.forEach(el => el.classList.add('revealed'));
      return;
    }

    const revealElements = $$('.reveal-fade-up');
    if (revealElements.length === 0) return;

    const observerOptions = {
      threshold: 0.1,
      rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          const delay = entry.target.dataset.delay || 0;
          setTimeout(() => {
            entry.target.classList.add('revealed');
          }, delay * 1000);
          observer.unobserve(entry.target);
        }
      });
    }, observerOptions);

    revealElements.forEach(el => observer.observe(el));
  }

  // ============================================
  // FAQ Accordion
  // ============================================
  function initFAQ() {
    const faqItems = $$('.faq-item');
    if (faqItems.length === 0) return;

    faqItems.forEach(item => {
      const question = item.querySelector('.faq-question');
      if (!question) return;

      question.addEventListener('click', () => {
        const isActive = item.classList.contains('active');
        
        // Close all items
        faqItems.forEach(otherItem => {
          otherItem.classList.remove('active');
          const otherQuestion = otherItem.querySelector('.faq-question');
          if (otherQuestion) {
            otherQuestion.setAttribute('aria-expanded', 'false');
          }
        });
        
        // Open clicked item if it wasn't active
        if (!isActive) {
          item.classList.add('active');
          question.setAttribute('aria-expanded', 'true');
        } else {
          question.setAttribute('aria-expanded', 'false');
        }
      });
    });
  }

  // ============================================
  // Animated Counter (Stats)
  // ============================================
  function initAnimatedCounter() {
    const statNumbers = $$('.stat-number');
    if (statNumbers.length === 0) return;

    const animateCounter = (element) => {
      const target = parseInt(element.getAttribute('data-target')) || 0;
      const duration = 2000; // 2 seconds
      const increment = target / (duration / 16); // 60fps
      let current = 0;

      const updateCounter = () => {
        current += increment;
        if (current < target) {
          element.textContent = Math.floor(current);
          requestAnimationFrame(updateCounter);
        } else {
          element.textContent = target;
        }
      };

      updateCounter();
    };

    const statsObserver = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          const statNumber = entry.target.querySelector('.stat-number');
          if (statNumber && !statNumber.classList.contains('animated')) {
            statNumber.classList.add('animated');
            animateCounter(statNumber);
          }
          statsObserver.unobserve(entry.target);
        }
      });
    }, { threshold: 0.5 });

    statNumbers.forEach(stat => {
      const statItem = stat.closest('.stat-item');
      if (statItem) {
        statsObserver.observe(statItem);
      }
    });
  }

  // ============================================
  // Hero Background Slider
  // ============================================
  function initHeroSlider() {
    if (prefersReducedMotion) return;

    const slides = $$('.hero-slide');
    if (slides.length <= 1) return;

    let currentSlide = 0;
    const slideInterval = 5000; // 5 seconds

    const showSlide = (index) => {
      slides.forEach((slide, i) => {
        slide.classList.toggle('active', i === index);
      });
    };

    const nextSlide = () => {
      currentSlide = (currentSlide + 1) % slides.length;
      showSlide(currentSlide);
    };

    // Start slider
    if (slides.length > 1) {
      setInterval(nextSlide, slideInterval);
    }
  }

  // ============================================
  // Parallax Effect (Light)
  // ============================================
  function initParallax() {
    if (prefersReducedMotion) return;

    const parallaxElements = $$('.shape');
    if (parallaxElements.length === 0) return;

    const handleScroll = () => {
      const scrolled = window.pageYOffset;
      const rate = scrolled * 0.5;

      parallaxElements.forEach((element, index) => {
        const speed = 0.3 + (index * 0.1);
        const yPos = -(rate * speed);
        element.style.transform = `translate3d(0, ${yPos}px, 0)`;
      });
    };

    window.addEventListener('scroll', handleScroll, { passive: true });
  }

  // ============================================
  // Magnetic Button Effect (Desktop only)
  // ============================================
  function initMagneticButtons() {
    if (prefersReducedMotion || window.innerWidth < 768) return;

    const magneticButtons = $$('.magnetic');
    if (magneticButtons.length === 0) return;

    magneticButtons.forEach(button => {
      button.addEventListener('mousemove', (e) => {
        const rect = button.getBoundingClientRect();
        const x = e.clientX - rect.left - rect.width / 2;
        const y = e.clientY - rect.top - rect.height / 2;
        
        const moveX = x * 0.15;
        const moveY = y * 0.15;

        button.style.transform = `translate(${moveX}px, ${moveY}px)`;
      });

      button.addEventListener('mouseleave', () => {
        button.style.transform = 'translate(0, 0)';
      });
    });
  }

  // ============================================
  // Testimonials Slider
  // ============================================
  function initTestimonialsSlider() {
    const slider = $('#testimonials-slider');
    if (!slider) return;

    const track = $('.testimonials-track', slider);
    const prevBtn = $('.slider-prev', slider);
    const nextBtn = $('.slider-next', slider);
    
    if (!track || !prevBtn || !nextBtn) return;

    const cards = $$('.testimonial-card', track);
    if (cards.length <= 1) {
      // Hide controls if only one card
      prevBtn.style.display = 'none';
      nextBtn.style.display = 'none';
      return;
    }

    let currentIndex = 0;
    const cardWidth = cards[0].offsetWidth + parseInt(getComputedStyle(track).gap);

    const scrollToCard = (index) => {
      const maxIndex = cards.length - 1;
      currentIndex = Math.max(0, Math.min(index, maxIndex));
      
      track.scrollTo({
        left: currentIndex * cardWidth,
        behavior: 'smooth'
      });
    };

    prevBtn.addEventListener('click', () => scrollToCard(currentIndex - 1));
    nextBtn.addEventListener('click', () => scrollToCard(currentIndex + 1));

    // Auto-scroll on track scroll (for touch devices)
    let scrollTimeout;
    track.addEventListener('scroll', () => {
      clearTimeout(scrollTimeout);
      scrollTimeout = setTimeout(() => {
        currentIndex = Math.round(track.scrollLeft / cardWidth);
      }, 100);
    }, { passive: true });
  }

  // ============================================
  // Portfolio Slider
  // ============================================
  function initPortfolioSlider() {
    const slider = $('#portfolio-slider');
    if (!slider) return;

    const track = $('.portfolio-showcase-track', slider);
    const prevBtn = $('.portfolio-slider-prev', slider);
    const nextBtn = $('.portfolio-slider-next', slider);
    
    if (!track || !prevBtn || !nextBtn) return;

    const items = $$('.portfolio-showcase-item', track);
    if (items.length <= 1) {
      // Hide controls if only one item
      prevBtn.style.display = 'none';
      nextBtn.style.display = 'none';
      return;
    }

    let currentIndex = 0;
    
    const getCardWidth = () => {
      const gap = parseInt(getComputedStyle(track).gap) || 0;
      return items[0].offsetWidth + gap;
    };

    const scrollToCard = (index) => {
      const maxIndex = items.length - 1;
      currentIndex = Math.max(0, Math.min(index, maxIndex));
      
      const cardWidth = getCardWidth();
      track.scrollTo({
        left: currentIndex * cardWidth,
        behavior: 'smooth'
      });
    };

    prevBtn.addEventListener('click', () => scrollToCard(currentIndex - 1));
    nextBtn.addEventListener('click', () => scrollToCard(currentIndex + 1));

    // Auto-update index on track scroll (for touch devices)
    let scrollTimeout;
    track.addEventListener('scroll', () => {
      clearTimeout(scrollTimeout);
      scrollTimeout = setTimeout(() => {
        const cardWidth = getCardWidth();
        currentIndex = Math.round(track.scrollLeft / cardWidth);
      }, 100);
    }, { passive: true });

    // Handle window resize
    let resizeTimeout;
    window.addEventListener('resize', () => {
      clearTimeout(resizeTimeout);
      resizeTimeout = setTimeout(() => {
        const cardWidth = getCardWidth();
        track.scrollTo({
          left: currentIndex * cardWidth,
          behavior: 'smooth'
        });
      }, 250);
    });
  }

  // ============================================
  // Card Tilt Effect (Desktop only)
  // ============================================
  function initCardTilt() {
    if (prefersReducedMotion || window.innerWidth < 1024) return;

    const cards = $$('.service-card');
    if (cards.length === 0) return;

    cards.forEach(card => {
      card.addEventListener('mousemove', (e) => {
        const rect = card.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top;

        const centerX = rect.width / 2;
        const centerY = rect.height / 2;

        const rotateX = (y - centerY) / 10;
        const rotateY = (centerX - x) / 10;

        card.style.transform = `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) translateY(-8px)`;
      });

      card.addEventListener('mouseleave', () => {
        card.style.transform = '';
      });
    });
  }

  // ============================================
  // Form Validation & Enhancement
  // ============================================
  function initForms() {
    const forms = $$('form');
    
    forms.forEach(form => {
      form.addEventListener('submit', (e) => {
        const inputs = $$('input[required], textarea[required]', form);
        let isValid = true;

        inputs.forEach(input => {
          if (!input.value.trim()) {
            isValid = false;
            input.classList.add('error');
          } else {
            input.classList.remove('error');
          }
        });

        if (!isValid) {
          e.preventDefault();
        }
      });

      // Real-time validation
      const inputs = $$('input, textarea', form);
      inputs.forEach(input => {
        input.addEventListener('blur', () => {
          if (input.hasAttribute('required') && !input.value.trim()) {
            input.classList.add('error');
          } else {
            input.classList.remove('error');
          }
        });
      });
    });
  }

  // ============================================
  // Message Dismissal
  // ============================================
  function initMessages() {
    const messageCloses = $$('.message-close');
    
    messageCloses.forEach(closeBtn => {
      closeBtn.addEventListener('click', () => {
        const message = closeBtn.closest('.message');
        if (message) {
          message.style.animation = 'slideOutRight 0.3s ease';
          setTimeout(() => message.remove(), 300);
        }
      });
    });

    // Auto-dismiss after 5 seconds
    const messages = $$('.message');
    messages.forEach(message => {
      setTimeout(() => {
        if (message.parentElement) {
          message.style.animation = 'slideOutRight 0.3s ease';
          setTimeout(() => message.remove(), 300);
        }
      }, 5000);
    });
  }

  // ============================================
  // Lazy Loading Images (Native with fallback)
  // ============================================
  function initLazyLoading() {
    const images = $$('img[loading="lazy"]');
    
    if ('loading' in HTMLImageElement.prototype) {
      // Native lazy loading supported
      return;
    }

    // Fallback for browsers without native lazy loading
    const imageObserver = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          const img = entry.target;
          if (img.dataset.src) {
            img.src = img.dataset.src;
            img.removeAttribute('data-src');
          }
          imageObserver.unobserve(img);
        }
      });
    });

    images.forEach(img => {
      if (img.dataset.src) {
        imageObserver.observe(img);
      }
    });
  }

  // ============================================
  // Performance: Debounce function
  // ============================================
  function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
      const later = () => {
        clearTimeout(timeout);
        func(...args);
      };
      clearTimeout(timeout);
      timeout = setTimeout(later, wait);
    };
  }

  // ============================================
  // Quote Modal
  // ============================================
  function initQuoteModal() {
    const openBtn = $('#open-quote-modal');
    const openBtnMobile = $('#open-quote-modal-mobile');
    const modal = $('#quote-modal');
    const closeBtn = $('#quote-modal-close');
    const backdrop = $('#quote-modal-backdrop');
    const mobileMenu = $('#mobile-menu');
    const mobileMenuToggle = $('#mobile-menu-toggle');
    
    if (!modal) return;

    const openModal = () => {
      // Fermer le menu mobile si ouvert
      if (mobileMenu && mobileMenu.getAttribute('aria-hidden') === 'false') {
        if (mobileMenuToggle) {
          mobileMenuToggle.setAttribute('aria-expanded', 'false');
        }
        mobileMenu.setAttribute('aria-hidden', 'true');
        const mobileBackdrop = $('#mobile-menu-backdrop');
        if (mobileBackdrop) {
          mobileBackdrop.setAttribute('aria-hidden', 'true');
          mobileBackdrop.classList.remove('active');
        }
        document.body.style.overflow = '';
        document.body.style.position = '';
        document.body.style.width = '';
      }
      
      modal.setAttribute('aria-hidden', 'false');
      document.body.style.overflow = 'hidden';
      // Focus sur le premier champ du formulaire
      const firstInput = modal.querySelector('input, textarea, select');
      if (firstInput) {
        setTimeout(() => firstInput.focus(), 100);
      }
    };

    const closeModal = () => {
      modal.setAttribute('aria-hidden', 'true');
      document.body.style.overflow = '';
    };

    // Ouvrir le modal depuis le bouton navbar
    if (openBtn) {
      openBtn.addEventListener('click', (e) => {
        e.preventDefault();
        openModal();
      });
    }

    // Ouvrir le modal depuis le bouton menu mobile
    if (openBtnMobile) {
      openBtnMobile.addEventListener('click', (e) => {
        e.preventDefault();
        openModal();
      });
    }

    // Ouvrir le modal depuis la page services
    const openBtnServices = $('#open-quote-modal-services');
    if (openBtnServices) {
      openBtnServices.addEventListener('click', (e) => {
        e.preventDefault();
        openModal();
      });
    }

    // Ouvrir le modal depuis la page détail service (hero et CTA)
    const openBtnServiceDetail = $('#open-quote-modal-service-detail');
    const openBtnServiceCTA = $('#open-quote-modal-service-cta');
    if (openBtnServiceDetail) {
      openBtnServiceDetail.addEventListener('click', (e) => {
        e.preventDefault();
        openModal();
      });
    }
    if (openBtnServiceCTA) {
      openBtnServiceCTA.addEventListener('click', (e) => {
        e.preventDefault();
        openModal();
      });
    }

    // Ouvrir le modal depuis la page about
    const openBtnAbout = $('#open-quote-modal-about');
    if (openBtnAbout) {
      openBtnAbout.addEventListener('click', (e) => {
        e.preventDefault();
        openModal();
      });
    }

    // Fermer le modal
    if (closeBtn) {
      closeBtn.addEventListener('click', (e) => {
        e.preventDefault();
        closeModal();
      });
    }

    // Fermer avec le backdrop
    if (backdrop) {
      backdrop.addEventListener('click', () => {
        closeModal();
      });
    }

    // Fermer avec Escape
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape' && modal.getAttribute('aria-hidden') === 'false') {
        closeModal();
      }
    });

    // Gérer la soumission du formulaire dans le modal
    const form = $('#quote-form');
    if (form) {
      form.addEventListener('submit', (e) => {
        // Le formulaire sera soumis normalement
        // Après soumission réussie, on peut fermer le modal
        // (géré par la redirection Django)
      });
    }
  }

  // ============================================
  // Technologies Carousel with Manual Scroll
  // ============================================
  function initTechnologiesCarousel() {
    const wrapper = $('.technologies-carousel-wrapper');
    const track = $('.technologies-track');
    if (!wrapper || !track) return;

    let isDragging = false;
    let isPaused = false;
    let startX = 0;
    let currentX = 0;
    let currentPosition = 0;
    let animationStartTime = 0;
    let animationId = null;
    let resumeTimeout = null;

    // Get current transform value from computed style
    const getCurrentTransform = () => {
      const style = window.getComputedStyle(track);
      const matrix = style.transform || style.webkitTransform;
      if (matrix === 'none') return 0;
      const values = matrix.split('(')[1].split(')')[0].split(',');
      return parseFloat(values[4]) || 0;
    };

    // Set transform position
    const setPosition = (position) => {
      track.style.transform = `translateX(${position}px)`;
      currentPosition = position;
    };

    // Normalize position to stay within bounds (infinite loop)
    const normalizePosition = (pos) => {
      const trackWidth = track.scrollWidth / 2;
      if (pos > 0) {
        return pos - trackWidth;
      } else if (pos < -trackWidth) {
        return pos + trackWidth;
      }
      return pos;
    };

    // Update animation position
    const updateAnimation = () => {
      if (!isDragging && !isPaused) {
        const now = Date.now();
        const elapsed = (now - animationStartTime) / 1000;
        const totalDuration = 30;
        const progress = (elapsed % totalDuration) / totalDuration;
        const trackWidth = track.scrollWidth / 2;
        const newPosition = normalizePosition(-progress * trackWidth);
        
        setPosition(newPosition);
        animationId = requestAnimationFrame(updateAnimation);
      }
    };

    // Start animation
    const startAnimation = () => {
      if (isDragging || isPaused) return;
      animationStartTime = Date.now() - (Math.abs(currentPosition) / (track.scrollWidth / 2)) * 30000;
      if (animationId) cancelAnimationFrame(animationId);
      updateAnimation();
    };

    // Stop animation
    const stopAnimation = () => {
      if (animationId) {
        cancelAnimationFrame(animationId);
        animationId = null;
      }
    };

    // Resume animation after delay
    const resumeAnimation = (delay = 2000) => {
      if (resumeTimeout) clearTimeout(resumeTimeout);
      resumeTimeout = setTimeout(() => {
        if (!isDragging) {
          isPaused = false;
          wrapper.classList.remove('paused');
          startAnimation();
        }
      }, delay);
    };

    // Mouse events
    const handleMouseDown = (e) => {
      isDragging = true;
      isPaused = true;
      wrapper.classList.add('paused');
      startX = e.pageX;
      currentX = startX;
      currentPosition = getCurrentTransform();
      track.classList.add('dragging');
      stopAnimation();
    };

    const handleMouseMove = (e) => {
      if (!isDragging) return;
      e.preventDefault();
      
      currentX = e.pageX;
      const deltaX = currentX - startX;
      const newPosition = normalizePosition(currentPosition + deltaX);
      
      setPosition(newPosition);
    };

    const handleMouseUp = () => {
      if (!isDragging) return;
      isDragging = false;
      track.classList.remove('dragging');
      currentPosition = getCurrentTransform();
      
      // Resume after delay
      resumeAnimation(2000);
    };

    // Touch events
    const handleTouchStart = (e) => {
      isDragging = true;
      isPaused = true;
      wrapper.classList.add('paused');
      startX = e.touches[0].pageX;
      currentX = startX;
      currentPosition = getCurrentTransform();
      track.classList.add('dragging');
      stopAnimation();
    };

    const handleTouchMove = (e) => {
      if (!isDragging) return;
      e.preventDefault();
      
      currentX = e.touches[0].pageX;
      const deltaX = currentX - startX;
      const newPosition = normalizePosition(currentPosition + deltaX);
      
      setPosition(newPosition);
    };

    const handleTouchEnd = () => {
      if (!isDragging) return;
      isDragging = false;
      track.classList.remove('dragging');
      currentPosition = getCurrentTransform();
      
      // Resume after delay
      resumeAnimation(2000);
    };

    // Pause on hover
    wrapper.addEventListener('mouseenter', () => {
      if (!isDragging) {
        isPaused = true;
        wrapper.classList.add('paused');
        stopAnimation();
      }
    });

    wrapper.addEventListener('mouseleave', () => {
      if (!isDragging) {
        resumeAnimation(1000);
      }
    });

    // Mouse drag events
    track.addEventListener('mousedown', handleMouseDown);
    document.addEventListener('mousemove', handleMouseMove);
    document.addEventListener('mouseup', handleMouseUp);

    // Touch drag events
    track.addEventListener('touchstart', handleTouchStart, { passive: false });
    track.addEventListener('touchmove', handleTouchMove, { passive: false });
    track.addEventListener('touchend', handleTouchEnd);

    // Wheel scroll
    wrapper.addEventListener('wheel', (e) => {
      e.preventDefault();
      isPaused = true;
      wrapper.classList.add('paused');
      stopAnimation();
      
      const delta = e.deltaY;
      const currentPos = getCurrentTransform();
      const newPosition = normalizePosition(currentPos - delta * 0.5);
      
      setPosition(newPosition);
      
      // Resume after delay
      resumeAnimation(2000);
    }, { passive: false });

    // Initialize animation
    currentPosition = 0;
    setPosition(0);
    startAnimation();
  }

  // ============================================
  // Initialize everything when DOM is ready
  // ============================================
  // ============================================
  // FAQ Pagination Scroll
  // ============================================
  function initFAQPaginationScroll() {
    // Si on arrive sur la page avec un paramètre ?page= et #faq dans l'URL
    const urlParams = new URLSearchParams(window.location.search);
    const pageParam = urlParams.get('page');
    const hash = window.location.hash;
    
    if (pageParam && hash === '#faq') {
      // Attendre que le DOM soit chargé
      setTimeout(() => {
        const faqSection = $('#faq');
        if (faqSection) {
          const offset = 80; // Navbar height
          const targetPosition = faqSection.getBoundingClientRect().top + window.pageYOffset - offset;
          
          window.scrollTo({
            top: targetPosition,
            behavior: 'smooth'
          });
        }
      }, 100);
    }
  }

  function init() {
    // Core functionality
    initScrollProgress();
    initNavbar();
    initMobileMenu();
    initSmoothScroll();
    initScrollReveal();
    initForms();
    initMessages();
    initLazyLoading();
    initQuoteModal();
    initAnimatedCounter();
    initFAQ();
    initFAQPaginationScroll();

    // Animations (only if motion is not reduced)
    if (!prefersReducedMotion) {
      initHeroSlider();
      initParallax();
      initMagneticButtons();
      initCardTilt();
    }

    // Sliders
    initTestimonialsSlider();
    initPortfolioSlider();
    initTechnologiesCarousel();

    // Handle resize for responsive features
    let resizeTimeout;
    window.addEventListener('resize', () => {
      clearTimeout(resizeTimeout);
      resizeTimeout = setTimeout(() => {
        // Reinitialize features that depend on window size
        if (window.innerWidth >= 768 && !prefersReducedMotion) {
          initMagneticButtons();
        }
        if (window.innerWidth >= 1024 && !prefersReducedMotion) {
          initCardTilt();
        }
      }, 250);
    }, { passive: true });
  }

  // Wait for DOM to be ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }

  // Add slideOutRight animation to CSS dynamically if needed
  const style = document.createElement('style');
  style.textContent = `
    @keyframes slideOutRight {
      from {
        transform: translateX(0);
        opacity: 1;
      }
      to {
        transform: translateX(100%);
        opacity: 0;
      }
    }
  `;
  document.head.appendChild(style);

})();
