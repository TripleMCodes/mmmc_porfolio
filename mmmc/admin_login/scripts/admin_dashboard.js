
let name_input = document.querySelector('#name');
let name_btn_input = document.querySelector('#name-btn')

let skill_input = document.querySelector('#skill')
let skill_btn = document.querySelector('.skill-btn')

let about_textarea = document.querySelector('#about')
let about_btn = document.querySelector('.about-btn')

let profile_pic_file = document.querySelector('#pp')
let update_pp_btn = document.querySelector(".upload-pp")

let banner_pic_file = document.querySelector('#bp')
let update_bp_btn = document.querySelector('.upload-bp')

let msgBox = document.querySelector('.notification')
let notyTimeout;

let old_password_input = document.querySelector('#old-password')
let new_password_input = document.querySelector('#new-password')
let email_input = document.querySelector('#email')
let password_btn_input = document.querySelector('#password-btn')


let old_email_input = document.querySelector('#old-email')
let new_email_input = document.querySelector('#new-email')
let password_input = document.querySelector('#password')
let email_btn = document.querySelector('#email-btn')


// notification functions
function removeMsg() {
    msgBox.classList.remove('on');
    msgBox.classList.add('off');
    msgBox.children[0].classList.add('off')
}

function notify(notification) {
    clearTimeout(notyTimeout);
    msgBox.classList.remove('off');
     msgBox.children[0].classList.remove('off')
    msgBox.classList.add('on');
    msgBox.children[0].innerText = notification;
    notyTimeout = setTimeout(removeMsg, 5000);
}


name_btn_input.addEventListener('click', function () {
    let updated_name = name_input.value;
    let data = {};
    data['updated name'] = updated_name;
    
    fetch('/update name', {
        method: 'POST',
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(data)
    }).then(response => response.json())
        .then(data => {
            let n = data.message;
            name_input.value = ""
            notify(n);
            alert(n)
    }).catch(err => {
        let n = 'Error - Name not updated';
        notify(n)
        alert(n)
        return ""
    })
})


email_btn.addEventListener('click', function () {
    let old_email = old_email_input.value
    let new_email = new_email_input.value
    let password = password_input.value

    fetch('/update email', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            "old_email": old_email,
            "new_email": new_email,
            "password": password
        })
    }).then(response => response.json())
        .then(data => {
            old_email_input.value = ''
            new_email_input.value = ''
            password_input.value = ''
            notify(data.message)
            alert(data.message)
            return
        }).catch(error => {
            alert("Error - Password not updated")
            return
        })
})


password_btn_input.addEventListener('click', function () {
    let old_password = old_password_input.value
    let new_password = new_password_input.value
    let email = email_input.value

    if (!old_password || !new_password || !email) {
        alert("Error - password or email input empty")
        return
    }
   
    fetch('/update password', {
        method: 'POST',
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({'old_password': old_password, "new_password": new_password, "email": email})
    }).then(response => response.json())
        .then(data => {
            let n = data.message;
            old_password_input.value = ""
            new_password_input.value = ""
            email_input.value = ""
            notify(n);
            alert(n)
        } 
    ).catch(error => {
        let n = 'Error - Password not updated';
        alert(n)
        notify(n)
        return ""
    })
})



skill_btn.addEventListener('click', function () {
    let new_skill = skill_input.value;
    let data = {};
    data['new skill'] = new_skill

    fetch('/add skill', {
        method: 'POST',
        headers: {
        "Content-Type": "application/json"
    },
        body: JSON.stringify(data)
    }).then(response => response.json())
        .then(data => {
            let n = data.message
            skill_input.value = ""
            notify(n)
            if (data.skill) {
                appendSkill(data.skill);
            }
        }).catch(err => {
            let n = 'Error - Skill not added'
            notify(n)
            alert(n)
            return ""
    })
})

function appendSkill(skill) {
    const skillsList = document.querySelector('.skills-list');
    const span = document.createElement('span');
    span.className = 'skill-item';
    span.innerHTML = `${skill.skill} <button class="delete-skill-btn" onclick="deleteSkill(${skill.id})">×</button>`;
    skillsList.appendChild(span);
}

about_btn.addEventListener('click', function () {
    // find: How to disable a dom element
    let new_about = about_textarea.value
    let data = {}

    data['updated about'] = new_about
    fetch('/update about', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    }).then(response => response.json())
        .then(data => {
            let n = data.message
            about_textarea.value = ''
            notify(n)
            alert(n)
        }).catch(err => {
            let n = 'Error - Short About not updated'
            notify(n)
            alert(n)
    })
})

update_pp_btn.addEventListener('click', function () {
    let file = profile_pic_file.files[0];
    if (!file) {
        notify('No file selected');
        return;
    }
    let formData = new FormData();
    formData.append('profile_picture', file);
    
    fetch('/update profile picture', {
        method: 'POST',
        body: formData
    }).then(response => response.json())
        .then(data => {
            let n = data.message;
            profile_pic_file.value = "";
            notify(n);
            alert(n)
        }).catch(err => {
            let n = 'Error - Profile picture not updated';
            notify(n);
            alert(n)
        });
})

update_bp_btn.addEventListener('click', function () {
    let file = banner_pic_file.files[0];
    if (!file) {
        notify('No file selected');
        return;
    }
    let formData = new FormData();
    formData.append('banner_picture', file);
    
    fetch('/update banner picture', {
        method: 'POST',
        body: formData
    }).then(response => response.json())
        .then(data => {
            let n = data.message;
            banner_pic_file.value = "";
            notify(n);
            alert(n)
        }).catch(err => {
            let n = 'Error - Banner picture not updated';
            notify(n);
            alert(n)
        });
})

function deleteSkill(id) {
    if (confirm('Are you sure you want to delete this skill?')) {
        fetch(`/delete skill/${id}`, {
            method: 'POST'
        }).then(response => response.json())
        .then(data => {
            notify(data.message);
            alert(data.message)
            // Remove the skill item from DOM
            const button = document.querySelector(`.delete-skill-btn[onclick="deleteSkill(${id})"]`);
            if (button) {
                button.parentElement.remove();
            }
        }).catch(err => {
            notify('Error deleting skill');
            alert('Error deleting skill');
        });
    }
}



const ga4Input = document.getElementById("ga4-id");
const ga4SaveBtn = document.getElementById("ga4-save-btn");
const ga4Message = document.getElementById("ga4-message");

if (ga4SaveBtn) {
    ga4SaveBtn.addEventListener("click", async () => {
        const ga4MeasurementId = ga4Input.value.trim();

        ga4Message.textContent = "";
        ga4Message.style.color = "";

        if (!ga4MeasurementId) {
            ga4Message.textContent = "Please enter a GA4 Measurement ID.";
            ga4Message.style.color = "red";
            return;
        }

        try {
            const response = await fetch("/save-update-ga4", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    name: "mmmc",
                    ga4_measurement_id: ga4MeasurementId
                })
            });

            const data = await response.json();

            if (response.ok && data.success) {
                ga4Message.textContent = data.message || "GA4 Measurement ID saved successfully.";
                ga4Message.style.color = "green";
            } else {
                ga4Message.textContent = data.message || "Failed to save GA4 Measurement ID.";
                ga4Message.style.color = "red";
            }
        } catch (error) {
            console.error("GA4 save/update error:", error);
            ga4Message.textContent = "Something went wrong while saving the GA4 ID.";
            ga4Message.style.color = "red";
        }
    });
}