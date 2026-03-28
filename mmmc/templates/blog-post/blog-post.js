// Reading time estimator and share buttons for blog-post.html


(function(){
    const content = document.getElementById('postContent');
    const readingEl = document.getElementById('readingTime');
    if (content && readingEl){
        const text = content.innerText || content.textContent || '';
        const words = text.trim().split(/\s+/).filter(Boolean).length;
        const minutes = Math.max(1, Math.round(words / 200));
        readingEl.textContent = minutes + ' min read';
    }

    // Basic share handlers
    document.querySelectorAll('.share-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            const type = btn.getAttribute('data-share');
            const url = encodeURIComponent(window.location.href);
            const title = encodeURIComponent(document.title);
            if (type === 'twitter' || type === 'x'){
                const shareUrl = `https://twitter.com/intent/tweet?url=${url}&text=${title}`;
                window.open(shareUrl,'_blank','noopener');
            } else if (type === 'copy'){
                navigator.clipboard && navigator.clipboard.writeText(window.location.href);
                btn.textContent = 'Copied';
                setTimeout(()=> btn.textContent='🔗',1200);
            }
        });
    });
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