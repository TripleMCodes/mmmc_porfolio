// 1. Generate floating particles (Works perfectly)
function createParticles() {
    const particlesContainer = document.getElementById('particles');
    if (!particlesContainer) return; // Safety check
    const particleCount = 30;

    for (let i = 0; i < particleCount; i++) {
        const particle = document.createElement('div');
        particle.className = 'particle';
        const size = Math.random() * 5 + 2;
        particle.style.width = `${size}px`;
        particle.style.height = `${size}px`;
        particle.style.left = `${Math.random() * 100}%`;
        particle.style.animationDelay = `${Math.random() * 20}s`;
        particle.style.animationDuration = `${Math.random() * 10 + 15}s`;
        particlesContainer.appendChild(particle);
    }
}

// 2. REFACTORED: Smooth scroll for internal IDs only
// We only preventDefault if the link is just a hash (e.g., href="#section")
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        const href = this.getAttribute('href');
        if (href !== "#" && href.startsWith("#")) {
            e.preventDefault();
            const target = document.querySelector(href);
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        }
    });
});

// 3. Intersection Observer (Works great for the new cards)
const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -100px 0px'
};

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.style.opacity = '1';
            entry.target.style.transform = 'translateY(0)';
        }
    });
}, observerOptions);

document.querySelectorAll('.music-card, .post-card, .about-section').forEach(el => {
    el.style.opacity = '0';
    el.style.transform = 'translateY(30px)';
    el.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
    observer.observe(el);
});

// // 4. REFACTORED: Glitch effect for profile name
// // We grab the text dynamically to support whichever alter ego is loaded
// const profileName = document.querySelector('.profile-name');
// if (profileName) {
//     const originalText = profileName.textContent;
//     const glitchChars = "!<>-_\\/[]{}—=+*^?#________";

//     profileName.addEventListener('mouseenter', () => {
//         let glitchIterations = 0;
//         const maxGlitches = 15;

//         const glitchInterval = setInterval(() => {
//             if (glitchIterations < maxGlitches) {
//                 profileName.textContent = originalText
//                     .split("")
//                     .map(char => (Math.random() > 0.7 ? glitchChars[Math.floor(Math.random() * glitchChars.length)] : char))
//                     .join("");
//                 glitchIterations++;
//             } else {
//                 profileName.textContent = originalText;
//                 clearInterval(glitchInterval);
//             }
//         }, 50);
//     });
// }

// 5. Navigation and Footer
const hamburger = document.getElementById("hamburger");
const navLinks = document.getElementById("navLinks");

if (hamburger && navLinks) {
    hamburger.addEventListener("click", () => {
        navLinks.classList.toggle("active");
    });
}

const dataSpan = document.querySelector("#date");
if (dataSpan) {
    dataSpan.textContent = new Date().getFullYear();
}

// Initialize
createParticles();

const particlesContainer = document.getElementById("particles");

function createOrb() {
  if (!particlesContainer) return;

  const orb = document.createElement("span");
  orb.classList.add("orb");

  const size = 80 + Math.random() * 180;
  orb.style.width = `${size}px`;
  orb.style.height = `${size}px`;

  orb.style.left = `${Math.random() * 100}%`;
  orb.style.top = `${Math.random() * 100}%`;

  const duration = 12 + Math.random() * 14;
  orb.style.animationDuration = `${duration}s`;

  particlesContainer.appendChild(orb);

  setTimeout(() => {
    orb.remove();
  }, duration * 1000);
}

for (let i = 0; i < 6; i++) {
  setTimeout(createOrb, i * 1200);
}

setInterval(createOrb, 4000);