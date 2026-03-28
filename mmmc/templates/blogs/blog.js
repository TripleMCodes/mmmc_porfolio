 // Client-side search/filter for blog archive
(function(){
    const input = document.getElementById('postSearch');
    const clearBtn = document.getElementById('clearSearch');
    const posts = Array.from(document.querySelectorAll('#postsGrid .post-card'));

    function filter(q){
        const t = q.trim().toLowerCase();
        posts.forEach(p => {
            const title = p.getAttribute('data-title').toLowerCase();
            const excerpt = p.getAttribute('data-excerpt').toLowerCase();
            const match = !t || title.includes(t) || excerpt.includes(t);
            p.style.display = match ? '' : 'none';
        });
    }

    input.addEventListener('input', (e) => filter(e.target.value));
    clearBtn.addEventListener('click', () => { input.value=''; filter(''); input.focus(); });

    // initialize
    filter('');
})();

const hamburger = document.getElementById("hamburger");
const navLinks = document.getElementById("navLinks");

hamburger.addEventListener("click", () => {
    navLinks.classList.toggle("active");
    }
)

let date = new Date().getFullYear();
dataSpan = document.querySelector("#date");
dataSpan.textContent = date;