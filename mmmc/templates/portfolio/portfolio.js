// Filter and modal script for portfolio
(function(){
    const grid = document.getElementById('portfolioGrid');
    const cards = Array.from(grid.querySelectorAll('.sample-card'));
    const filterBtns = Array.from(document.querySelectorAll('.filter-btn'));
    const searchInput = document.getElementById('portfolioSearch');

    function applyFilter(tag, q){
        const query = (q||'').trim().toLowerCase();
        cards.forEach(card => {
            const tags = card.getAttribute('data-tags') || '';
            const title = (card.getAttribute('data-title')||'').toLowerCase();
            const desc = (card.querySelector('.sample-desc')||{textContent:''}).textContent.toLowerCase();
            const tagMatch = tag === 'all' || tags.split(',').map(t=>t.trim()).includes(tag);
            const textMatch = !query || title.includes(query) || desc.includes(query);
            card.style.display = (tagMatch && textMatch) ? '' : 'none';
        });
    }

    filterBtns.forEach(btn => btn.addEventListener('click', () => {
        filterBtns.forEach(b=>b.classList.remove('active'));
        btn.classList.add('active');
        const tag = btn.getAttribute('data-filter');
        applyFilter(tag, searchInput.value);
    }));

    searchInput.addEventListener('input', (e) => {
        const active = document.querySelector('.filter-btn.active').getAttribute('data-filter');
        applyFilter(active, e.target.value);
    });

    // Modal preview
    const overlay = document.getElementById('overlay');
    const modalTitle = document.getElementById('modalTitle');
    const modalBody = document.getElementById('modalBody');
    const modalClose = document.getElementById('modalClose');

    document.querySelectorAll('.view-btn[data-detail]').forEach(btn => {
        btn.addEventListener('click', (e) => {
            e.preventDefault();
            const raw = btn.getAttribute('data-detail');
            const parts = raw.split('|');
            modalTitle.textContent = parts[0] || '';
            modalBody.textContent = parts[1] || '';
            overlay.style.display = 'flex';
        });
    });

    modalClose.addEventListener('click', () => overlay.style.display = 'none');
    overlay.addEventListener('click', (e) => { if (e.target === overlay) overlay.style.display = 'none'; });

    // initialize
    applyFilter('all','');
})();