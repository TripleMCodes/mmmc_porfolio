const now = new Date();
const oneMonthAgo = new Date(
now.getFullYear(),
now.getMonth() - 1,
now.getDate()
).toISOString().split('T')[0];
lastUpdatedDate = document.querySelector('.last-updated')
lastUpdatedDate.innerText = oneMonthAgo;

const hamburger = document.getElementById("hamburger");
const navLinks = document.getElementById("navLinks");

hamburger.addEventListener("click", () => {
    navLinks.classList.toggle("active");
    })