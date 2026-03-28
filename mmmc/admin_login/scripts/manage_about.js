function notify(message) {
    const msgBox = document.getElementById('msgBox');
    msgBox.textContent = message;
    msgBox.classList.add('on');
    setTimeout(() => msgBox.classList.remove('on'), 5000);
}

document.addEventListener("DOMContentLoaded", () => {
  const heroIdEl = document.getElementById("hero-id");
  const titleEl = document.getElementById("hero-title");
  const briefEl = document.getElementById("hero-brief");
  const saveBtn = document.getElementById("btn-save-hero");
  const statusEl = document.getElementById("hero-status");

  function setStatus(msg, isError = false) {
    statusEl.textContent = msg;
    statusEl.style.opacity = msg ? "1" : "0";
    statusEl.style.color = isError ? "crimson" : "";
  }

  async function saveHero() {
    const hero_title = titleEl.value.trim();
    const hero_brief = briefEl.value.trim();

    if (!hero_title || !hero_brief) {
      setStatus("Please fill in both title and brief.", true);
      return;
    }

    saveBtn.disabled = true;
    saveBtn.textContent = "Saving...";
    setStatus("Saving...");

    try {
      const res = await fetch("/hero", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ "hero-title":hero_title, "hero-brief":hero_brief }),
      });

      const data = await res.json().catch(() => ({}));

      if (!res.ok) {
        setStatus(data.message || "Failed to save hero.", true);
        return;
      }

      // Update hidden id so UI knows it’s now saved
      if (data.hero && data.hero.id) {
        heroIdEl.value = data.hero.id;
      }

      setStatus(data.message || "Saved.");
    } catch (err) {
      console.error(err);
      setStatus("Network error while saving hero.", true);
    } finally {
      saveBtn.disabled = false;
      saveBtn.textContent = "Save Hero";
    }
  }

  saveBtn.addEventListener("click", saveHero);
});


document.addEventListener("DOMContentLoaded", () => {
  const editor = document.getElementById("foundation-editor");
  if (!editor) return;

  const idEl = document.getElementById("foundation-id");
  const titleEl = document.getElementById("foundation-title");
  const parasWrap = document.getElementById("foundation-paragraphs");
  const addBtn = document.getElementById("btn-add-foundation-para");
  const saveBtn = document.getElementById("btn-save-foundation");
  const statusEl = document.getElementById("foundation-status");

  function setStatus(msg, isError = false) {
    statusEl.textContent = msg;
    statusEl.style.color = isError ? "crimson" : "";
  }

  saveBtn.addEventListener("click", async () => {
    // const title = titleEl.value.trim();

    const paragraphsArr = Array.from(parasWrap.querySelectorAll(".foundation-para"))
      .map(t => t.value.trim())
      .filter(Boolean);

    console.log(paragraphsArr)

    // if (!title) {
    //   setStatus("Please provide a title.", true);
    //   return;
    // }
    if (paragraphsArr.length === 0) {
      setStatus("Add at least one paragraph.", true);
      return;
    }
    // console.log(paragraphsArr)

    saveBtn.disabled = true;
    saveBtn.textContent = "Saving...";
    setStatus("Saving...");

    try {
      const res = await fetch("/foundation", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({paragraphsArr }),
      });

      const data = await res.json().catch(() => ({}));

      if (!res.ok) {
        setStatus(data.message || "Failed to save foundation.", true);
        return;
      }

      if (data.foundation && data.foundation.id) {
        idEl.value = data.foundation.id;
      }

      setStatus(data.message || "Saved.");
    } catch (err) {
      console.error(err);
      setStatus("Network error while saving foundation.", true);
    } finally {
      saveBtn.disabled = false;
      saveBtn.textContent = "Save Foundation";
    }
  });
});




function saveSection(sectionName) {
    const title = document.getElementById(sectionName + '-title');
    let content = {};

    if (sectionName === 'hero') {
        content = { brief: document.getElementById('hero-brief').value };
    } else if (sectionName === 'foundation') {
        const paras = document.querySelectorAll('#foundation-paragraphs .foundation-para');
        content = { paragraphs: Array.from(paras).map(p => p.value) };
        console.log(content)
    } else if (sectionName === 'craft') {
        const paras = document.querySelectorAll('#craft-paragraphs .craft-para');
        content = { paragraphs: Array.from(paras).map(p => p.value) };
    } else if (sectionName === 'journey') {
        const items = document.querySelectorAll('#journey-items .journey-item');
        content = Array.from(items).map(item => ({
            year: item.querySelector('.year').value,
            description: item.querySelector('.desc').value
        }));
    } else if (sectionName === 'expertise') {
        const cards = document.querySelectorAll('#expertise-cards .expertise-card');
        content = { cards: Array.from(cards).map(card => ({
            icon: card.querySelector('.icon').value,
            title: card.querySelector('.title').value,
            description: card.querySelector('.desc').value
        })) };
    } else if (sectionName === 'testimonials') {
        const slides = document.querySelectorAll('#testimonials-slides .testimonial-slide');
        content = { slides: Array.from(slides).map(slide => ({
            quote: slide.querySelector('.quote').value,
            author: slide.querySelector('.author').value
        })) };
    } else if (sectionName === 'cta') {
        content = {
            text: document.getElementById('cta-text').value,
            button: document.getElementById('cta-button').value
        };
    }

    fetch('/update about section', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ section_name: sectionName, title: title, content: JSON.stringify(content) })
    })
    .then(response => response.json())
    .then(data => {
        notify(data.message);
        alert('Added successfully.')
    })
      .catch(err => {
        alert('Error saving section')
        notify('Error saving section')
      }
      );
    
}

function addParagraph(section) {
    const container = document.getElementById(section + '-paragraphs');
    const textarea = document.createElement('textarea');
    textarea.className = section + '-para';
    textarea.placeholder = 'Paragraph';
    container.appendChild(textarea);
}

function addJourneyItem() {
    const container = document.getElementById('journey-items');
    const div = document.createElement('div');
    div.className = 'journey-item';
    div.innerHTML = `
        <input type="text" class="year" placeholder="Year">
        <textarea class="desc" placeholder="Description"></textarea>
        <button class="save-btn" onclick="removeItem(this)">Remove</button>
    `;
    container.appendChild(div);
}


function addTestimonialSlide() {
    const container = document.getElementById('testimonials-slides');
    const div = document.createElement('div');
    div.className = 'testimonial-slide';
    div.innerHTML = `
        <textarea class="quote" placeholder="Quote"></textarea>
        <input type="text" class="author" placeholder="Author">
        <button class="save-btn" onclick="removeItem(this)">Remove</button>
    `;
    container.appendChild(div);
}

function removeItem(button) {
    button.parentElement.remove();
}


const hamburger = document.getElementById("hamburger");
const navLinks = document.getElementById("navLinks");

hamburger.addEventListener("click", () => {
    navLinks.classList.toggle("active");
    }
)


document.addEventListener("DOMContentLoaded", () => {
  const wrap = document.getElementById("expertise-cards");
  const addBtn = document.getElementById("btn-add-expertise");

  // --- small helper
  const escapeHtml = (str = "") =>
    String(str)
      .replaceAll("&", "&amp;")
      .replaceAll("<", "&lt;")
      .replaceAll(">", "&gt;")
      .replaceAll('"', "&quot;")
      .replaceAll("'", "&#039;");

  // Create a card element (saved or draft)
  function createCardEl({ exp_id = null, icon = "", expertise = "", desc = "", isDraft = false } = {}) {
    const el = document.createElement("article");
    el.className = "expertise-card";
    if (exp_id) el.dataset.expId = exp_id;
    if (isDraft) el.dataset.draft = "1";

    el.innerHTML = `
      <div class="field-row">
        <label class="field">
          <span class="field-label">Icon</span>
          <input type="text" class="icon" value="${escapeHtml(icon)}" placeholder="✨" maxlength="8">
        </label>

        <label class="field">
          <span class="field-label">Title</span>
          <input type="text" class="title" value="${escapeHtml(expertise)}" placeholder="e.g. Mixing & Mastering">
        </label>
      </div>

      <label class="field">
        <span class="field-label">Description</span>
        <textarea class="desc" placeholder="Describe this expertise...">${escapeHtml(desc)}</textarea>
      </label>

      <div class="card-actions">
        ${
          isDraft
            ? `<button type="button" class="save-btn js-create-expertise">Save</button>
               <button type="button" class="save-btn ghost js-cancel-draft">Cancel</button>`
            : `<button type="button" class="save-btn danger js-delete-expertise">Delete</button>`
        }
      </div>
    `;
    return el;
  }

  // Add a draft card (client-only)
  addBtn.addEventListener("click", () => {
    const draft = createCardEl({ isDraft: true });
    wrap.prepend(draft);
    draft.querySelector(".icon")?.focus();
  });

  // Event delegation for Save/Delete/Cancel
  wrap.addEventListener("click", async (e) => {
    const card = e.target.closest(".expertise-card");
    if (!card) return;

    // Cancel draft
    if (e.target.closest(".js-cancel-draft")) {
      card.remove();
      return;
    }

    // Create (POST) new expertise
    if (e.target.closest(".js-create-expertise")) {
      const btn = e.target.closest(".js-create-expertise");
      const icon = card.querySelector(".icon").value.trim();
      const expertise = card.querySelector(".title").value.trim();
      const desc = card.querySelector(".desc").value.trim();

      if (!icon || !expertise || !desc) {
        alert("Please fill icon, title, and description.");
        return;
      }

      btn.disabled = true;
      btn.textContent = "Saving...";

      try {
        const res = await fetch("/add-expertise", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ icon, expertise, desc }),
        });

        const data = await res.json().catch(() => ({}));

        if (!res.ok) {
          btn.disabled = false;
          btn.textContent = "Save";
          alert(data.message || "Failed to create expertise.");
          return;
        }

        // Need exp_id returned by backend
        if (!data.exp_id) {
          btn.disabled = false;
          btn.textContent = "Save";
          alert("Created, but server did not return exp_id. Please update /add-expertise to return it.");
          return;
        }

        // Convert draft to saved UI
        delete card.dataset.draft;
        card.dataset.expId = data.exp_id;

        // Replace actions: Save/Cancel -> Delete
        card.querySelector(".card-actions").innerHTML =
          `<button type="button" class="save-btn danger js-delete-expertise">Delete</button>`;

      } catch (err) {
        console.error(err);
        btn.disabled = false;
        btn.textContent = "Save";
        alert("Network error while creating expertise.");
      }

      return;
    }

    // Delete (DELETE) existing expertise
    if (e.target.closest(".js-delete-expertise")) {
      const expId = card.dataset.expId;

      // If no id, it's not saved yet: just remove
      if (!expId) {
        card.remove();
        return;
      }

      const ok = confirm("Delete this expertise card permanently?");
      if (!ok) return;

      const btn = e.target.closest(".js-delete-expertise");
      btn.disabled = true;
      btn.textContent = "Deleting...";

      try {
        const res = await fetch(`/delete-expertise/${encodeURIComponent(expId)}`, {
          method: "DELETE",
          headers: { "Content-Type": "application/json" },
        });

        const data = await res.json().catch(() => ({}));

        if (!res.ok) {
          btn.disabled = false;
          btn.textContent = "Delete";
          alert(data.message || "Failed to delete expertise.");
          return;
        }
        card.remove();

      } catch (err) {
        console.error(err);
        btn.disabled = false;
        btn.textContent = "Delete";
        alert("Network error while deleting expertise.");
      }
    }
  });
});


document.addEventListener("DOMContentLoaded", () => {
  const wrap = document.getElementById("testimonials-slides");
  const addBtn = document.getElementById("btn-add-testimonial");

  const escapeHtml = (str = "") =>
    String(str)
      .replaceAll("&", "&amp;")
      .replaceAll("<", "&lt;")
      .replaceAll(">", "&gt;")
      .replaceAll('"', "&quot;")
      .replaceAll("'", "&#039;");

  function createTestimonialCardEl({
    t_id = null,
    testimonial = "",
    artist_name = "",
    artist_social = "",
    isDraft = false,
  } = {}) {
    const el = document.createElement("article");
    el.className = "testimonial-card";
    if (t_id) el.dataset.tId = t_id;
    if (isDraft) el.dataset.draft = "1";

    el.innerHTML = `
      <label class="field">
        <span class="field-label">Testimonial</span>
        <textarea class="testimonial" placeholder="Quote...">${escapeHtml(testimonial)}</textarea>
      </label>

      <div class="field-row">
        <label class="field">
          <span class="field-label">Artist name</span>
          <input type="text" class="artist-name" value="${escapeHtml(artist_name)}" placeholder="Artist A">
        </label>

        <label class="field">
          <span class="field-label">Social link</span>
          <input type="text" class="artist-social" value="${escapeHtml(artist_social)}" placeholder="https://instagram.com/...">
        </label>
      </div>

      <div class="card-actions">
        ${
          isDraft
            ? `<button type="button" class="save-btn js-create-testimonial">Save</button>
               <button type="button" class="save-btn ghost js-cancel-testimonial">Cancel</button>`
            : `<button type="button" class="save-btn danger js-delete-testimonial">Delete</button>`
        }
      </div>
    `;
    return el;
  }

  // Add draft testimonial card (client-side)
  addBtn.addEventListener("click", () => {
    const draft = createTestimonialCardEl({ isDraft: true });
    wrap.prepend(draft);
    draft.querySelector(".testimonial")?.focus();
  });

  // Event delegation for Save/Cancel/Delete
  wrap.addEventListener("click", async (e) => {
    const card = e.target.closest(".testimonial-card");
    if (!card) return;

    // Cancel draft
    if (e.target.closest(".js-cancel-testimonial")) {
      card.remove();
      return;
    }

    // Create testimonial (POST)
    if (e.target.closest(".js-create-testimonial")) {
      const btn = e.target.closest(".js-create-testimonial");

      const testimonial = card.querySelector(".testimonial").value.trim();
      const artist_name = card.querySelector(".artist-name").value.trim();
      const artist_social_link = card.querySelector(".artist-social").value.trim();

      if (!testimonial || !artist_name || !artist_social_link) {
        alert("Please fill testimonial, artist name, and social link.");
        return;
      }

      btn.disabled = true;
      btn.textContent = "Saving...";

      try {
        const res = await fetch("/add-testimonial", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ testimonial, artist_name, artist_social_link }),
        });

        const data = await res.json().catch(() => ({}));

        if (!res.ok) {
          btn.disabled = false;
          btn.textContent = "Save";
          alert(data.message || "Failed to add testimonial.");
          return;
        }

        // Backend MUST return t_id for immediate UI to support delete without refresh
        if (!data.t_id) {
          btn.disabled = false;
          btn.textContent = "Save";
          alert("Saved, but server didn’t return t_id. Update /add-testimonial to return it.");
          return;
        }

        // Convert draft -> saved
        delete card.dataset.draft;
        card.dataset.tId = data.t_id;

        // Replace actions with Delete
        card.querySelector(".card-actions").innerHTML =
          `<button type="button" class="save-btn danger js-delete-testimonial">Delete</button>`;

      } catch (err) {
        console.error(err);
        btn.disabled = false;
        btn.textContent = "Save";
        alert("Network error while adding testimonial.");
      }

      return;
    }

    // Delete testimonial (DELETE)
    if (e.target.closest(".js-delete-testimonial")) {
      const tId = card.dataset.tId;

      // If no id (unsaved draft), just remove
      if (!tId) {
        card.remove();
        return;
      }

      const ok = confirm("Delete this testimonial permanently?");
      if (!ok) return;

      const btn = e.target.closest(".js-delete-testimonial");
      btn.disabled = true;
      btn.textContent = "Deleting...";

      try {
        const res = await fetch(`/delete-testimonial/${encodeURIComponent(tId)}`, {
          method: "DELETE",
          headers: { "Content-Type": "application/json" },
        });

        const data = await res.json().catch(() => ({}));

        if (!res.ok) {
          btn.disabled = false;
          btn.textContent = "Delete";
          alert(data.message || "Failed to delete testimonial.");
          return;
        }

        // Remove from UI ✅
        card.remove();

      } catch (err) {
        console.error(err);
        btn.disabled = false;
        btn.textContent = "Delete";
        alert("Network error while deleting testimonial.");
      }
    }
  });
});

// journey section
document.addEventListener("DOMContentLoaded", () => {
  const wrap = document.getElementById("journey-items");
  const addBtn = document.getElementById("btn-add-journey");
  const statusEl = document.getElementById("journey-status");

  function setStatus(msg, isError = false) {
    statusEl.textContent = msg;
    statusEl.style.color = isError ? "crimson" : "";
  }

  function makeDraftJourneyRow(year = "", desc = "") {
    const div = document.createElement("div");
    div.className = "journey-item";
    div.dataset.draft = "1";
    div.innerHTML = `
      <input type="number" class="year" placeholder="Year" value="${year}">
      <textarea class="desc" placeholder="Description">${desc}</textarea>

      <div class="row-actions">
        <button type="button" class="save-btn js-create-journey">Save</button>
        <button type="button" class="save-btn ghost js-cancel-draft">Cancel</button>
      </div>
    `;
    return div;
  }

  addBtn?.addEventListener("click", () => {
    const row = makeDraftJourneyRow("", "");
    wrap.prepend(row);
    row.querySelector(".year")?.focus();
  });

  wrap.addEventListener("click", async (e) => {
    const row = e.target.closest(".journey-item");
    if (!row) return;

    // Cancel draft
    if (e.target.closest(".js-cancel-draft")) {
      row.remove();
      return;
    }

    // CREATE
    if (e.target.closest(".js-create-journey")) {
      const yearVal = row.querySelector(".year").value.trim();
      const descVal = row.querySelector(".desc").value.trim();

      const year = parseInt(yearVal, 10);
      if (!yearVal || Number.isNaN(year)) {
        setStatus("Year must be a number.", true);
        return;
      }
      if (!descVal) {
        setStatus("Description is required.", true);
        return;
      }

      const btn = e.target.closest(".js-create-journey");
      btn.disabled = true;
      btn.textContent = "Saving...";
      setStatus("Saving...");

      try {
        const res = await fetch("/journey", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ year, desc: descVal }),
        });

        const data = await res.json().catch(() => ({}));

        if (!res.ok) {
          setStatus(data.message || "Failed to create journey item.", true);
          btn.disabled = false;
          btn.textContent = "Save";
          return;
        }

        // Backend must return id
        if (!data.journey || !data.journey.id) {
          setStatus("Saved, but server didn't return id.", true);
          btn.disabled = false;
          btn.textContent = "Save";
          return;
        }

        // Convert draft -> saved row UI (Update/Delete)
        delete row.dataset.draft;
        row.dataset.journeyId = data.journey.id;

        row.querySelector(".row-actions").innerHTML = `
          <button type="button" class="save-btn js-update-journey">Update</button>
          <button type="button" class="save-btn danger js-delete-journey">Delete</button>
        `;

        setStatus("Journey item created");
      } catch (err) {
        console.error(err);
        setStatus("Network error creating journey item.", true);
      } finally {
        btn.disabled = false;
        btn.textContent = "Save";
      }
      return;
    }

    // UPDATE (PUT)
    if (e.target.closest(".js-update-journey")) {
      const id = row.dataset.journeyId;
      if (!id) return;

      const yearVal = row.querySelector(".year").value.trim();
      const descVal = row.querySelector(".desc").value.trim();

      const year = parseInt(yearVal, 10);
      if (!yearVal || Number.isNaN(year)) {
        setStatus("Year must be a number.", true);
        return;
      }
      if (!descVal) {
        setStatus("Description is required.", true);
        return;
      }

      const btn = e.target.closest(".js-update-journey");
      btn.disabled = true;
      btn.textContent = "Updating...";
      setStatus("Updating...");

      try {
        const res = await fetch(`/journey/${encodeURIComponent(id)}`, {
          method: "PUT",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ year, desc: descVal }),
        });

        const data = await res.json().catch(() => ({}));
        if (!res.ok) {
          setStatus(data.message || "Failed to update journey item.", true);
          return;
        }

        setStatus("Updated");
      } catch (err) {
        console.error(err);
        setStatus("Network error updating journey item.", true);
      } finally {
        btn.disabled = false;
        btn.textContent = "Update";
      }
      return;
    }

    // DELETE (DELETE)
    if (e.target.closest(".js-delete-journey")) {
      const id = row.dataset.journeyId;
      if (!id) {
        // unsaved draft
        row.remove();
        return;
      }

      const ok = confirm("Delete this timeline item permanently?");
      if (!ok) return;

      const btn = e.target.closest(".js-delete-journey");
      btn.disabled = true;
      btn.textContent = "Deleting...";
      setStatus("Deleting...");

      try {
        const res = await fetch(`/journey/${encodeURIComponent(id)}`, {
          method: "DELETE",
        });

        const data = await res.json().catch(() => ({}));
        if (!res.ok) {
          setStatus(data.message || "Failed to delete journey item.", true);
          btn.disabled = false;
          btn.textContent = "Delete";
          return;
        }

        row.remove();
        setStatus("Deleted");
      } catch (err) {
        console.error(err);
        setStatus("Network error deleting journey item.", true);
      }
    }
  });
});
