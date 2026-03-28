// Gallery filtering and lightbox logic
const filters = document.getElementById('filters');
const filterBtns = document.querySelectorAll('.filter-btn');
const galleryGrid = document.getElementById('galleryGrid');
const thumbs = Array.from(document.querySelectorAll('.thumb'));

filters.addEventListener('click', (e) => {
    const btn = e.target.closest('.filter-btn');
    if (!btn) return;
    filterBtns.forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    const filter = btn.dataset.filter;
    thumbs.forEach(t => {
    if (filter === 'all') t.style.display = '';
    else if (t.dataset.type && t.dataset.type.split(' ').includes(filter)) t.style.display = '';
    else t.style.display = 'none';
    });
});

// Lightbox
const lightbox = document.getElementById('lightbox');
const lbMedia = document.getElementById('lbMedia');
const lbTitle = document.getElementById('lbTitle');
const lbMeta = document.getElementById('lbMeta');
const lbExternal = document.getElementById('lbExternal');
const lbClose = document.getElementById('lbClose');
const prevBtn = document.getElementById('prevBtn');
const nextBtn = document.getElementById('nextBtn');

let visibleItems = thumbs.slice();
let currentIndex = 0;

function refreshVisible() {
    visibleItems = thumbs.filter(t => t.style.display !== 'none');
}

function openLightbox(index) {
    refreshVisible();
    currentIndex = index;
    showItem(visibleItems[currentIndex]);
    lightbox.classList.add('visible');
    lightbox.setAttribute('aria-hidden','false');
    document.body.style.overflow = 'hidden';
}

function closeLightbox() {
    lightbox.classList.remove('visible');
    lightbox.setAttribute('aria-hidden','true');
    lbMedia.innerHTML = '';
    document.body.style.overflow = '';
}

function showItem(item) {
    if (!item) return;
    lbMedia.innerHTML = ''; // clear
    const title = item.dataset.title || '';
    lbTitle.textContent = title;
    lbMeta.textContent = item.dataset.type ? item.dataset.type.toUpperCase() : '';

    if (item.dataset.video) {
    const iframe = document.createElement('iframe');
    iframe.src = `https://www.youtube.com/embed/${item.dataset.video}?autoplay=1&rel=0`;
    iframe.allow = 'accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture';
    iframe.style.width = '100%';
    iframe.style.height = '80vh';
    iframe.setAttribute('allowfullscreen','');
    lbMedia.appendChild(iframe);
    lbExternal.href = `https://youtu.be/${item.dataset.video}`;
    lbExternal.textContent = 'Open on YouTube';
    } else {
    const img = document.createElement('img');
    img.src = item.dataset.src || item.querySelector('img')?.src;
    img.alt = item.dataset.title || '';
    lbMedia.appendChild(img);
    lbExternal.href = img.src;
    lbExternal.textContent = 'Open Image';
    }
}

// Thumb click opens lightbox at that visible index
thumbs.forEach((t) => {
    t.addEventListener('click', () => {
    refreshVisible();
    const index = visibleItems.indexOf(t);
    openLightbox(index === -1 ? 0 : index);
    });
});

lbClose.addEventListener('click', closeLightbox);
lightbox.addEventListener('click', (e) => {
    if (e.target === lightbox) closeLightbox();
});

prevBtn.addEventListener('click', () => {
    refreshVisible();
    currentIndex = (currentIndex - 1 + visibleItems.length) % visibleItems.length;
    showItem(visibleItems[currentIndex]);
});

nextBtn.addEventListener('click', () => {
    refreshVisible();
    currentIndex = (currentIndex + 1) % visibleItems.length;
    showItem(visibleItems[currentIndex]);
});

// Keyboard navigation
document.addEventListener('keydown', (e) => {
    if (!lightbox.classList.contains('visible')) return;
    if (e.key === 'ArrowRight') nextBtn.click();
    if (e.key === 'ArrowLeft') prevBtn.click();
    if (e.key === 'Escape') closeLightbox();
});

// Ensure initial visibleItems reflect current filter state
refreshVisible();

const hamburger = document.getElementById("hamburger");
const navLinks = document.getElementById("navLinks");

hamburger.addEventListener("click", () => {
    navLinks.classList.toggle("active");
    }
)


let date = new Date().getFullYear();
dataSpan = document.querySelector("#date");
dataSpan.textContent = date;