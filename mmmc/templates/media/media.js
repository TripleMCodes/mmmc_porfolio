// Media page filtering
const filterBtns = document.querySelectorAll('.filter-btn');
const musicCards = document.querySelectorAll('.music-card');

filterBtns.forEach(btn => {
    btn.addEventListener('click', () => {
        // Update active button
        filterBtns.forEach(b => b.classList.remove('active'));
        btn.classList.add('active');

        const filterValue = btn.dataset.filter;

        musicCards.forEach(card => {
            if (filterValue === 'all') {
                card.style.display = 'flex';
            } else if (card.dataset.type.includes(filterValue)) {
                card.style.display = 'flex';
            } else {
                card.style.display = 'none';
            }
        });
    });
});

// Initialize with all visible
musicCards.forEach(card => card.style.display = 'flex');

hamburger.addEventListener("click", () => {
    navLinks.classList.toggle("active");
    }
)

let date = new Date().getFullYear();
dataSpan = document.querySelector("#date");
dataSpan.textContent = date;