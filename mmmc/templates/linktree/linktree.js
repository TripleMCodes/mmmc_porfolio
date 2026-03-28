// Copy email button behavior (guard DOM lookups)
(function(){
  const btn = document.getElementById('copyEmail');
  const copied = document.getElementById('copied');
  const emailFallback = 'vickey@gmail.com';

  if (btn) {
    btn.addEventListener('click', async () => {
      // try to extract an email from the button text if present
      const emailText = (btn.dataset && btn.dataset.email) || btn.textContent.replace(/\s+/g, ' ').trim() || emailFallback;
      try {
        if (!navigator.clipboard) throw new Error('clipboard API not available');
        await navigator.clipboard.writeText(emailText);
        if (copied) {
          copied.style.display = 'inline-block';
          setTimeout(() => copied.style.display = 'none', 1600);
        }
      } catch (err) {
        // fallback: open mailto
        window.location.href = 'mailto:' + encodeURIComponent(emailText || emailFallback);
      }
    });
  }

  // optional: log clicks to console for local testing (only if links exist)
  const clickableEls = document.querySelectorAll('.lt-links a, .lt-links button');
  if (clickableEls && clickableEls.length) {
    clickableEls.forEach(el => el.addEventListener('click', () => {
      try { console.log('Link click:', (el.href || el.textContent).toString()); } catch(e){}
    }));
  }
})();

// Hamburger navigation toggle: use class selector and guard nulls
const hamburger = document.getElementById('hamburger');
const navLinks = document.querySelector('.nav-links');

if (hamburger && navLinks) {
  hamburger.addEventListener('click', () => {
    navLinks.classList.toggle('active');
  });
}



// linktree.js — vanilla carousel (buttons + dots + swipe + keyboard)
(() => {
  const root = document.querySelector("[data-carousel]");
  if (!root) return;

  const viewport = root.querySelector("[data-carousel-viewport]");
  const track = root.querySelector("[data-carousel-track]");
  const btnPrev = root.querySelector("[data-carousel-prev]");
  const btnNext = root.querySelector("[data-carousel-next]");
  const dotsWrap = root.querySelector("[data-carousel-dots]");

  if (!viewport || !track) return;

  const slides = Array.from(track.children).filter(el => el.classList.contains("streaming-card"));
  if (slides.length === 0) return;

  let index = 0;
  let isTransitioning = false;

  const clamp = (n, min, max) => Math.max(min, Math.min(max, n));

  const getGap = () => {
    const style = window.getComputedStyle(track);
    const gap = style.columnGap || style.gap || "0";
    return parseFloat(gap);
  };

  const getSlideWidth = () => {
    if (!slides[0]) return 0;
    return slides[0].offsetWidth || 260;
  };

  const getScrollLeft = (i) => {
    const gap = getGap();
    const slideWidth = getSlideWidth();
    return i * (slideWidth + gap);
  };

  const getCurrentIndex = () => {
    const gap = getGap();
    const slideWidth = getSlideWidth();
    const step = slideWidth + gap;
    if (step === 0) return 0;
    return Math.round(viewport.scrollLeft / step);
  };

  const updateUI = () => {
    btnPrev && (btnPrev.disabled = index === 0);
    btnNext && (btnNext.disabled = index === slides.length - 1);

    if (dotsWrap) {
      const dots = dotsWrap.querySelectorAll("button");
      dots.forEach((d, di) => {
        d.setAttribute("aria-current", di === index ? "true" : "false");
      });
    }
  };

  const goTo = (i, smooth = true) => {
    index = clamp(i, 0, slides.length - 1);
    const targetScroll = getScrollLeft(index);
    
    viewport.scrollTo({
      left: targetScroll,
      behavior: smooth ? "smooth" : "auto",
    });
    
    updateUI();
  };

  // Build dots
  if (dotsWrap) {
    dotsWrap.innerHTML = "";
    slides.forEach((_, i) => {
      const dot = document.createElement("button");
      dot.type = "button";
      dot.className = "dot";
      dot.setAttribute("aria-label", `Go to slide ${i + 1}`);
      dot.addEventListener("click", () => goTo(i));
      dotsWrap.appendChild(dot);
    });
  }

  // Buttons
  btnPrev?.addEventListener("click", () => goTo(index - 1));
  btnNext?.addEventListener("click", () => goTo(index + 1));

  // Keyboard (focus the carousel to use arrows)
  root.tabIndex = 0;
  root.addEventListener("keydown", (e) => {
    if (e.key === "ArrowLeft") goTo(index - 1);
    if (e.key === "ArrowRight") goTo(index + 1);
  });

  // Keep dots in sync when user scrolls manually
  let scrollTimer = null;
  viewport.addEventListener("scroll", () => {
    clearTimeout(scrollTimer);
    scrollTimer = setTimeout(() => {
      index = getCurrentIndex();
      updateUI();
    }, 100);
  });

  // Touch swipe snap (nice on mobile)
  let startX = 0;
  let startLeft = 0;
  let touching = false;

  viewport.addEventListener("touchstart", (e) => {
    touching = true;
    startX = e.touches[0].clientX;
    startLeft = viewport.scrollLeft;
  }, { passive: true });

  viewport.addEventListener("touchmove", (e) => {
    if (!touching) return;
    const dx = startX - e.touches[0].clientX;
    viewport.scrollLeft = startLeft + dx;
  }, { passive: true });

  viewport.addEventListener("touchend", () => {
    touching = false;
    index = getCurrentIndex();
    goTo(index, false); // snap to nearest
  });

  window.addEventListener("resize", () => {
    index = getCurrentIndex();
    goTo(index, false);
  });

  // Init
  goTo(0, false);
})();
