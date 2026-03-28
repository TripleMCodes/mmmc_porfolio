const notification = document.getElementById('notification');

        function notify(message, type = 'success') {
            notification.textContent = message;
            notification.className = 'notification on ' + type;
            setTimeout(() => notification.classList.remove('on'), 3000);
        }

        // Live preview updates
        // document.getElementById('configAvatar').addEventListener('input', function() {
        //     document.getElementById('previewAvatar').textContent = this.value;
        // });
        // document.getElementById('configName').addEventListener('input', function() {
        //     document.getElementById('previewName').textContent = this.value;
        // });
        // document.getElementById('configHandle').addEventListener('input', function() {
        //     document.getElementById('previewHandle').textContent = this.value || 'Lyrical Linguist • Ghostwriter';
        // });
        // document.getElementById('configBio').addEventListener('input', function() {
        //     document.getElementById('previewBio').textContent = this.value || 'Precision language engineering for artists, producers and brands — select a link below.';
        // });

        function saveLinktreeConfig() {
            const avatar = document.getElementById('configAvatar').value.trim() ;
            const name = document.getElementById('configName').value.trim() ;
            const handle = document.getElementById('configHandle').value.trim();
            const bio = document.getElementById('configBio').value.trim() ;
            const email = document.getElementById('configEmail').value.trim();

            let data = {}
            if (avatar) data['avatar'] = avatar;
            if (name) data['name'] = name;
            if (handle) data['handle'] = handle;
            if (bio) data['bio'] = bio;
            if (email) data['email'] = email;

            fetch('/update linktree config', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify(data)
            })
            .then(r => r.json())
            .then(j => {
                notify(j.message, 'success');
                setTimeout(() => location.reload(), 1500);
            })
            .catch(() => notify('Error saving configuration', 'error'));
        }

        function createLink() {
            const text = document.getElementById('newText').value.trim();
            const url = document.getElementById('newUrl').value.trim();
            const is_secondary = document.getElementById('newSecondary').checked;

            if (!text || !url) {
                notify('Text and URL are required', 'error');
                return;
            }

            fetch('/create linktree link', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({text, url, is_secondary})
            })
            .then(r => r.json())
            .then(j => {
                notify('Link created! Refresh to see it.', 'success');
                document.getElementById('newText').value = '';
                document.getElementById('newUrl').value = '';
                document.getElementById('newSecondary').checked = false;
                setTimeout(() => window.location.reload(), 1500);
            })
            .catch(() => notify('Error creating link', 'error'));
        }

        function editLinkModal(id, text, url, is_secondary) {
            document.getElementById('editId').value = id;
            document.getElementById('editText').value = text;
            document.getElementById('editUrl').value = url;
            document.getElementById('editSecondary').checked = is_secondary;
            document.getElementById('editModal').classList.add('open');
        }

        function closeEditModal() {
            document.getElementById('editModal').classList.remove('open');
        }

        function saveLinkEdit() {
            const id = document.getElementById('editId').value;
            const text = document.getElementById('editText').value.trim();
            const url = document.getElementById('editUrl').value.trim();
            const is_secondary = document.getElementById('editSecondary').checked;

            if (!text || !url) {
                notify('Text and URL are required', 'error');
                return;
            }

            fetch(`/edit linktree link/${id}`, {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({text, url, is_secondary})
            })
            .then(r => r.json())
            .then(j => {
                notify(j.message, 'success');
                closeEditModal();
                setTimeout(() => window.location.reload(), 1000);
            })
            .catch(() => notify('Error updating link', 'error'));
        }

        function deleteLink(id) {
            if (confirm('Are you sure you want to delete this link?')) {
                fetch(`/delete linktree link/${id}`, {method: 'POST'})
                .then(r => r.json())
                .then(j => {
                    notify(j.message, 'success');
                    setTimeout(() => window.location.reload(), 1000);
                })
                .catch(() => notify('Error deleting link', 'error'));
            }
        }

     const hamburger = document.getElementById("hamburger");
        const navLinks = document.getElementById("navLinks");

        hamburger.addEventListener("click", () => {
            navLinks.classList.toggle("active");
            }
        )