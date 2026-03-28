(function(){
    const form = document.getElementById('hireForm');

    form.addEventListener('submit', function(e){
        e.preventDefault();
        
        const pathParts = window.location.pathname.split('/');
        const artistSlug = pathParts[1]; 

        const name = document.getElementById('name').value.trim();
        const email = document.getElementById('email').value.trim();
        const message = document.getElementById('message').value.trim();
        const nda = document.getElementById('nda').checked;

        if (!name || !email || !message){
            alert('Please complete name, email, and project brief.');
            return;
        }

        const formData = new FormData();
        formData.append('name', name);
        formData.append('email', email);
        formData.append('message', message);
        if (nda) {
            formData.append('nda', 'on');
        }

        fetch(`/contact`, {
            method: 'POST',
            headers: {
                'X-Requested-With': 'XMLHttpRequest'
            },
            body: formData
        })
        .then(response => {
            if (!response.ok) throw new Error('Network response was not ok');
            return response.json();
        })
        .then(data => {
            if (data.success) {
                alert(data.message);
                form.reset();
            } else {
                alert(data.message || 'Error sending message.');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Error sending message. Please try again.');
        });
    });
})();

// Mobile menu and Date remain fine as they are UI-only
const hamburger = document.getElementById("hamburger");
const navLinks = document.getElementById("navLinks");

hamburger.addEventListener("click", () => {
    navLinks.classList.toggle("active");
});

document.querySelector("#date").textContent = new Date().getFullYear();