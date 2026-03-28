const form = document.getElementById("portfolioForm");

form.addEventListener("submit", async (e) => {
    e.preventDefault();

    const title = document.getElementById("title").value;
    const description = document.getElementById("description").value;
    const project_url = document.getElementById("url").value;

    try {
        const response = await fetch("/api/portfolio", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                title,
                description,
                project_url
            })
        });

        const data = await response.json();

        if (response.ok) {

            // addSampleToList(data.sample);
            loadPortfolio(currentPage);

            form.reset();
        } else {
            alert(data.error);
        }

    } catch (error) {
        console.error(error);
    }
});


// -------------------
// Add item to UI
// -------------------
// function addSampleToList(sample) {

//     const list = document.getElementById("portfolioList");

//     const li = document.createElement("li");

//     li.id = `sample-${sample.id}`;

//     li.innerHTML = `
//         <strong>${sample.title}</strong>
//         <p>${sample.description}</p>
//         <a href="${sample.project_url}">Project url</a>
//         <button onclick="deleteSample(${sample.id})">
//             Delete
//         </button>
//     `;

//     list.appendChild(li);
// }


// -------------------
// Delete Portfolio Item
// -------------------
async function deleteSample(id) {

    if (!confirm("Delete this portfolio item?")) return;

    try {

        const response = await fetch(`/api/portfolio/${id}`, {
            method: "DELETE"
        });

        const data = await response.json();

        if (response.ok) {
            // document.getElementById(`sample-${id}`).remove();
            loadPortfolio(currentPage);
        } else {
            alert(data.error);
        }

    } catch (error) {
        console.error(error);
    }
}


let currentPage = 1;

async function loadPortfolio(page = 1) {

    try {

        const response = await fetch(`/api/portfolio?page=${page}`);
        const data = await response.json();

        const list = document.getElementById("portfolioList");
        list.innerHTML = "";

        data.portfolio.forEach(sample => {

            const div = document.createElement("div");

            div.classList.add("portfolio-item");
            div.id = `sample-${sample.id}`;

            div.innerHTML = `
                <div class="portfolio-title">
                    ${sample.title}
                </div>

                <div class="portfolio-description">
                    ${sample.description}
                </div>

                <a href="${sample.project_url}" 
                   target="_blank"
                   class="portfolio-url">
                    View Project
                </a>

                <div class="portfolio-actions">
                    <button 
                        class="delete-btn"
                        onclick="deleteSample(${sample.id})">
                        Delete
                    </button>
                </div>
            `;

            list.appendChild(div);
        });

        updatePagination(data);

    } catch (error) {
        console.error(error);
    }
}


function updatePagination(data) {

    currentPage = data.current_page;

    document.getElementById("pageInfo").innerText =
        `Page ${data.current_page} of ${data.total_pages}`;

    document.getElementById("prevBtn").disabled = !data.has_prev;
    document.getElementById("nextBtn").disabled = !data.has_next;
}


document.getElementById("prevBtn").addEventListener("click", () => {
    loadPortfolio(currentPage - 1);
});

document.getElementById("nextBtn").addEventListener("click", () => {
    loadPortfolio(currentPage + 1);
});



document.addEventListener("DOMContentLoaded", () => {
    loadPortfolio(1);
});