function notify(msg){ alert(msg); }

d = {
    "spotify": "https://spotify.com",
    "soundcloud": "https://on.soundcloud.com/vytY8liCK5auv86bYK",
    "youtubemusic": "https://www.youtube.com/@ConnorOdyssey", "applemusic": "https://applemusic.com/@vi",
    "audiomack": "https://audiomack.com/@vickykae",
    "bandcamp": "https://bandcamp.com/@vickykae",
    "amazon": "https://amazon.com/@vickykae",
    "itunes": "https://itunes.com/@vickykae",
    "gpm": "https://google.play.music.com/@vickykae", "instagram": "https://instagram.com/@vickykae",
    "thread": "https://thread.com/@vickykae",
    "tiktok": "https://tiktok.com/@vickykae",
    "facebook": "https://facebook.com/@vickykae",
    "x": "https://x.com/@vickykae"
}

function saveStreaming(){
    const payload = { streaming: {
        spotify: document.getElementById('spotify').value,
        soundcloud: document.getElementById('soundcloud').value,
        youtubemusic: document.getElementById('youtubemusic').value,
        youtube: document.getElementById('youtube').value,
        applemusic: document.getElementById('applemusic').value,
        audiomack: document.getElementById('audiomack').value,
        bandcamp: document.getElementById('bandcamp').value,
        amazon: document.getElementById('amazon').value,
        itunes: document.getElementById('itunes').value,
        gpm: document.getElementById('gpm').value,
        instagram: document.getElementById('instagram').value,
        thread: document.getElementById('thread').value,
        tiktok: document.getElementById('tiktok').value,
        facebook: document.getElementById('facebook').value,
        x: document.getElementById('x').value,
    }};
    fetch('/update streaming links', {method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(payload)})
    .then(r=>r.json()).then(j=>notify(j.message)).catch(()=>notify('Error'))
}

function savePlaylist(){
    const payload = { playlist: document.getElementById('playlist').value };
    fetch('/update featured playlist', {method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(payload)})
    .then(r=>r.json()).then(j=>notify(j.message)).catch(()=>notify('Error'))
}




function addEPSRow(){
    const container = document.getElementById('epsList');
    const div = document.createElement('div'); div.className='eps-item';
    div.innerHTML = `
        <input class="title" type="text" placeholder="Title">
        <input class="year small" type="text" placeholder="Year">
        <input class="stream small" type="text" placeholder="Stream URL">
        <input class="buy small" type="text" placeholder="Buy URL">
        <button class="save-btn" onclick="removeEPS(this)">Remove</button>
    `;
    container.appendChild(div);
}


function addSingle() {
    const container = document.querySelector('.s-list')
    const div = document.createElement('div');
    div.classList = 's-item'
    div.innerHTML = `
        <input class="title" type="text" placeholder="Title" value="">
        <input class="artist" type="text" placeholder="Artist" value="">
        <input class="album" type="text" placeholder="album" value="">
        <input class="link"  type="text" placeholder="link" value="">
        <input class="buy_link"  type="text" placeholder="Buy URL" value="">
        <button class="save-btn" onclick="removeSingle(this)">Remove</button>
        <button class="save-btn" onclick="saveSingle(this)">Save Single</button>
    `
    container.appendChild(div)
}



function addAlbumRow() {
    const list = document.getElementById('albumList');

    const div = document.createElement('div');
    div.className = 'album-item';

    div.innerHTML = `
        <input class="title" type="text" placeholder="Title">
        <input class="artist" type="text" placeholder="Artist">
        <input class="released_date small" type="date">
        <input class="link" type="text" placeholder="Album URL">
        <input class="buy-link" type="text" placeholder="Buy URL (optional)" value="">
        <button class="save-btn" onclick="removeAlbum(this)">Remove</button>
        <button class="save-btn" onclick="saveAlbum(this)">Save Album</button>
    `;

    list.appendChild(div);
}




async function saveAlbum(btn) {
    const row = btn.closest('.album-item');

    console.log(row.querySelector('.buy-link').value.trim())

    const data = {
        title: row.querySelector('.title').value.trim(),
        artist: row.querySelector('.artist').value.trim(),
        released_date: row.querySelector('.released_date').value,
        link: row.querySelector('.link').value.trim(),
        buy_link: row.querySelector('.buy-link').value.trim()
    };

    if (!data.title || !data.artist || !data.released_date || !data.link) {
        alert('All album fields are required');
        return;
    }

    try {
        const res = await fetch('/add album', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });

        const result = await res.json();

        if (!res.ok) {
            throw new Error(result.message);
        }

        // btn.textContent = 'Saved ✓';
        // setTimeout(() => btn.textContent = 'Save Album', 1200);

        notify(result.message)

    } catch (err) {
        // console.error(err);
        alert('Failed to save album');
    }
}

async function removeAlbum(btn) {
    const row = btn.closest('.album-item');

    const data = {
        title: row.querySelector('.title').value.trim(),
        artist: row.querySelector('.artist').value.trim(),
        released_date: row.querySelector('.released_date').value
    };

    if (!data.title || !data.artist || !data.released_date) {
        btn.parentElement.remove()
        // alert('Cannot delete album with missing data');
        return;
    }

    if (!confirm('Delete this album permanently?')) return;

    try {
        const res = await fetch('/delete album', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });

        const result = await res.json();

        if (!res.ok) {
            throw new Error(result.message);
        }

        row.remove();

    } catch (err) {
        console.error(err);
        alert('Failed to delete album');
    }
}

async function removeSingle(btn) {
    const row = btn.closest('.s-item');

    const data = {
        title: row.querySelector('.title').value.trim(),
        artist: row.querySelector('.artist').value.trim(),
        album: row.querySelector('.album').value.trim()
    };

    if (!data.title || !data.artist || !data.album) {
        alert('Cannot delete single with missing data');
        return;
    }

    if (!confirm('Delete this single permanently?')) return;

    try {
        const res = await fetch('/delete single', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });

        const result = await res.json();

        if (!res.ok) {
            throw new Error(result.message);
        }

        row.remove();

    } catch (err) {
        console.error(err);
        alert('Failed to delete single');
    }
}


async function saveSingle(btn) {
    const row = btn.closest('.s-item');

    const data = {
        title: row.querySelector('.title').value.trim(),
        artist: row.querySelector('.artist').value.trim(),
        album: row.querySelector('.album').value.trim(),
        links: row.querySelector('.link').value.trim(),
        buy_link: row.querySelector('.buy_link').value.trim()
    };

    if (!data.title || !data.artist || !data.album || !data.links) {
        alert("All fields are required.");
        row.remove()
        return;
    }

    try {
        const res = await fetch('/add single', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });

        const result = await res.json();

        if (!res.ok) {
            throw new Error(result.message || 'Failed to save single');
        }

        // btn.textContent = 'Saved ✓';
        // setTimeout(() => btn.textContent = 'Save Single', 1200);
        notify(res.message || "Single saved");

    } catch (err) {
        console.error(err);
        alert('Error saving single');
    }
}

function removeEPS(btn){ btn.parentElement.remove(); }

function saveEPS(){
    const rows = Array.from(document.querySelectorAll('#epsList .eps-item'));
    const eps = rows.map(r=>({ title: r.querySelector('.title').value, year: r.querySelector('.year').value, stream_url: r.querySelector('.stream').value, buy_url: r.querySelector('.buy').value, artist: r.querySelector('.artist') }));
    fetch('/update eps', {method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({eps})})
    .then(r=>r.json()).then(j=>notify(j.message)).catch(()=>notify('Error'))
}




function saveLatest() {
    const sInput = document.getElementById('s-url');
    const vInput = document.getElementById('v-url');
    const streamingUrl = sInput.value.trim();
    const vidUrl = vInput.value.trim();

    if (!streamingUrl && !vidUrl) {
        notify("Please enter at least one URL");
        return;
    }

    fetch('/add latest', {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            'latest': [vidUrl, streamingUrl]
        })
    })
    .then(r => r.json())
    .then(j => {
        notify(j.message);

        //Update DOM
        const container = document.getElementById('latestList');
        const inputRow = container.querySelector('.latest-item');
        container.querySelectorAll('.eps-item').forEach(el => el.remove());
        

        const appendNewLink = (url) => {
            if (!url) return;
            
            const div = document.createElement('div');
            div.className = 'eps-item';
            div.innerHTML = `<span><a href="${url}" target="_blank">${url}</a></span>`;
            
            container.insertBefore(div, inputRow);
        };

        // Add the new links visually
        appendNewLink(vidUrl);
        appendNewLink(streamingUrl);

        sInput.value = '';
        vInput.value = '';
    })
    .catch((e) => {
        console.error(e);
        notify('Error saving data');
    });
}

 const hamburger = document.getElementById("hamburger");
const navLinks = document.getElementById("navLinks");

hamburger.addEventListener("click", () => {
    navLinks.classList.toggle("active");
    }
)
