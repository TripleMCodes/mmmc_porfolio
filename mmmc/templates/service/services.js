// Small pricing toggle: switches visible prices between monthly and yearly values
(function(){
    const toggle = document.getElementById('billingToggle');
    const priceEls = document.querySelectorAll('.plan-price');
    function setPrices(yearly){
        priceEls.forEach(el => {
            el.textContent = yearly ? el.getAttribute('data-year') : el.getAttribute('data-month');
        });
    }
    toggle.addEventListener('change', () => setPrices(toggle.checked));
    // initialize to monthly (unchecked)
    setPrices(toggle.checked);
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