// Event page script: add any interactivity here
document.addEventListener('DOMContentLoaded', () => {
    // Log upcoming events to console (for debugging)
    const upcomingCards = document.querySelectorAll('.event-card');
    console.log(`Found ${upcomingCards.length} upcoming events`);
});

const hamburger = document.getElementById("hamburger");
const navLinks = document.getElementById("navLinks");

hamburger.addEventListener("click", () => {
    navLinks.classList.toggle("active");
    }
)

let date = new Date().getFullYear();
dataSpan = document.querySelector("#date");
dataSpan.textContent = date;